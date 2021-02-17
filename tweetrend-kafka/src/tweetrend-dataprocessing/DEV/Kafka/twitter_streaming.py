from TwitterAPI import (
    TwitterAPI,
    TwitterOAuth,
    TwitterRequestError,
    TwitterConnectionError,
)
from logger import Log
import json
import datetime
import time
import config


class TwitterConnector:
    def __init__(self):
        """
        twitter API 를 사용하기 위해 API KEY를 이용해 연결하고, 요청에 필요한 파라미터를 초기화
        실시간 데이터를 응답받기 위해선 twitter 에서 정해놓은 query 형식에 따라 rule 을 등록한 후 요청해야 함
        모든 rule 은 계정(API KEY)에 연동되고 각가 id로 구분되며, 추가적인 등록/삭제가 없다면 변경되지 않음
        여기서 rule 이란 특정한 조건을 만족하는 streaming data 를 받기위한 filtering 방법
        """
        try:
            auth_info = TwitterOAuth.read_file()
            self.api = TwitterAPI(
                auth_info.consumer_key,
                auth_info.consumer_secret,
                auth_type="oAuth2",
                api_version="2",
            )
        except TwitterRequestError as e:
            msg_list = []
            for msg in iter(e):
                msg_list.append(msg)
            err_msg = "RequestError: " + "|".join(msg_list)
            Log.e(err_msg)

        except TwitterConnectionError as e:
            Log.e(f"ConnectionError: {e}")
            self.prompt_reconnect_msg(2)

        except Exception as e:
            Log.e(f"BaseException: {e}")
            self.prompt_reconnect_msg(2)

        # twitter conifg 파일
        twitter_config = config.Config('configs/twitter_config.conf')

        self.query_string = twitter_config.load_config('API_QUERY', 'rules')
        self.output_file_name = twitter_config.load_config('OUTPUT_FILES', 'stream_result')

        # comma-seperated list with no space between fields
        self.expansions = twitter_config.load_config('CONTENTS', 'expansions')
        self.media_fields = twitter_config.load_config('CONTENTS', 'media_fields')
        self.tweet_fields = twitter_config.load_config('CONTENTS', 'tweet_fields')
        self.user_fields = twitter_config.load_config('CONTENTS', 'user_fields')
        self.place_fields = twitter_config.load_config('CONTENTS', 'place_fields')

    def init_stream_rules(self):
        """
        기존에 등록된 모든 rule 을 제거하고, 초기 rule 을 등록

        :return: -
        """
        cur_rules = self.get_stream_rules()
        self.delete_stream_rules(cur_rules)
        self.add_stream_rules(self.query_string)

    def add_stream_rules(self, request_query):
        """
        계정에 특정 rule 을 등록

        :param request_query: [str] 문법에 맞는 쿼리문
        :return: -
        """
        try:
            response = self.api.request(
                "tweets/search/stream/rules", {"add": [{"value": request_query}]}
            )
            Log.i(f"[{response.status_code}] RULE ADDED: {response.text}")
            if response.status_code != 201:
                raise Exception(response.text)

        except TwitterRequestError as e:
            msg_list = []
            for msg in iter(e):
                msg_list.append(msg)
            err_msg = "RequestError: " + "|".join(msg_list)
            Log.e(err_msg)

        except TwitterConnectionError as e:
            Log.e(f"ConnectionError: {e}")
            self.prompt_reconnect_msg(2)

        except Exception as e:
            Log.e(f"BaseException: {e}")
            self.prompt_reconnect_msg(2)

    def get_stream_rules(self):
        """
        현재 계정에 등록된 rule 목록을 조회

        :return: [list(str)] rule's ids
        """
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
            msg_list = []
            for msg in iter(e):
                msg_list.append(msg)
            err_msg = "RequestError: " + "|".join(msg_list)
            Log.e(err_msg)

        except TwitterConnectionError as e:
            Log.e(f"ConnectionError: {e}")
            self.prompt_reconnect_msg(2)

        except Exception as e:
            Log.e(f"BaseException: {e}")
            self.prompt_reconnect_msg(2)

    def delete_stream_rules(self, rule_ids):
        """
        특정 rule 을 삭제

        :param rule_ids: [list(str)] 삭제 하기위한 rule 의 id 목록
        :return: -
        """
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
            msg_list = []
            for msg in iter(e):
                msg_list.append(msg)
            err_msg = "RequestError: " + "|".join(msg_list)
            Log.e(err_msg)

        except TwitterConnectionError as e:
            Log.e(f"ConnectionError: {e}")
            self.prompt_reconnect_msg(2)

        except Exception as e:
            Log.e(f"BaseException: {e}")
            self.prompt_reconnect_msg(2)

    def start_stream(self, producer, topic):
        """
        계정에 등록된 rule 에 따라 filtered streaming data 를 받아옴
        data를 정상적으로 받아오고 있다면 오류/종료 전까지 반복문에서 빠져나오지 않음
        에러 원인에 따라 재연결을 시도하여 서버가 유지될 수 있도록 함
        rule 과 별개로 하나의 tweet 에서 받아오고자 하는 정보를 쿼리에 포함시킬 수 있음

        kafka 의 prodcer 역할을 하는 부분으로 받아오는 data 를 producer 와 연결된 broker 로 전달함

        :param producer: [kafka.producer] kafka 의 produce 객체
        :param topic: [str] 데이터를 전달하고자하는 broker 의 특정 topic

        :return: -
        """
        total_cnt = 0
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

                if (
                    response.status_code != 200
                    and response.status_code != 400
                    and response.status_code != 429
                ):
                    # 에러 원인별 다른 처리를 위해 응답 코드로 구분
                    raise Exception(response)

                with open(
                    self.output_file_name, "a", encoding="utf-8"
                ) as output_file, open("logs/data_count.txt", "a") as cnt_file:
                    # data_count.txt : 유실을 확인하기위해 count
                    # [데이터를 받아온 시간] 해당 tweet 의 게시 시간 (파일이 open 된 후 받아온 데이터의 수 / 프로그램이 실행된 후 받아온 데이터의 수)
                    print(f"[{datetime.datetime.now()}] file re-open", file=cnt_file)
                    for no, item in enumerate(response):
                        self.check_error_response(item)
                        data = json.dumps(item, ensure_ascii=False)
                        print(data, file=output_file, flush=True)
                        producer.send_data(topic=topic, data=data)
                        print(
                            f"[{datetime.datetime.now()}] {item['data']['created_at']} ({no} / {total_cnt})",
                            file=cnt_file,
                            flush=True,
                        )
                        total_cnt += 1

            except TwitterRequestError as e:
                # ConnectionException will be caught here

                msg_list = []
                for msg in iter(e):
                    msg_list.append(msg)
                err_msg = "RequestError: " + "|".join(msg_list)
                Log.e(err_msg)

                if e.status_code >= 500:
                    self.prompt_reconnect_msg(3)
                elif e.status_code == 429:
                    self.prompt_reconnect_msg(63)
                else:
                    exit()

            except TwitterConnectionError as e:
                Log.e(f"ConnectionError: {e}")
                self.prompt_reconnect_msg(3)

            except Exception as e:
                Log.e(f"Exception: {e}")
                self.prompt_reconnect_msg(3)

    def check_error_response(self, item):
        """
        twitter api 의 response 가 error 메세지 일 경우 데이터 포멧이 다르므로 따로 처리

        :param item: [dict] twitter api response data
        :return: terminate | raise Exception
        """
        error_type = {
            # 에러 원인 중 해당 정보를 제공하는 겨우 재연결 시도가 의미없으므로 프로그램 종료
            "CRITICAL": [
                "https://api.twitter.com/2/problems/usage-capped",
                "https://api.twitter.com/2/problems/rule-cap",
                "https://api.twitter.com/2/problems/invalid-rules",
                "https://api.twitter.com/2/problems/duplicate-rules",
            ]
        }
        if "data" in item:
            return
        elif "errors" in item:
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
        안내문구 출력 후 특정시간 동안 대기
        아래와 같은 이용 정책을 준수하기 위해 최소 요구되는 대기 시간은 2~3초로 판단

        Twitter API has usage rate limit (Per 15m)
        - 50 connect
        - 450 adding, deleting, listing

        :param wait_secs: [int] 대기 시간 (초)
        :return: -
        """
        Log.i(f"wait {wait_secs}secs for reconnecting..")
        time.sleep(wait_secs)
