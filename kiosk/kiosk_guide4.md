### tornado.service 실행

```bash

cd /lib/systemd/system

sudo systemctl start tornado.service

sudo systemctl status tornado.service 


# tornado.service / restart 부분은 guide1 이랑 변경함
[Unit]
Description=TornadoWebserver

[Service]
ExecStart=/home/pi/www/shell/tornado.sh
Restart=on-failure
User=pi
Group=pi

[Install]
WantedBy=multi-user.target

```

### tornado.sh 실행

```bash

cd shell

# tornado.sh
/home/pi/.virtualenvs/elcsoft/bin/python /home/pi/www/python/webserver.py

```

### 서버 실행 동작 테스트
```bash
# 기본 데스크톱 환경 확인

sudo systemctl get-default

- 출력이 multi-user.target이라면, GUI 모드가 아니라 텍스트 모드로 부팅하도록 설정되어 있습니다.


# GUI 모드로 변경

sudo systemctl set-default graphical.target

sudo reboot


# LXDE 관련 패키지가 설치되어 있는지 확인하려면 다음 명령어를 사용

dpkg -l | grep lxde


# LXDE 환경을 완전히 설치하려면 lxde-common 패키지를 다시 설치해야 합니다. 다음 명령어로 패키지를 재설치

sudo apt-get install lxde-common


# 만약 LXDE의 다른 필수 구성 요소들이 누락된 상태일 수 있으므로, LXDE 전체 환경을 설치하려면 다음 명령어를 사용하세요

sudo apt-get install lxde

sudo reboot

```






