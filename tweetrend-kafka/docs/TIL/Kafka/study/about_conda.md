#1. git bash에서 anaconda activate 사용
```
source ~/anaconda3/etc/profile.d/conda.sh
conda activate my_env
```

#2. anaconda 개발환경 추출
```
conda list --export > requirements.txt      # pip freeze > requirements.txt
conda create --name <envname> --file requirements.txt       # 해당 패키지가 설치된 가상환경 생성
```
- pip 와 conda 끼리의 호환은 안되는 듯함

#3. anaconda (vs pip)
- 요약
  + pip : 패키지 관리 도구로, 모듈 설치/모듈간 디펜던시 관리에 사용 
  + conda
    * 가상 환경 제공하는 도구(virtualenv와 유사) 가상 환경 내에서 pip를 사용해 패키지 설치
    * 물론 conda 도 anaconda.org에서 관리하는 패키지들을 설치가능
    * 설치할 수 있는 패키지가 anaconda.org에서 관리하는 패키지로 한정(없으면 pip로 받아 옴)
    * virtualenv + pip 의 느낌

1. Conda
    1) 사람들마다 쓰는게 다른데(윈도우, 맥, 리눅스) 모두 실행 가능한 관리 시스템 만들기
    2) 패키지 환경 관리 시스템(오픈소스)
    3) 장점 : 어떤 OS에서든 패키지 및 종속을 빠르게 설치

2. Conda vs pip
    1) 공통점 : 패키지의 관리자
    2) pip는 python에 한정된 패키지 관리자 (버전별 pip2, pip3라는 명령어도 존재 but 설치 장소 다름)
    3) conda는 다른 언어 c, java 등 포함한 패키지 관리자. 가상 환경 생성 포함

3. 가상환경
    1) 여러 버전의 환경 만들어서 호환성 문제 없도록 만든 환경
    2) virtualenv : python2 버전때부터 쓰인 가상환경 라이브러리
    3) venv : python 3.3 버전 이후부터 기본모듈에 포함됨
    4) conda : Anaconda = pip + venv + 과학 <- 통합된 느낌으로 쓰임
        (윈도우 미지원 pyenv : Python Version Manager + 가상환경 기능 플러그인)

4. 주의
    1) Intel Distribution for Python이라는 것이 conda에 포함됨
    2) 인텔에서 파이썬을 위해 개발한 연산속도 향상 패키지
    3) 모든 파이썬이 아니라 특정 데이터사이언스를 위한 패키지
    4) numpy, scipy, ML 등을 다룰 때 연산속도를 향상시켜주는 패키지인데 이 안에 mkl_fft(주파수 특성 분석) 등 활용됨
    5) conda install numpy는 디폴트로 intel-numpy를 설치
    6) intel 패키지는 mkl_fft을 이용하여 연산속도를 향상
    7) mkl_fft = 1.0.10가 intel-numpy의 dependency가 설치
    8) 이걸 pip install -r requirements.txt를 하게 되면 PyPI에서 mkl_fft를 찾게 되고, 최신버전 mkl_fft = 1.0.6버전(설치 에러 발생)
    9) 즉, 자동으로 설치하기 위해 PyPI의 버전에 맞추어야 함

5. PyPI - Python Package Index
    1) distribution system 배포 시스템
    2) 2000년대 후반에 파이썬 표준 라이브러리로 추가됨
    3) 파이썬 중추 개발팀과 협력하여 인증된 패키지를 관리
    
#4. PackagesNotFoundError
PackagesNotFoundError: The following packages are not available from current channels:

conda install에서 가장 흔히 발생하는 오류 중 하나로 
conda에서 패키지를 다운로드하려는 기본 채널에 패키지가 존재하지 않는 경우 발생하는데 다음과 같이 해결 가능
```
conda install -c conda-forge 패키지명
```
- -c 채널 옵션에 conda-forge를 주어서 패키지를 다운로드한다.
- Conda-forge 는 anaconda에서 쉽게 설치할 수 있도록 검증된 파이썬 패키지들을 모아 놓은 하나의 채널
