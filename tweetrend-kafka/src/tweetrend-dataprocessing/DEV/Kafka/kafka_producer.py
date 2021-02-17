from kafka import KafkaProducer
from kafka.errors import KafkaError
from logger import Log


class Producer:
    def __init__(self, host="localhost", port="9092"):
        """
        Kafka Producer Option (not all)
         - bootstrap_servers(default=9092): 브로커(host:port)를 리스트로 나열, 노드 전부를 쓸 필요는 없음
         - acks(default=1): 0, 서버로부터 어떠한 ack도 기다리지 않음. 처리량 증가하지만 유실율도 증가
                            1, 리더의 기록을 확인 후 ack 받음. 모든 팔로워에 대해서 확인하지는 않음
                            'all', 모든 ISR(리더의 모든 팔로워)의 기록을 확인 후 ack 받음. 무손실 보장
         - compression_type(default=None): 데이터를 압축하여 보낼 포멧 (‘gzip’, ‘snappy’, ‘lz4’, or None)
         - value_serializer(default=None): 유저가 보내려는 msg를 byte의 형태로 변환할 함수(callable). 여기서는 변환 후 인코딩
        """
        try:
            self.producer = KafkaProducer(
                api_version=(2, 7, 0),
                bootstrap_servers=[f"{host}:{port}"],
                acks=-1,
                compression_type="gzip",
                value_serializer=lambda x: x.encode("utf-8"),
                batch_size=1024*64,
                linger_ms=10,
            )
        except KafkaError as e:
            Log.e(f"KafkaProducer fail. {e}")
        Log.i("KafkaProducer connect.")

    def send_data(self, topic, data):
        """
        Kafka 의 producer 객체를 통해 연결된 broker 에게 데이터를 전송

        :param topic: [str] 데이터를 전송하고자 하는 연결된 broker 의 특정 topic
        :param data: [OPTIONAL] broker 에게 전다랗고자 하는 data
        :return: -
        """
        self.producer.send(topic, value=data).add_callback(self.on_send_success).add_errback(self.on_send_error)
        # flush 를 사용하면 batch size 나 linger_ms 에 구애받지 않고 producer 내의 buffer 를 비워 broker 에게 전달
        # self.producer.flush()

    def on_send_success(self, record_metadata):
        """
        send 함수의 callback 으로 데이터가 broker 에게 전달된 것이 확인된 후 호출됨

        :param record_metadata: 전달 후 broker에 저장된 데이터에 대한 metadata
        :return: -
        """
        Log.d(f"{record_metadata.topic}, {record_metadata.partition}, {record_metadata.offset}")

    def on_send_error(self, exception):
        """
        send 함수의 callback 으로 데이터가 broker 에게 전달되지 못할 시 호출됨

        :param exception: 전달에 실패한 오류(kafka exception)에 대한 설명
        :return: -
        """
        Log.e(f"{exception}")