## Zookeeper Error

> WARN org.apache.zookeeper.server.quorum.QuorumCnxManager: Cannot open channel to 2 at election address xxxx/xx.xx.xx.xx:3888
 - zookeeper 를 클러스터로 구성 했을 경우, zookeeper 가 시작되면 Leader 와 Follower 를 결정해야 하는데 시작 직후 다른 port 들이 연결되지 않아 재시도를 반복하는 것
 - 다른 node를 모두 실행시켜주면 사라짐


--------------------------------------
## Kafka Error

> Replication factor: 1 larger than available brokers: 0.
 - kafka 실행 시 --zookeeper 의 인자와 server.properties 내의 zookeeper.connect 가 다를 경우
 - 보통 zookeeper 의 루트 노드가 아닌 하위노드를 지정했을 경우, 이것이 일치시켜줘야 함

> kafka.common.InconsistentClusterIdException: The Cluster ID doesn't match stored clusterId Some in meta.properties. 
> The broker is trying to join the wrong cluster. Configured zookeeper.connect may be wrong.
 - server.properties 내의 log.dirs 에 저장된 meta.properties 을 지워주고 재실행하면 해결
 
> Caused by: java.net.BindException: Address already in use
 - 정상종료 안되었을 때 사용하던 포트를 해제하지 않는 경우
 - 아래와 같이 포트 사용 확인 후 해당 포트 해제(Port_Number 는 보통 9092 또는 2181)
``` 
$ sudo netstat -nltp|grep {port_number}
$ sudo fuser -k Port_Number/tcp
```