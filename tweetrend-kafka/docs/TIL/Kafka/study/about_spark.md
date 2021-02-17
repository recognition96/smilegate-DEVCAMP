## 1. 비교
> vs Hadoop
- 구글의 Mapreduce와 GFS 개념을 보완한 빅데이터용 오픈소스인 Hadoop의 핵심기술은 Mapreducer와 HDFS
- 하지만 하드디스크에서 파일을 처리하여 처리속도가 느림(클러스터로부터 데이터를 읽고 연산을 수행하며 클러스터에 다시 결과를 작성하여 시간이 소요)
- Spark는 메모리기반(In-memory)의 데이터 처리 방법과 Task 정리방법을 개선하여 RDD를 이용한 데이터셋을 적용한 것(최대 100배 더 빠름)

> vs Kafka

- Kafka is a Message broker. Spark is the open-source platform.
- Kafka has Producer, Consumer, Topic to work with data. Where Spark provides platform pull the data, hold it, process and push from source to target.
- Kafka provides real-time streaming, window process. Where Spark allows for both real-time stream and batch process.
- In Kafka, we cannot perform a transformation. Where In Spark we perform ETL
- Kafka does not support any programming language to transform the data. Where spark supports multiple programming languages and libraries.
- So Kafka is used for real-time streaming as Channel or mediator between source and target. Where Spark uses for a real-time stream, batch process and ETL also.

- We can use Kafka as a message broker. It can persist the data for a particular period of time. 
Using Kafka we can perform real-time window operations. But we can’t perform ETL transformation in Kafka. 
Using Spark we can persist data in the data object and perform end-to-end ETL transformations.

So it’s the best solution if we use Kafka as a real-time streaming platform for Spark.


## 2. RDD
 - 디스크에서 읽어온 뒤 연산 이후 데이터를 휘발성인 '메모리'에 저장하기 위해 추상화 작업이 필요 -> RDD
 - Spark에서 사용하는 기본 추상 개념으로, 클러스터의 머신(노드)의 여러메모리에 분산하여 저장할 수 있는 데이터의 집합
 - 메모리에 저장된 데이터가 유실되면 Spark는 메모리의 데이터를 읽기전용으로 만들고, 
   데이터를 만드는 방법을 기록하여 데이터가 유실되면 다시 만듬
 - RDD는 Immutable 하기 때문에 연산수행에 있어 기존방식과는 다르게 수행. 크게 Transformations와 Actions 2가지
 - Transformations 는 RDD에게 변형방법(연산로직, 계보) 를 알려주고 새로운 RDD를 만들지만
 - 실제 연산의 수행은 Actions를 통해 이루어짐 -> 결과값을 보여주고 저장하는 역할 + Transformations 에게 연산 지시
 - 즉 실제 RDD가 생성되는 시점은 Actions에서 이루어짐

## 3. Dstream(이산 스트림)
 - Spark Streaming 의 추상화 개념으로, 시간별로 도착한 데이터(RDD)들의 연속적인 모음
 - Kafka, Flume, HDFS 등 다양한 입력 원천으로부터 만들어 질 수 있다.
 - 두가지 타입의 연산 제공: 새로운 DStream을 만들어 낼 수 있는 transformation 와 외부 시스템에 데이터를 써주는 결과연산(output operation)
 - RDD에서 가능한 것과 동일한 종류의 연산을 지원
 - 구현
   1) StreamingContext 에서 생성되며 이는 곧 하부 계층에 존재하는 SparkContext도 생성(데이터 처리에 사용)
   2) Sparkstreaming이 데이터를 받기 시작하려면 StreamingContext 의 start()를 호출해야 함
   3) 그러면 Sparkstreaming은 스파크 작업들을 스케줄링하기 시작
   4) 이는 별도의 스레드에서 실행되므로 사용자 app이 종료되어도 작업을 유지하기 위해 
       streaming 연산이 완료되기를 기다리도록 awaitTermination을 호출할 필요가 있음
   5) StreamingContext는 한 번만 시작할 수 있으므로  DStream과 출력 연산에 대한 모든 것을 작업 후 시작해야 함


