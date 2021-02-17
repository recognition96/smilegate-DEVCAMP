
# Twitter API v2 Guide

## 1. Building query
### 1) stream 데이터를 요청하기 전, Rules 를 Add 해줘야 함
```
   (1) restful : POST tweets/search/stream/rules
   (2) 위의 주소로 요청을 보냄으로써 Add
   (3) filltered stream endpoints 에서는 최대 25개의 queries(=rules, filter), 512자 이하를 허용
```
### 2) Operator syntax
```
   (1) AND(모두 포함하고 싶을 때) : 키워드들을 ' ' 로 연결 
     - ex. snow day #NoSchool
     - snow, day와 해시태그로 NoSchool을 포함하는 Tweets
   (2) OR : 키워드들을 'OR' 로 연결
     - ex. snow OR day OR #NoSchool
     - snow, day, 해시태그로 NoSchool 중 하나라도 포함하는 Tweets
   (3) Negate: 키워드 앞에 '-' 를 붙이면 해당 키워드는 제외
     - ex. snow -day #NoSchool
     - snow, 해시태그로 NoSchool를 포함하고, day는 포함되지 않은 Tweets
     - 키워드 뿐만 아니라 -is:retweet 처럼 Rtweets은 제외할 수 있음 (original Tweets만)
     - 'sample'을 제외한 모든 연산에 적용 가능
   (4) Group operator: 연산들을 괄호로 묶어서 처리할 수 있음
     - negate시, 괄호에 넣어서 하지말 것
     - '-(snow OR day OR noschool)' 대신 '-snow -day -noschool' 로 사용하기를 권장
```
### 3) Standalone operators
```
   (1) keyword, emoji 은 tweet body 내의 text를 tokenize하여 비교
     - punctuation, symbols, and Unicode basic plane separator characters 를 기준으로 tokenize
     - ex. coca-cola 와 같이 delimeter가 포함된 키워드로 match 하고 싶으면 "coca-cola"와 같이 사용(본문에 정확히 일치)
   (2) 해시태그(#)
     - 해시태그는 Tweet의 해시태그와 정확히 일치하는 것(tokenize되지 않은)
     - \#thanku 는 정확히 해당 형태와 일치. (#thankunext 는 match되지않음)
   (3) from: / to: / retweets_of:
     - 특정 username 또는 user's numeric user ID 를 대상으로 하는 수신/발신/리트윗 Tweet과 match
     - 언급(mention)인 @ 표시는 제외  ->  @로 필터링할 때는 '@' 문자까지 포함해서 match 시킴
   (4) url:
     - Tweet 내의 validly-formatted URL 와 tokenize하여 match. 이때 URL 에 punctuation등이 포함되므로 " "로 감싸준다
     - 단 Tweet 본문 에서는 URL을 shortening 하여 보여주기 때문에(글 작성했을 때와 다름) 
       실제 URL(entities.urls.expanded_url) 이나 short URL(entities.urls.url) 둘 중 하나만 해도 match 됨
   (5) conversation_id:
     - conversation 을 시작한 Tweet의 Tweet Id 
     - conversation이 정확히 뭔지 모르겠는데 특정 Tweet에 대해 Reply를 주고 받은 내역을 의미하는 듯
```
### 4) Non-standalone operators : standalon operator 없이는 사용 불가
```
   (1) is:retweet
     - Retweets 글만 match(Quote Tweets은 match 되지 않음)
   (2) is:reply
     - 답장하는 글만 match(replies to an original Tweet, replies in quoted Tweets and replies in Retweets)
     - negate를 적용하여 답장하는 글만 제외시킬 수도 있음
   (3) is:quote
     - 인용하는 글(원본 Tweets과 이에 대한 comment를 포함하는 Tweets)만 match
   (4) has:hashtag (:links, :mentions, :media, :images, :videos)
     - 본문에 해당하는 컨텐츠가 포함된 Tweets 과 match
   (5) sample:
     - 나머지 rule에 해당하는 전체 Tweets 중 (1~100) percent 의 양 만큼을 랜덤하게 match -> filtering
     - 모든 rule에 적용되기 때문에 OR 로 묶인 rule들은 grouped 시켜야 함
   (6) lang:
     - 특정 언어로 분류된 Tweets과 match (분류는 Twitter에서 함)
     - 하나의 Tweets은 하나의 언어로만 분류되므로 lang rule을 여러 개(AND)로 적용하면 응답이 없다
     - 총 47개의 lang으로 분류하고, 분류될 수 없는 Tweets 은 'und'로 분류(표시)됨 (undefined)
```

## 2. Filtered stream
 1) 스트림 등록/삭제
```
  (1) POST /2/tweets/search/stream/rules
  (2) Tweets stream를 원하는 주제와 형태로 받기 위해선 rule을 등록(추가)해야 함
  (3) 한 번 등록한 rule은 직접 삭제하기 전까지 유지(계정에 귀속되는 지, 코드 실행할 때마다 재등록해줄 필요 없음)
  (4) 각 rule들은 id로 구별됨  
```
 2) 스트림 정보 조회
```
  (1) GET /2/tweets/search/stream/rules
  (2) 현재 스트림에 등록되어 있는 rule들을 조회. 삭제해주기 전까진 유지
  (3) rule ID들을 Comma-separated list의 형태로 입력할 수 있지만, 따로 없다면 모든 rule을 조회
```
 3) 실시간 Tweets 스트림 조회
```
  (1) GET /2/tweets/search/stream
  (2) rule에 따라 filtered stream 의 데이터를 받음
  (3) 한 달에 500,000 건을 받을 수 있고, 초과하면 1달 기준일(가입날)까지 기다려야 함
  (4) 요청 body에 아래와 같은 fields와 그에 속하는 정보들(Comma-separated list)을 key-value로 넣어 받을 수 있음
     (expansions, media.fields, place.fields, poll.fields, tweet.fields, user.fields)
```
 4) 이용량 제한(15분당)
   - Connecting : 50회
   - Adding/deleting filters : 450회
   - Listing filters : 450회


