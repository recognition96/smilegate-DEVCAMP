## default port : 주키퍼(2181, 2888, 3888), 카프카(9092)


## window
0. 카프카 설치 경로로 이동
```
cd C:\kafka\bin\windows
```
1. 주키퍼 실행
```
.\zookeeper-server-start.bat ..\..\config\zookeeper.properties
```
2. 카프카 실행
```
.\kafka-server-start.bat ..\..\config\server.properties
```
3. 실행 확인
```
netstat -a
```
4. 토픽 생성
```
.\kafka-topics.bat --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic (토픽이름)
```
5. 토픽 생성 확인
```
.\kafka-topics.bat --list --bootstrap-server localhost:9092
```
6. producer로 메세지 보내기
```
.\kafka-console-producer.bat --broker-list localhost:9092 --topic (토픽이름)
```
7. consumer로 메세지 받기
```
.\kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic (토픽이름) --from-beginning
```
---

## Linux

1. 주키퍼 실행
```
sudo bin/zookeeper-server-start.sh ./config/zookeeper.properties
```
2. 카프카 실행
```
sudo bin/kafka-server-start.sh config/server.properties
```
3. 토픽
```
- 토픽 생성
sudo bin/kafka-topics.sh --create --zookeeper zk1:2181/brk1 --replication-factor 3 --partitions 10 --topic test
sudo bin/kafka-topics.sh --create --zookeeper test-broker01:2181,test-broker02:2181,test-broker03:2181/test --replication-factor 3 --partitions 9 --topic test2

- 토픽 삭제
sudo bin/kafka-topics.sh --delete --zookeeper zk1:2181,was02:2181,was03:2181 --topic test2

- 토픽 정보
sudo bin/kafka-topics.sh --list --zookeeper zk1:2181/node
sudo bin/kafka-topics.sh --describe --zookeeper zk1:2181/brk1 --topic test
```

4. 프로듀서
```
sudo bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test2
```
5. 컨슈머
```
sudo bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test2 --from-beginning
```
6. 응용
```
# 토픽 생성/조회/수정
kafka-topics.sh
# 토픽으로 레코드 전달
kafka0consol-producer.sh
# 토픽의 레코드 조회
kafka-console-consumer.sh
# 컨슈머그룹 조회/ 컨슈머 오프셋 확인/수정
kafka-consumer-groups.sh
# 카프카 오프셋 리셋
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group test-conumser-group --topic test --reset-offsets
옵션 : --shift-by <LONG>, --to-offset <LONG>, --to-latest, --to-earliest
```




