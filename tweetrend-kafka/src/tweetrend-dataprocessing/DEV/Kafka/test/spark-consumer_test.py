from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition
import findspark
from kazoo.client import KazooClient
import json


def get_zookeeper_instance():
    """
    zookeeper instance 등록
    """
    globals()['KazooSingletonInstance'] = KazooClient("localhost:2181")
    globals()['KazooSingletonInstance'].start()
    return globals()['KazooSingletonInstance']


def read_offsets(zk, topics, consumer_group):
    """
    등록된 zookeeper 로부터 특정 topic 을 consume 하는 특정 consumer_group 의 오프셋을 읽어옴
    """
    from_offsets = {}
    for topic in topics:
        child_nodes = zk.get_children(f"/consumers/{consumer_group}/owners/{topic}")
        for partition in child_nodes:
            topic_partition = TopicAndPartition(topic, int(partition))
            partition_offset = zk.get(f"/consumers/{consumer_group}/owners/{topic}/{partition}")
            print(f"{partition} offset :", partition_offset)
            if not partition_offset:
                print('The spark streaming started first time and offset value should be ZERO.')
                offset = 0
            else:
                offset = int(partition_offset[0])
            from_offsets[topic_partition] = offset
    print("from_offset:", from_offsets)
    return from_offsets


def save_offsets(rdd, consumer_group):
    """
    등록된 zookeeper 에게 특정 topic 을 consume 하는 특정 consumer_group 에게 offset 갱신
    """
    zk = get_zookeeper_instance()
    for offset in rdd.offsetRanges():
        print("in offsetRanges()", offset)
        path = f"/consumers/{consumer_group}/owners/{offset.topic}/{offset.partition}"
        zk.ensure_path(path)
        zk.set(path, str(offset.untilOffset).encode())


if __name__ == "__main__":
    findspark.init()

    # SparkContext represents the connection to a Spark cluster
    # Only one SparkContext may be active per JVM
    sc = SparkContext(appName="Kafka Spark Demo")

    # Creating a streaming context with batch interval of 10 sec
    # As the main point of entry for streaming, StreamingContext handles the streaming application's actions,
    # including checkpointing and transformations of the RDD.
    ssc = StreamingContext(sc, 5)

    zookeeper = get_zookeeper_instance()
    from_offsets = read_offsets(zookeeper, ['test'], 'test-group')
    print(from_offsets)

    # kafka option 선택 가능
    kafka_params = {
        "metadata.broker.list": "localhost:9092",
        # "auto.offset.reset": "smallest",
        # "enable.auto.commit": "false",
        # "auto.commit.interval.ms": "30000",
    }


    # DStream(RDD 로 이루어진 객체) 반환
    # kafkaStream = KafkaUtils.createDirectStream(
    #     ssc, topics=["test"], kafkaParams=kafka_params, fromOffsets=from_offsets
    # )
    # print(type(kafkaStream))

    # createdDirectStream 은 zookeeper 의 offset 변경못함
    kafkaStream = KafkaUtils.createStream(
        ssc, 'localhost:2181', 'test-group', topics={'test': 1}, kafkaParams=kafka_params,
    )
    print(type(kafkaStream))

    # kafkaStream.foreachRDD(lambda rdd: save_offsets(rdd, 'tmp'))
    # Parse Twitter Data as json
    json_stream = kafkaStream.map(lambda tweet: json.loads(tweet[1]))
    json_stream.pprint()
    # parsed = json_stream.map(lambda tweet: tweet_filter(tweet))
    # parsed.foreachRDD(lambda x: x.saveToCassandra("bts", "tweet_dataset"))
    # parsed.pprint()

    # Count Twitter Data by word
    # words = kafkaStream.map(lambda x: x[1]).flatMap(lambda x: x.split(" "))
    # wordcount = words.map(lambda x: (x, 1)).reduceByKey(lambda a, b: a + b)
    # wordcount.pprint()

    # Start Execution of Streams
    ssc.start()
    ssc.awaitTermination()