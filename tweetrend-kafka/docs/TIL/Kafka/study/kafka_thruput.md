
>__log.retention.hours=72__ (데이터를 실시간으로 가져가기 때문에 저장기간을 주말 장애 등을 고려해 3일)<br>
>> EX. 1KB(메시지 사이즈) * 10,000(초당 메시지 수) * 60(1분) * 60(1시간) * 24(1일) * 7(일) * 3(replica=3) * 10(# of topics)<br>
> [__168TB__]
>
>__delete.topic.enable=true__ (기본적으로 topic 삭제 시, 삭제표시만 남겨둠. 실제로 삭제하기 위해 허용)<br>
>__allow.auto.create.topics=false__ (관리자가 인지하지 못하는 topic의 생성을 방지)<br>
>__log.dirs=/data__ (topic들의 메세지가 저장되는 경로. OS 영역 등에 저장되어 용량 문제가 발생할 수 있으므로 별도의 경로로 변경)

LAG : 현재 토픽의 저장된 메시지와 컨슈머가 가져간 메시지의 차이. 값이 크면 해당 토픽 또는 컨슈머가 읽어가지 못한 메시지가 많은 것


## 측정
> 25 ~ 200 KB / sec
```
1시간 -> 10만건
(3600초) -> "
(30초) -> 833.33 건
==> 27 tweets / sec
==> 1~6 KB / tweet
```


(코로나)
1. 4~6 tweets/5sec
2. 10~20 tweets/1min (a tweet per 3sec)

(코로나 OR covid)
1. 30초 -> 630건 -> 2.04MB (2,142,002 바이트)
  20 tweets / sec

(코로나 OR 코로나19 OR 코로나바이러스 OR covid OR covid19 OR coronavirus)
1. 3600tweets/3min (20tweets/sec)

