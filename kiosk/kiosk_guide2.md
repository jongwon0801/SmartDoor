### 가상환경 활성화
```bash
source /home/pi/.virtualenvs/elcsoft/bin/activate

# 가상환경 비활성화
deactivate

# (elcsoft) pi@raspberrypi:~ $
```

### kiosk 서버에서 버젼 txt 파일생성(의존성 패키지는 따로 설치안함)
```bash
pip freeze > requirements1.txt
```


#### 의존성 패키지 제거

```bash
pip-tools를 사용해 의존성을 확인

pip install pip-tools


# requirements.txt에서 다음 줄을 삭제합니다.

arandr==0.1.10

cupshelpers==1.0

lazy-object-proxy==0.0.0

mypy, pygame, Werkzeug==1.0.1


1. SDL 개발 라이브러리 설치
sudo apt-get install libsdl-dev

2. Jedi 경고 해결
pip install --upgrade jedi

3. 잘못된 의존성 (Lazy Object Proxy) 문제 해결

lazy-object-proxy==1.10.0

4. python setup.py egg_info 오류 해결

sudo apt-get install build-essential
sudo apt-get install python3-dev

5. 필수 SDL 라이브러리 설치

sudo apt-get install libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev
sudo apt-get install libsdl2-dev


6. 최신 버전의 pip, setuptools, wheel 설치

pip install --upgrade pip setuptools wheel

sudo apt-get install libsdl1.2-dev libfreetype6-dev libpng-dev libjpeg-dev


requirements.txt를 분석하고 의존성을 자동으로 정리한 optimized-requirements.txt 파일을 생성

pip-compile --output-file=optimized-requirements.txt requirements.txt

```

### 의존성 제거 후 필수 패키지 목록

```bash

Flask==1.1.2
oauthlib==3.1.0
requests==2.25.1
requests-oauthlib==1.0.0
PyJWT==1.7.1
paho-mqtt==2.1.0
numpy==1.19.5
pycryptodome==3.20.0
pyserial==3.5b0
pyOpenSSL==20.0.1
pylint==2.7.2
#pyqt5==5.15.2
#pyqt5 제거하고 진행

```

### tornado 실행
```bash

# 필요 패키지 설치

pip install Pillow

sudo systemctl daemon-reload
sudo systemctl restart tornado.service
sudo systemctl status tornado.service


```





