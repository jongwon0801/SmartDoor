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

source /home/pi/.local/bin/virtualenvwrapper.sh (kiosk 서버와 sh 파일 위치가 다름)

-> login 하면 workon 명령어 사용 가능

sudo reboot

```

#### 가상환경 폴더 생성

```bash
mkvirtualenv elcsoft

/home/pi/.virtualenvs/elcsoft 위치에 가상환경 폴더 생성됨

```

#### tornado 설치

```bash

pip install tornado

```

#### tornado.service 

- tornado.sh 를 tornado.service 파일에 넣어서 autostart 할 때 사용
  
```bash

sudo nano /lib/systemd/system/tornado.service

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

sudo systemctl daemon-reload
sudo systemctl enable tornado.service
sudo systemctl start tornado.service
sudo systemctl status tornado.service

```

#### /home/pi/shell/tornado.sh

```bash

# elcsoft 가상 환경의 Python 인터프리터로 webserver.py 모듈 실행
/home/pi/.virtualenvs/elcsoft/bin/python /home/pi/www/python/webserver.py

```





