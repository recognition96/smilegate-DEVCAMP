from twitter_streaming import TwitterConnector
from kafka_producer import Producer
from config import *


def run():
    # CLI 실행시 config 파일 선택 가능
    # if len(sys.argv) != 2:
    #     print("Usage : python {.py file} {kafka_config_file}")
    #     sys.exit(1)
    # kafka_config = Config(sys.argv[1])

    # kafka producer 초기화
    kafka_config = Config('configs/kafka_config.conf')
    host = kafka_config.load_config('BROKER', 'host1')
    port = kafka_config.load_config('BROKER', 'port_default')
    topic = kafka_config.load_config('TOPIC', 'covid_kor')
    producer = Producer(host=host, port=port)

    # twitter api 연결
    twitter_api = TwitterConnector()
    twitter_api.init_stream_rules()
    twitter_api.start_stream(producer=producer, topic=topic)


if __name__ == "__main__":
    run()

