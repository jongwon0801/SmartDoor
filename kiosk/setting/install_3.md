#### 압축
```bash
tar -czvf kiosk.tar.gz Bookshelf Downloads Public Videos css image json nohup.out reversessh.log.save screen.sh temp.txt 
www Music README.md Workspace font index.html log python reversesshservice.sh shell test Documents Pictures Templates click html
js logview.sh reversessh.log rsync.sh sound test.html

# www 폴더만 압축
tar -czvf kiosk.tar.gz www

-c (create): 아카이브 생성 - 새로운 tar 파일을 생성
-z (gzip): gzip으로 압축 - .gz 형식으로 압축
-v (verbose): 진행 상황 표시 - 처리 중인 파일 목록을 출력
-f (file): 파일 이름 지정 - 대상 아카이브 파일 이름을 지정

```

#### sftp 명령어로 압축파일 전송
```bash
sftp pi@192.168.0.161

get /home/pi/kiosk.tar.gz /home/pi

# 현재 경로에 압축해제
tar -xzvf kiosk.tar.gz -C /home/pi

-x (extract): 압축을 풀기 위해 사용
-z (gzip): .gz 형식의 gzip 압축을 해제
-v (verbose): 압축을 푸는 과정을 화면에 출력 (파일 목록이 보임)
-f (file): 대상이 되는 파일 이름을 지정


```

#### 가상환경 설치

```bash

pip install virtualenv

-> Location: /home/pi/.local/lib/python3.9/site-packages


pip install virtualenvwrapper

-> Location: /home/pi/.local/lib/python3.9/site-packages


sudo nano ~/.profile 하단에 입력

source /home/pi/.local/bin/virtualenvwrapper.sh (161 서버와 sh 파일 위치가 다름)

-> login 하면 workon 명령어 사용 가능

sudo reboot

```

#### 가상환경 폴더 생성

```bash
mkvirtualenv elcsoft

/home/pi/.virtualenvs/elcsoft 위치에 가상환경 폴더 생성됨

# 가상환경 켜고 패키지 설치하면 이 경로에 파이썬 패키지들이 설치됨
/home/pi/.virtualenvs/elcsoft/lib/python3.9/site-packages

일반적으로 --user로 설치한 패키지는 ~/.local/lib/pythonX.X/site-packages에 저장됨

```

#### 의존성 패키지 제외하고 설치

```bash
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

#### webserver.py 실행하면서 설치

```bash
pip install firebase-admin

pip install Pillow

pip install qrcode

pip install pyzbar

pip install PyMySQL

pip install DBUtils

pip install websockets

pip install gTTS

pip install pydub

pip install nmcli

pip install RPi.GPIO

pip install gpiozero

pip install python-vlc

pip install lgpio

pip install opencv-python   

pip install face-recognition   # 가상공간 따로 할당해서 설치하는법 검색

pip install dlib

```

#### face_recognition 설치

- face_recognition은 dlib 라이브러리를 기반으로 작동하므로, dlib의 빌드에 필요한 패키지들을 먼저 설치해야 합니다

```bash

# 필수 의존성 설치
sudo apt update

sudo apt install -y build-essential cmake libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev libboost-all-dev

sudo apt install -y python3-dev python3-pip


# SWAP 파일 크기 변경
sudo nano /etc/dphys-swapfile

# CONF_SWAPSIZE 값을 2048 (2GB) 또는 4096 (4GB)로 수정
CONF_SWAPSIZE=4096

# SWAP 서비스 재시작
sudo dphys-swapfile setup
sudo dphys-swapfile swapon


pip cache purge

sudo apt update

pip install --upgrade pip

pip install face_recognition

# 해시 무시하고 강제 설치
pip install --no-cache-dir --no-deps face-recognition

# face_recognition 패키지를 사용하기 전에 face_recognition_models 라이브러리를 설치
pip install git+https://github.com/ageitgey/face_recognition_models



```

#### ttyUSB 심볼릭 링크 설정

sudo nano /etc/udev/rules.d/99-com.rules


```bash

# PWM export results in a "change" action on the pwmchip device (not "add" of a new device), so match actions other than "remove".
SUBSYSTEM=="pwm", ACTION!="remove", PROGRAM="/bin/sh -c 'chgrp -R gpio /sys%p && chmod -R g=u /sys%p'"
# 두줄 추가
SUBSYSTEM=="tty", ATTRS{idVendor}=="1d6b", ATTRS{idProduct}=="0002", SYMLINK+="hione"
SUBSYSTEM=="tty", ATTRS{idVendor}=="04d8", ATTRS{idProduct}=="000a", SYMLINK+="ttyUSB_PIR"

Udev 서비스를 재시작 하거나 리부팅
sudo udevadm control --reload-rules

sudo reboot


```

#### tornado 설치

```bash

pip install tornado

```

#### /home/pi/www/shell/tornado.sh

```bash

# elcsoft 가상 환경의 Python 인터프리터로 webserver.py 모듈 실행
/home/pi/.virtualenvs/elcsoft/bin/python /home/pi/www/python/webserver.py

```

#### tornado.service 

- tornado.sh 를 tornado.service 파일에 넣어서 autostart 할 때 사용

---

#### /home/pi/.config/systemd/user/tornado.service

mkdir -p ~/.config/systemd/user

```less
# 유저 단위 서비스 ~/.config/systemd/user/ 에 작성

[Unit]
Description=TornadoWebserver

[Service]
#User=pi
#Group=pi

# X11 환경 변수 설정
Environment=DISPLAY=:0
Environment="XAUTHORITY=/home/pi/.Xauthority"
ExecStart=/home/pi/www/shell/tornado.sh

Restart=on-failure
Restart=on-abort

[Install]
#WantedBy=multi-user.target
WantedBy=default.target

```


```less

systemctl --user daemon-reload

systemctl --user enable tornado.service

systemctl --user start tornado.service

systemctl --user status tornado.service

# 부팅 후 자동실행
sudo loginctl enable-linger pi

```


#### sudo nano /lib/systemd/system/tornado.service

```bash
# 벨누르고 영상통화 후 벨 안되는 서비스

[Unit]
Description=TornadoWebserver

[Service]
ExecStart=/home/pi/www/shell/tornado.sh
Restart=on-abort
User=pi
Group=pi
Restart=on-failure

[Install]
#WantedBy=default.target
WantedBy=multi-user.target


sudo systemctl stop tornado.service

sudo systemctl disable tornado.service

sudo rm /lib/systemd/system/tornado.service

sudo systemctl daemon-reload

sudo nano /etc/systemd/system/tornado.service

sudo systemctl enable tornado.service

sudo systemctl start tornado.service

sudo systemctl status tornado.service
```



#### tornado 재실행

```bash
sudo systemctl daemon-reload

sudo systemctl enable tornado.service

sudo systemctl start tornado.service

sudo systemctl status tornado.service

```

#### chromium 설치


```bash
sudo apt update

sudo apt install chromium-browser -y

chromium-browser


```



#### autostart 설정

sudo nano /etc/xdg/lxsession/LXDE-pi/autostart

```bash

@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash

@chromium-browser --kiosk --autoplay-policy=no-user-gesture-required --check-for-update-interval=31536000 http://127.0.0.1
#@chromium-browser http://127.0.0.1

```

```bash

pkill chromium

cd ~/.config/chromium/

rm -f SingletonLock

rm -f SingletonSocket

sudo reboot

```



















