### 가상환경 활성화
```bash
source /home/pi/.virtualenvs/elcsoft/bin/activate

# 가상환경 비활성화
deactivate

# (elcsoft) pi@raspberrypi:~ $
```

### kiosk 서버에서 버젼 txt 파일생성
```bash
pip freeze > requirements1.txt
```

### package 설치 requirement.txt kiosk에 설치된거
```bash
pip install requests

pip install pillow

cd ~/www/python/
pip install -r requirements.txt


# 캐시삭제
pip cache purge
```

### 설치 안되는 패키지
```bash
cupshelpers==1.0

lazy-object-proxy==0.0.0

lxml==4.6.3

mypy==0.812

pygame-1.9.6

PyQt5==5.15.2
PyQt5-sip==12.8.1

pysmbc==1.0.23

python-apt==2.2.1

python-prctl==1.7

virtualenv==20.4.0+ds
virtualenv-clone==0.3.0
virtualenvwrapper==4.8.4

pgzero==1.2

picamera2==0.3.12

jedi==0.18.0 -> jedi

mypy==0.812
(mypy-extensions==0.4.3)생략

```


### pygame 설치하려면

```bash
sudo apt update
sudo apt install libsdl1.2-dev

```

