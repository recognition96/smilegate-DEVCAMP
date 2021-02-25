from datetime import datetime, time, timedelta
import kafka_producer
import kafka_consumer
import config
import copy
import random
import json
from logger import Log
import time as t
config = config.Config([None, 'configs/kafka_config.conf'])

class DataGenerator:
    def __init__(self):
        init_datetime = datetime.utcnow()
        self.init_hms = [init_datetime.hour, init_datetime.minute, init_datetime.second]
        self.daily_cnt = 0
        self.producer = kafka_producer.Producer('localhost', '9093')
        Log.i("DataGenerator on.")

    def load_data_from_broker(self):
        consumer = kafka_consumer.Consumer('localhost', '9092', 'test')
        for origin_tweet in consumer.consumer:
            print(origin_tweet.value)
            self.make_days_random_data(origin_tweet.value)

    def toggle_time_format(self, source_time):
        if isinstance(source_time, str) and source_time[-1] == 'Z':
            return datetime.strptime(source_time, "%Y-%m-%dT%H:%M:%S.000Z")
        else:
            return source_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    def make_diff_time_data(self, origin_data: dict, diff_day=5, diff_time='000000'):
        if 'created_at' in origin_data['data']:
            new_data = copy.deepcopy(origin_data)
            datetime_origin = self.toggle_time_format(origin_data['data']['created_at'])
            diff = timedelta(days=diff_day, hours=int(diff_time[:2]), minutes=int(diff_time[2:4]), seconds=int(diff_time[4:6]))

            new_created_at = self.toggle_time_format(datetime_origin + diff)
            new_data['data']['created_at'] = new_created_at
        else:
            Log.e("KEYERROR no 'created_at' in origin_data['data'].")

    def make_days_random_data(self, origin_data, days=7, num_of_tweets=20000):
        if 'created_at' in origin_data['data']:
            if self.daily_cnt >= num_of_tweets:
                exit()
            else:
                start = t.time()
                while (num_of_tweets) > 0:
                    data = json.dumps(origin_data, ensure_ascii=False)
                    self.producer.send_data('test', data)
                    num_of_tweets -= 1
                print("elapsed :", t.time() - start)
        else:
            Log.e("KEYERROR no 'created_at' in origin_data['data'].")


if __name__ == '__main__':
    generator = DataGenerator()
    generator.load_data_from_broker()
