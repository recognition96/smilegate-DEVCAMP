from TwitterAPI import (
    TwitterAPI,
    TwitterOAuth,
    TwitterRequestError,
    TwitterConnectionError,
)
from apscheduler.schedulers.background import BackgroundScheduler
from logger import Log
import json
import datetime
import time

"""
twitter api response 를 5초마다 집계하여 누적 카운트하는 테스트(batch test)
"""


class TwitterConnector:
    def __init__(self):
        try:
            auth_info = TwitterOAuth.read_file()
            self.api = TwitterAPI(
                auth_info.consumer_key,
                auth_info.consumer_secret,
                auth_type="oAuth2",
                api_version="2",
            )
        except TwitterRequestError as e:
            msg_list = ["RequestError:", e]
            for msg in iter(e):
                msg_list.append(msg)
            err_msg = " ".join(msg_list)
            Log.e(err_msg)

        except TwitterConnectionError as e:
            Log.e(f"ConnectionError: {e}")
            self.prompt_reconnect_msg(2)

        except Exception as e:
            Log.e(f"BaseException: {e}")
            self.prompt_reconnect_msg(2)

        # comma-seperated list with no space between fields
        self.expansions = "attachments.media_keys,author_id,entities.mentions.username,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id,geo.place_id"
        self.media_fields = "preview_image_url,type,url,public_metrics"
        self.tweet_fields = "id,text,attachments,author_id,conversation_id,created_at,entities,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,source"
        self.user_fields = "entities,id,name,username,profile_image_url,verified"
        self.place_fields = "full_name,id,country,country_code,name,place_type"

        self.output_file_name = "../logs/stream_result.txt"

    def init_stream_rules(self, query_string):
        cur_rules = self.get_stream_rules()
        self.delete_stream_rules(cur_rules)
        self.add_stream_rules(query_string)

    def add_stream_rules(self, request_query):
        try:
            response = self.api.request(
                "tweets/search/stream/rules", {"add": [{"value": request_query}]}
            )
            Log.i(f"[{response.status_code}] RULE ADDED: {response.text}")
            if response.status_code != 201:
                raise Exception(response.text)

        except TwitterRequestError as e:
            msg_list = ["RequestError:", e]
            for msg in iter(e):
                msg_list.append(msg)
            err_msg = " ".join(msg_list)
            Log.e(err_msg)

        except TwitterConnectionError as e:
            Log.e(f"ConnectionError: {e}")
            self.prompt_reconnect_msg(2)

        except Exception as e:
            Log.e(f"BaseException: {e}")
            self.prompt_reconnect_msg(2)

    def get_stream_rules(self):
        rule_ids = []
        try:
            response = self.api.request(
                "tweets/search/stream/rules", method_override="GET"
            )
            Log.i(f"[{response.status_code}] RULES: {response.text}")
            if response.status_code != 200:
                raise Exception(response.text)
            else:
                for item in response:
                    if "id" in item:
                        rule_ids.append(item["id"])
                    else:
                        Log.i(json.dumps(item, ensure_ascii=False))
                return rule_ids

        except TwitterRequestError as e:
            msg_list = ["RequestError:", e]
            for msg in iter(e):
                msg_list.append(msg)
            err_msg = " ".join(msg_list)
            Log.e(err_msg)

        except TwitterConnectionError as e:
            Log.e(f"ConnectionError: {e}")
            self.prompt_reconnect_msg(2)

        except Exception as e:
            Log.e(f"BaseException: {e}")
            self.prompt_reconnect_msg(2)

    def delete_stream_rules(self, rule_ids):
        try:
            if len(rule_ids) > 0:
                response = self.api.request(
                    "tweets/search/stream/rules", {"delete": {"ids": rule_ids}}
                )
                Log.i(
                    f"[{response.status_code}] RULES DELETED: {json.dumps(response.json())}"
                )
                if response.status_code != 200:
                    raise Exception(response.text)

        except TwitterRequestError as e:
            msg_list = ["RequestError:", e]
            for msg in iter(e):
                msg_list.append(msg)
            err_msg = " ".join(msg_list)
            Log.e(err_msg)

        except TwitterConnectionError as e:
            Log.e(f"ConnectionError: {e}")
            self.prompt_reconnect_msg(2)

        except Exception as e:
            Log.e(f"BaseException: {e}")
            self.prompt_reconnect_msg(2)

    def start_stream(self, producer, topic):
        total_cnt = [0]  # 스케줄러 함수의 인자로, 값이 변경될 수 있도록 mutable 객체인 list 로 선언
        while True:
            try:
                response = self.api.request(
                    "tweets/search/stream",
                    {
                        "expansions": self.expansions,
                        "media.fields": self.media_fields,
                        "tweet.fields": self.tweet_fields,
                        "user.fields": self.user_fields,
                        "place.fields": self.place_fields,
                    },
                )
                Log.i(f"[{response.status_code}] START...")
                Log.i(response.get_quota())  # API connect 회수 조회
                if response.status_code != 200 and response.status_code != 429:
                    raise Exception(response)

                elif response.status_code != 200:
                    # 그 외의 경우 예외처리 및 재연결 시도
                    raise Exception(response)

                with open(
                    self.output_file_name, "a", encoding="utf-8"
                ) as output_file, open("../logs/data_count.txt", "a") as cnt_file:
                    print(f"[{datetime.datetime.now()}] file re-open", file=cnt_file)
                    scheduler = BackgroundScheduler()  # 5초마다 실행을 위해 백그라운드 스케줄러 사용
                    batch_cnt = [0]  # 5초 간격으로 함수 내에서 reset 하기 위해 mutable 객체인 list 로 선언
                    scheduler.add_job(
                        self.print_periodically,
                        "cron",
                        second="*/5",
                        args=[batch_cnt, total_cnt, cnt_file],
                    )
                    scheduler.start()

                    for item in response:
                        self.check_error_response(item)
                        data = json.dumps(item, ensure_ascii=False)
                        print(data, file=output_file, flush=True)
                        producer.send_data(topic=topic, data=data)

                        batch_cnt[0] += 1
                        total_cnt[0] += 1

            except TwitterRequestError as e:
                msg_list = ["RequestError:", e]
                for msg in iter(e):
                    msg_list.append(msg)
                err_msg = " ".join(msg_list)
                Log.e(err_msg)
                if e.status_code >= 500:
                    self.prompt_reconnect_msg(2)
                elif e.status_code == 429:
                    self.prompt_reconnect_msg(60)
                else:
                    exit()

            except TwitterConnectionError as e:
                Log.e(f"ConnectionError: {e}")
                self.prompt_reconnect_msg(2)

            except Exception as e:
                Log.e(f"Exception: {e}")
                self.prompt_reconnect_msg(2)

    def check_error_response(self, item):
        """
        twitter api 의 response 가 error 메세지 일 경우 따로 처리

        :param item: [dict] twitter api response data
        :return: terminate | raise Exception
        """
        error_type = {
            "CRITICAL": [
                "https://api.twitter.com/2/problems/usage-capped",
                "https://api.twitter.com/2/problems/rule-cap",
                "https://api.twitter.com/2/problems/invalid-rules",
                "https://api.twitter.com/2/problems/duplicate-rules",
            ]
        }
        if "errors" in item:
            title_ = item["errors"][0]["title"]
            detail_ = item["errors"][0]["detail"]
            type_ = item["errors"][0]["type"]

            ret_msg = [title_, detail_, type_]
            ret_msg = "|".join(ret_msg)

            if type_ in error_type["CRITICAL"]:
                Log.c(ret_msg)
                exit()
            else:
                raise Exception(ret_msg)

    def prompt_reconnect_msg(self, wait_secs):
        """
        Twitter API has usage rate limit (Per 15m)
        - 50 connect
        - 450 adding, deleting, listing

        :param wait_secs:
        :return:
        """
        Log.i(f"wait {wait_secs}secs for reconnecting..")
        time.sleep(wait_secs)

    def print_periodically(self, batch_cnt, total_cnt, file_name=None):
        print(
            f"[{datetime.datetime.now()}] batch_cnt : {batch_cnt[0]} / total_cnt : {total_cnt[0]})",
            file=file_name,
            flush=True,
        )
        batch_cnt[0] = 0  # 5초 마다 호출 후에 변수를 reset
