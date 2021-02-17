# Kafka manager
> Kafka를 CLI 환경에서 운영을 할 수 있지만, 자체적으로 웹 GUI환경을 제공하지 않고 있다. 
 yahoo에서 자체적으로 운영 하던 kafka-manager라는 웹GUI를 오픈소스로 공개 하였으며, 실제로 많은  Kafka운영에서 적용되고 있다.
 주요 기능(CLI환경에서 모두 가능하고, 더 많은 내용을 다룰 수 있긴 함)
> - 여러 개의 클러스터를 등록 및 관리*
> - 클러스터 상태를 쉽게 확인
> - 파티션 추가
> - 파티션 리발란스
> - 토픽 생성 & 삭제 *
> - 토픽 리스트*
> - 토픽 설정 업데이트

## 0. 준비 
- JAVA 11+ 버전 및 $JAVA_HOME 환경변수 세팅
   기존 java파일 삭제
```
$ sudo apt-get remove openjdk*
$ sudo apt-get remove oracle*
$ sudo apt-get autoremove --purge
$ sudo apt-get autoclean
```
- javaj 11에 새로 도입된 클래스들을 빌드할 땐 문제될 수 있어 아래와 같은 방법
```
$ sudo add-apt-repository ppa:openjdk-r/ppa
$ sudo apt install openjdk-11-jdk
$ java -version
```
- sbt(Simple Build Tool, 스칼라를 위한 빌드 툴) 설치 
```
$ echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823
$ sudo apt-get update
$ sudo apt-get install sbt
```

## 1. 원하는 버전의 tar.gz 파일 링크로 부터 다운로드 
버전확인 : https://github.com/yahoo/CMAK/releases 
```
$ wget https://github.com/yahoo/CMAK/archive/3.0.0.5.tar.gz
$ tar -xvzf 3.0.0.5.tar.gz
```

## 2. 압축 해제 후 생성 된 CMAK-3.0.0.5 파일 내의 sbt 실행
```
$ cd CMAK-3.0.0.5
$./sbt clean dist
```

## 3. 실행이 끝난 후 아래와 같은 메세지로 zip파일이 생성된 위치를 알려줌
- 여기서 많은 예제들의 파일이름이 kafka-manager로 되어 있는데 나는 아니어서 애를 좀 먹음
```
 [info] Your package is ready in {zip파일 경로}/cmak-3.0.0.5.zip
```
- 해당 파일을 원하는 경로에 압축 해제 실행 
```
$ unzip -d {원하는 경로} {zip파일 경로}/cmak-3.0.0.5.zip
```

## 4. 원하는 경로에 해제된 파일의 conf 설정 변경
```
$ vim cmak-3.0.0.5/conf/application.conf
```
- 많은 예제들이 `kafka-manager.zkhosts`만 수정하는데, 계속 안되어서 고생하다가 `cmak.zkhosts`도 수정해주니 해결되었음(파일이름 달라서 그런듯)
```
파일이름에 따라 바꿔주면 될 것 같다
kafka-manager.zkhosts="{주키퍼서버1의 ip}:2181,{주키퍼서버2의 ip}:2181,{주키퍼서버3의 ip}:2181"
cmak.zkhosts="{주키퍼서버1의 ip}:2181,{주키퍼서버2의 ip}:2181,{주키퍼서버3의 ip}:2181"
```
## 5. bin/cmak 파일 실행(주키퍼-카프카 실행 먼저)
```
$ sudo cmak-3.0.0.5/bin/cmak -java-home $JAVA_HOME -Dconfig.file=cmak-3.0.0.5/conf/application.conf -Dhttp.port=9000
 -java-home JAVA 경로
 -Dconfig.file 수정한 파일경로
 -Dhttp.port=8080 (기본포트는 9000)
```
- 활용은 링크 참고<br>
https://blog.naver.com/PostView.nhn?blogId=occidere&logNo=221395731049&categoryNo=0&parentCategoryNo=0&viewDate=&currentPage=1&postListTopCurrentPage=1&from=postView







