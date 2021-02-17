## 신뢰도에 따른 스트림 처리 방식
- At-most-once: 데이터 유실이 있을 수 있어, 추천하지 않는 방식
- At-least-once: 데이터 유실은 없으나 재전송으로 인해 중복이 생길 수 있음. 대부분의 경우 충분한 방식
- Exactly-once: 데이터가 오직 한 번만 처리되어 유실도 중복도 없음. 모든 상황에 대해 완벽히 보장하기 어렵지만 이상적인 방식

## Kafka - SparkStreaming 연동
1. Receiver-based approach
    - `Receiver` 사용하여 kafka 로부터 전달받음 
    - 처음 `Receiver`를 시작할 때 만들어진 Kafka 연결을 계속 사용하여, 매 배치마다 연결 지연 없음
    - 유실방지를 위해 WAL(Write Ahead Logs) 사용하여 받은 데이터를 저장하면서 처리
    - Kafka 의 offset 을 Zookeeper 에 갱신하기 전 시스템이 실패하면 spark streaming 은 데이터를 받았다고, Kafka 는 데이터를 전달하지 않았다고 인식
    - 시스템이 복구 될 때 spark streaming 은 WAL 에 저장된 데이터로 복구 처리를 하고 `Receiver` 를 동작
    - 다시 `Rceiver` 가 kafka 로부터 다음 데이터를 받아오려하면 offset 갱신을 하지 않은 kafka 는 이전 데이터를 다시 보내게 됨
    - 복구 처리 두번 발생 `At-least-once`
2. Direct stream approach (kafka 에서만 사용 가능)
    - `Receiver` 사용하지 않음
        - 매 배치마다 새로 할당받은 `executor` 에서 kafka 에 연결해 데이터를 가져와 연결 지연이 발생하지만 `Exactly-once` 보장
        - kafka 의 각 파티션은 하나의 `executor` 에서 직접 받아오고, 하나의 RDD 파티션이 생성 됨
        - 즉 kafka 의 파티션 수만큼 병렬화하여 데이터를 가져옴 (kafka 파티션 수로 병렬 수준을 제어)
    - __Zookeeper 에 offset 정보를 갱신하지 않는다. offset 정보를 직접 Handling 필요__
        - 이와 관련하여 offset 을 관리하는 두가지 방법이 있음
        - kafka 에서 offset 을 읽어와 Hbase, HDFS, Kafka, Zookeeper 등에 저장하는 방식
        - Spark 의 checkpoint 에 저장하는 방식
            - spark streaming 이 알아서 저장했음에도 불구하고 offset 을 checkpoint 에 저장하지 못하고 장애가 발생할 우려
            - checkpoint 의 데이터를 읽을 수 없다면 재시작 시 마지막 처리 이후로 작업을 할 수 없음
            - 코드변경에 취약하여 다른 코드로 재실행시 역직렬화 문제 우려
3. Structured streaming
   - apache spark 2.0 이상에서 새로 도입
   - spark SQL 엔진 위에 구축된 확장 가능하한 내결함성 스트림처리 엔진
   - Dstream 및 spark API 와 관련된 이슈가 아닌 스트림 처리와 계산이 배치처리와 유사
   - 구조화된 streaming 엔진은 정확히 한 번 stream 처리, 처리 결과에 대한 증분 업데이트, 집계 등과 같은 내용을 처리
   - __들어오는 데이터를 마이크로 배치 처리하고 수신 시간을 데이터 분할의 수단으로 사용하므로 실제 이벤트 시간을 고려하지 않는 이슈를 해결__<br>
     (수신되는 데이터에서 이런 이벤트 시간을 지정하여 최신 데이터가 자동으로 처리되도록 할 수 있음)
  - 실시간 data stream 을 처리할 때 연속적으로 추가 되는 무제한 테이블로 처리하여 계산과 SQL 쿼리를 통해 결과 테이블을 생성