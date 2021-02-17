##0. 설치
```
openjdk 8 설치
sudo apt-get install openjdk-8-jdk
sudo wget https://downloads.apache.org/kafka/2.7.0/kafka_2.13-2.7.0.tgz
sudo tar -xvzf kafka_2.13-2.7.0.tgz
```
```
이후에 openjdk 11로 교체해야할 때
$ sudo apt-get remove openjdk*
$ sudo apt-get remove oracle*
$ sudo add-apt-repository ppa:openjdk-r/ppa
$ sudo apt install openjdk-11-jdk
```

##1. 주키퍼설정
- zookeeper.properties 편집
```
$ sudo vim config/zookeeper.properties

이후 아래의 설정으로 편집
# the directory where the snapshot is stored.
dataDir=/tmp/zookeeper
# the port at which the clients will connect 
clientPort=2181

# disable the per-ip limit on the number of connections 
# since this is a non-production config
maxClientCnxns=0

initLimit=5 # 처음 follower가 leader와 연결 시도시 가지는 tick 제한 횟수(10초)
syncLimit=2 # follwer와 leader가 sync된 후, 동기화를 유지하기 위한 tick 제한 횟수(4초)
# tickTime=2000 # 위 설정들에 대한 단위 tick시간 default=2000(2초)

server.1={hostname1}:2888:3888 # 2888은 leader node가 follower node를 위해 열어두는 포트(동기화용)
server.2={hostname2}:2888:3888 # 3888은 leader node 선출을 위한 election 용 포트.
server.3={hostname3}:2888:3888
```


- 각 서버마다 server.x 의 x에 해당되는 id 값을 파일로 기록(zookeeper 서버 끼리의 연동)
```
서버1
$ echo 1 > /tmp/zookeeper/myid
서버2
$ echo 2 > /tmp/zookeeper/myid
서버3
$ echo 3 > /tmp/zookeeper/myid
```

##2. 카프카설정
```
$ sudo vim config/server.properties

이후 아래의 설정으로 편집
# The id of the broker. This must be set to a unique integer for each broker.
broker.id=0
listeners=PLAINTEXT://:9092
advertised.listeners=PLAINTEXT:/ls/test-broker01:9092
zookeeper.connect=test-broker01:2181,test-broker02:2181,test-broker03/test
```


##3. 실행
sudo bin/zookeeper-server-start.sh ./config/zookeeper.properties

sudo bin/kafka-server-start.sh config/server.properties

sudo bin/kafka-topics.sh --create --zookeeper zk1:2181/brk1 --replication-factor 3 --partitions 10 --topic test

sudo bin/kafka-topics.sh --create --zookeeper test-broker01:2181,test-broker02:2181,test-broker03:2181/test --replication-factor 3 --partitions 9 --topic test2
sudo bin/kafka-topics.sh --delete --zookeeper zk1:2181,was02:2181,was03:2181 --topic test2

sudo bin/kafka-topics.sh --list --zookeeper zk1:2181/node
sudo bin/kafka-topics.sh --describe --zookeeper zk1:2181/brk1 --topic test

sudo bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test2

sudo bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test2 --from-beginning







