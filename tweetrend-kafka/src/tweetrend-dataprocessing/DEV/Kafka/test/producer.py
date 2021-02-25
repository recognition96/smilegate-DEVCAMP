from kafka import KafkaProducer
from json import dumps
import time

"""
Kafka Producer Option
 - bootstrap_servers(default=9092): 브로커(host:port)를 리스트로 나열, 노드 전부를 쓸 필요는 없음
 - acks(default=1): 0, 서버로부터 어떠한 ack도 기다리지 않음. 처리량 증가하지만 유실율도 증가
                    1, 리더의 기록을 확인 후 ack 받음. 모든 팔로워에 대해서 확인하지는 않음
                    'all', 모든 ISR(리더의 모든 팔로워)의 기록을 확인 후 ack 받음. 무손실 보장
 - compression_type(default=None): 데이터를 압축하여 보낼 포멧 (‘gzip’, ‘snappy’, ‘lz4’, or None)
 - value_serializer(default=None): 유저가 보내려는 msg를 byte의 형태로 직렬화할 함수(callable). 여기서는 변환 후 인코딩
"""
producer = KafkaProducer(
    bootstrap_servers=["localhost:9093"],
    acks=-1,
    compression_type="gzip",
    value_serializer=lambda x: x.encode("utf-8"),
    batch_size=1024 * 16,
    linger_ms=5,
)

if __name__ == '__main__':
    start = time.time()
    for _ in range(100):
        producer.send("dev_topic", value="TEST STRING")
        producer.flush()
        time.sleep(1)
    print("elapsed :", time.time() - start)
