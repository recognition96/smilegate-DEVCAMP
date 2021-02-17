from datetime import datetime, time, timedelta
import kafka_producer
import kafka_consumer
from config import *
import copy
import random
import json
from logger import Log

"""
부족한 데이터 및 테스트를 위해 원본 데이터를 기반으로 새로운 날짜의 데이터를 생성하기 위한 class
"""


class DataGenerator:
    def __init__(self):
        # CLI 실행시 config 파일 선택 가능
        # if len(sys.argv) != 2:
        #     print("Usage : python {.py file} {kafka_config_file}")
        #     sys.exit(1)

        init_datetime = datetime.utcnow()
        self.init_hms = [init_datetime.hour, init_datetime.minute, init_datetime.second]
        self.daily_cnt = 0

        # self.config = Config(sys.argv[1])
        self.config = Config('configs/kafka_config.conf')
        self.host = self.config.load_config('BROKERS', 'host2')
        self.port = self.config.load_config('BROKERS', 'port_default')
        self.producer = kafka_producer.Producer(self.host, self.port)
        Log.i("DataGenerator on.")

    def load_data_from_broker(self):
        """
        기존 kafka 의 broker 로 들어오는 데이터를 consume 하여 source 로 사용하기 위해 data 를 받아 옴
        데이터를 정상적으로 받아오고 있다면 종료되지 않고 반복문에서 계속 실행

        :return: -
        """
        self.topic = self.config.load_config('BROKERS', 'dup')
        self.cosumer_group = self.config.load_config('CONSUMER_GROUP', 'group_default')
        consumer = kafka_consumer.Consumer(self.topic, self.cosumer_group, self.host, self.port)

        for origin_tweet in consumer.consumer:
            print(origin_tweet.value)
            self.make_days_random_data(origin_tweet.value)

    def toggle_time_format(self, source_time):
        """
        twitter API 에서 제공하는 데이터의 시간 format 과 random time 을 생성하기 위한 datetime format 간의 전환

        :param source_time: [datetime.datetime|str] 서로 반대의 format 으로 변환하기 위한 시간 정보
        :return: [str|datetime.datetime] 반대 format 으로 변환된 시간 정보
        """
        if isinstance(source_time, str) and source_time[-1] == 'Z':
            # tweet 에서 제공하는 format 임을 보장하기 위한 'Z' 확인 (Zulu 코드)
            return datetime.strptime(source_time, "%Y-%m-%dT%H:%M:%S.000Z")
        else:
            return source_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    def make_diff_time_data(self, origin_data: dict, diff_day=5, diff_time='000000'):
        """
        원본 tweet 을 기반으로 시간의 차이를 통해 새로운 시간의 tweet 데이터를 생성

        :param origin_data: [Tweet Data] 원본 tweet 데이터
        :param diff_day: [int] 생성하고자 하는 데이터와 원본 데이터의 날짜 차이
        :param diff_time: [str] 생성하고자 하는 데이터와 원본 데이터의 시간 차이('HHMMSS')

        :return: -
        """
        if 'created_at' in origin_data['data']:
            new_data = copy.deepcopy(origin_data)
            datetime_origin = self.toggle_time_format(origin_data['data']['created_at'])
            diff = timedelta(days=diff_day, hours=int(diff_time[:2]), minutes=int(diff_time[2:4]), seconds=int(diff_time[4:6]))

            new_created_at = self.toggle_time_format(datetime_origin + diff)
            new_data['data']['created_at'] = new_created_at
        else:
            Log.e("KEYERROR no 'created_at' in origin_data['data'].")

    def make_days_random_data(self, origin_data, days=6, num_of_tweets=20000):
        """
        원본 tweet 을 기반으로 원하는 날짜, 랜덤한 시간의 새로운 tweet 데이터를 생성하여 broker 에게 전송
        생성하고자 하는 수만큼의 데이터가 생성되었다면 프로그램 종료

        :param origin_data: [Tweet Data] 원본 tweet 데이터
        :param days: [int] 생성하고자 하는 데이터와 원본 데이터의 날짜 차이. 해당하는 일 수만큼의 전날에서 하루 전날까지 포함
        :param num_of_tweets: [int] 범위 내의 모든 날짜마다 생성하고자 하는 tweet 데이터의 수

        :return: -
        """
        if 'created_at' in origin_data['data']:
            if self.daily_cnt >= num_of_tweets:
                exit()
            else:
                datetime_origin = self.toggle_time_format(origin_data['data']['created_at'])
                if datetime_origin.month == 2 and datetime_origin.day > 4:
                    # 특정 날짜를 제거하기 위해 filtering
                    with open("logs/random_data_list", "a", encoding="utf-8") as output_file:
                        # 생성한 데이터 기록
                        for day_ago in range(-days, 0):
                            # 중첩 dictionary의 복제를 위해 deepcopy 사요
                            new_data = copy.deepcopy(origin_data)
                            datetime_post = datetime_origin + timedelta(days=day_ago)
                            random_hms = time(hour=random.randint(0, 23), minute=random.randint(0, 59), second=random.randint(0, 59))
                            # 특정 날짜와 랜덤한 시간을 합친 datetime 생성
                            datetime_post = datetime.combine(datetime_post.date(), random_hms)

                            new_created_at = self.toggle_time_format(datetime_post)
                            # print("new_created_at", new_created_at)
                            new_data['data']['created_at'] = new_created_at
                            new_data = json.dumps(new_data, ensure_ascii=False)

                            self.producer.send_data('test', new_data)
                            print(new_data, file=output_file, flush=True)
                    self.daily_cnt += 1
                    print(self.daily_cnt)
        else:
            Log.e("KEYERROR no 'created_at' in origin_data['data'].")


if __name__ == '__main__':
    generator = DataGenerator()
    generator.load_data_from_broker()