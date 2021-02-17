# burrow

## 소개
 - 카프카나 주키퍼에 오프셋을 커밋하는 consumer lag monitoring tool
 - 컨슈머 그룹이 사용하는 모든 토픽과 파티션을 모니터링 이를 통해 컨슈머의 상태를 파악 가능
 - 여러 HTTP 엔드포인트를 제공,이 엔드포인트를 통해 카프카 클러스터나 컨슈머의 정보 수신

## 특징
 - NO THRESHOLDS! : Groups are evaluated over a sliding window.
 - 여러 카프카 클러스터 지원
 - 커밋된 오프셋을 사용하여 모든 Consumer를 자동으로 모니터링 
 - Zookeeper 커밋 오프셋 지원
 - Storm 커밋 오프셋 지원
 - Consumer 그룹 상태 및 브로커 정보 제공을 위한 HTTP 엔드포인트 제공
 - 경고 이메일 전송 기능 지원
 - 다른 시스템에 경고를 보내가 위한 HTTP 클라이언트 지원

## 설치 & 실행
 - go 다운로드 (https://golang.org/doc/install)
 - burrow clone (https://github.com/linkedin/Burrow)
 - 가이드대로 따라하면 됨 포인트는 환경변수 설정과 burrow.toml의 위치를 예제대로 할 것
 - ```
   실행
   cd {go 설치(압축해제)한 경로}
   platformdev@10:~/go$ bin/Burrow --config-dir ~/Burrow/config/ # --config-dir=clone 후 생긴 burrow.toml이 저장된 directory
   ```

## .toml 파일 설정
(참고) https://gunju-ko.github.io/kafka/2018/06/06/Burrow.html
<br>

```
[general] # pid

[logging] # 로깅 설정
level="info"

[zookeeper] # burrow의 메타데이터 저장
servers=[ "10.250.93.21:2181", "10.250.93.22:2181", "21.250.93.26:2181" ]
root-path="/burrow/test"

[client-profile.test] # 클라이언트 설정
client-id="burrow-test"
kafka-version="2.0.0"

[cluster.test] # 카프카 클러스터 설정
class-name="kafka"
servers=["10.250.93.4:9092", "10.250.93.16:9092", "10.250.93.19:9092"]
client-profile="test"
topic-refresh=120
offset-refresh=30

[consumer.test] # 컨슈머 설정
class-name="kafka"
cluster="test"
servers=["10.250.93.4:9092", "10.250.93.16:9092", "10.250.93.19:9092"]
client-profile="test"
group-denylist="^(console-consumer-|python-kafka-consumer-|quick-).*$"
group-allowlist=""

[httpserver.test] # burrow api port
address=":8000"

[storage.test]
class-name="inmemory"
workers=20
intervals=15
expire-group=604800
min-distance=1
```

## endpoint

- Healthcheck
```
Method : GET
URL Format : /burrow/admin
설명 : burrow의 healthcheck
```

- List Clustsers
```
Method : GET
URL Format : /v3/kafka
설명 : kafka broker list
```

- Kafka Cluster Detail
```
Method : GET
URL Format : /v3/kafka/(cluster)
설명 : kafka broker들의 정보를 가져온다.
```

- List Consumers
```
Method : GET
URL Format : /v3/kafka/(cluster)/consumer
설명 : 해당 kafka broker에 존재하는 consumer group 리스트를 가져온다.
```

- List Cluster Topics
```
Method : GET
URL Format : /v3/kafka/(cluster)topic
설명 : 해당 kafka broker에 존재하는 topic 리스트를 가져온다.
```

- Get Consumer Detail
```
Method : GET
URL Format : /v3/kafka/(cluster)/consumer/(group)
설명 : 해당 kafka broker의 consumer group에 대한 lag, offset 정보를 가져온다.
```

- Consumer Group Status
```
Method : GET
URL Format : /v3/kafka/(cluster)/consumer/(group)/status
설명 : 해당 consumer group의 partition정보, status, total lag정보 조회. 
```
> Status의 종류
<br>* NOTFOUND - Consumer group이 cluster에 존재하지 않는 경우
<br>* OK - Consumer group, Partition 정상작동 중
<br>* WARN - offset이 증가하면서 lag도 증가하는 경우(데이터가 증가하는데 consumer가 다소 따라가지 못할 경우)
<br>* ERR - offset이 중지된 경우이지만 lag이 0이 아닌 경우
<br>* STOP - offset commit이 일정시간 이상 중지된 경우
<br>* STALL - offset이 commit되고 있지만 lag이 0이 아닌경우
<br> (참고) Status를 결정하는 로직 : https://blog.voidmainvoid.net/244

- Consumer Group Lag
```
Method : GET
URL Format : /v3/kafka/(cluster)/consumer/(group)/lag
설명 : 해당 consumer group의 partition정보, status, total lag정보 조회
```

- Remove Consumer Group
```
Method : DELETE
URL Format : /v3/kafka/(cluster)/consumer/(group)
설명 : consumer group제거 
```

- Get Topic Detail
```
Method : GET
URL Format : /v3/kafka/(cluster)/topic/(topic)
설명 : topic의 현재 offset 조회
```