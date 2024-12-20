### 가상환경 활성화
```bash
source /home/pi/.virtualenvs/elcsoft/bin/activate

# 가상환경 비활성화
deactivate

# (elcsoft) pi@raspberrypi:~ $
```

### package 설치 requirement.txt kiosk에 설치된거
```bash
pip install requests

pip install pillow

cd ~/www/python/
pip install -r requirements.txt


# 캐시삭제
pip cache purge
# 삭제
face-recognition-models==0.3.0
google-api-python-client==2.114.0
dlib==19.24.2
cryptography==41.0.7
grpcio==1.60.0
numpy==1.26.4
dbus-fast==2.21.1
```

### numpy kiosk 에 설치된 버젼
```bash
pip install numpy==1.19.5
```

### kiosk 서버에서 버젼 txt 파일생성
```bash
pip freeze > requirements1.txt

arandr를 수동으로 설치

sudo apt-get install arandr

```

#### 이거 대로 라즈베리에 설치
```bash
삭제한 패키지
arandr==0.1.10
```








