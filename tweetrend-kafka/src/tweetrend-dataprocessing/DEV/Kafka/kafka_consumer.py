from kafka import KafkaConsumer
from kafka.errors import KafkaError
from logger import Log
from json import loads
import time


class Consumer:
    def __init__(self, topic='covid_kor', consumer_group='my-group', host="localhost", port="9092"):
        """
        Kafka Consumer Option (not all)
         - bootstrap_servers(default=9092): 브로커(host:port)를 리스트로 나열, 노드 전부를 쓸 필요는 없음
         - auto_offset_reset(default='latest'): 0, 서버로부터 어떠한 ack도 기다리지 않음. 처리량 증가하지만 유실율도 증가
                            1, 리더의 기록을 확인 후 ack 받음. 모든 팔로워에 대해서 확인하지는 않음
                            'all', 모든 ISR(리더의 모든 팔로워)의 기록을 확인 후 ack 받음. 무손실 보장
         - enable_auto_commit(default=True): 데이터를 압축하여 보낼 포멧 (‘gzip’, ‘snappy’, ‘lz4’, or None)
         - value_deserializer(default=None): 압축된 msg를 받았을 때 이를 역직렬화할 함수(callable).
                                             (producer 의 serializer와 동일한 값으로 하지않으면 예외 발생)
        """
        try:
            self.consumer = KafkaConsumer(
                f"{topic}",
                bootstrap_servers=[f"{host}:{port}"],
                auto_offset_reset="latest",
                enable_auto_commit=True,
                group_id=consumer_group,
                value_deserializer=lambda x: loads(x.decode("utf-8")),
                consumer_timeout_ms=1000*60*5,
            )
        except KafkaError as e:
            Log.e(f"KafkaConsuemr fail. {e}")
        Log.i("KafkaConsuemr connect.")


if __name__ == '__main__':
    consumer = Consumer('test', '10.250.93.4', '9092')
    # consumer list를 가져온다
    print("[begin] get consumer list")
    start = time.time()
    for message in consumer.consumer:
        print(
            "Topic: %s, Partition: %d, Offset: %d, Key: %s, Value: %s"
            % (message.topic, message.partition, message.offset, message.key, message.value)
        )
    print(f"[end] get consumer list {time.time() - start}")
