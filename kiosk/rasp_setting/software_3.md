#### 압축

tar -czvf kiosk.tar.gz Bookshelf Downloads Public Videos css image json nohup.out reversessh.log.save screen.sh temp.txt 
www Music README.md Workspace font index.html log python reversesshservice.sh shell test Documents Pictures Templates click html
js logview.sh reversessh.log rsync.sh sound test.html


#### sftp 명령어로 압축파일 전송
```bash
sftp pi@192.168.0.161

get /home/pi/kiosk.tar.gz /home/pi

# 현재 경로에 압축해제
tar -xzvf kiosk.tar.gz -C /home/pi


```

#### 가상환경 설치

```bash

pip show virtualenv

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

pip install opencv-python   # 오래걸림

pip install face-recognition   # 가상공간 따로 할당해서 설치하는법 검색

```


#### tornado 설치

```bash

pip install Pillow

pip install tornado

```

#### /home/pi/shell/tornado.sh

```bash

# elcsoft 가상 환경의 Python 인터프리터로 webserver.py 모듈 실행
/home/pi/.virtualenvs/elcsoft/bin/python /home/pi/www/python/webserver.py

```

#### tornado.service 

- tornado.sh 를 tornado.service 파일에 넣어서 autostart 할 때 사용
  

#### sudo nano /lib/systemd/system/tornado.service

```bash
[Unit]
Description=TornadoWebserver

[Service]
ExecStart=/home/pi/www/shell/tornado.sh
Restart=on-abort
User=pi
Group=pi
Restart=on-failure

[Install]
WantedBy=multi-user.target
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



















