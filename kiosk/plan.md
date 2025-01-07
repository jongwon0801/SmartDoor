
### 전체 구성

<img width="688" alt="image" src="https://github.com/user-attachments/assets/c2fc57e9-a564-443a-adec-c92d3003b20a" />

- 통신 방식 : 시리얼 통신, 비동기 통신

- 시리얼 통신은 직렬 연결이라는 뜻을 가지고 있으며, 직렬 연결은 한번 에 하나의 비트단위로 1(High)과 0(Low)의 신호로 데이터를 전송하는 통신 방법

- 비동기 통신은 클럭 신호를 사용하지 않기 때문에 통신에 필요한 선의 수가 더 적음, 하지만 통신 속도 측면에서는 동기 통신방식이 효율이 더 좋다
- 비동기 통신을 사용할 때에는 통신에 참여하는 두 주체가 서로 대등한 관계에서 일대일 통신을 한다.

통신 표준 : RS-485

UART(범용 비동기화 송수신기: Universal asynchronous receiver/transmitter)는 병렬 데이터의 형태를 직렬 방식으로 전환하여 데이터를 전송하는 컴퓨터 하드웨어

### 비동기(Asynchronous) 통신

- 비동기 통신은 동기를 맞추기 위한 별도의 클럭 신호 없이 데이터를 주고 받는 방법
- 클럭 신호가 없기 때문에 송신자는 한 바이트의 데이털르 전송하기 직전에 통신의 시작을 알리는 시작 비트를 먼저 보내 데이터의 전송이 시작된다는 것을 수신자에게 알림
- 시작 비트를 보낸 다음부터 데이터를 한 비트씩 보내고 마지막에는 통신의 끝을 알리는 정지 비트를 보내 통신이 끝났음을 알림

### gpio

<img width="688" alt="image" src="https://github.com/user-attachments/assets/f2c9dcce-049a-4b97-87d5-ce77f3682119" />

### 스마트도어 스크린

<img width="335" alt="image" src="https://github.com/user-attachments/assets/9d573b71-5432-465c-b8dd-333470290ee0" />

### pir 센서
- 센서 감지로 카메라가 켜짐 (얼굴인식 기능위해 필요)
- 적외선 PIR센서(PIR, Passive Infrated Sensor)는말그대로수동적외선센서로써적외선을통해 사람의 움직임(모션, motion)을 감지하는센서

<img width="82" alt="image" src="https://github.com/user-attachments/assets/c4d6ca72-1c28-41a8-9324-27795141115a" />

### usb 포트
sd card 라즈베리파이에 직접 연결 안해도 된다

<img width="148" alt="image" src="https://github.com/user-attachments/assets/3c665cf0-ad18-4c7c-aa0a-ae6bad9a964f" />

### 파워
- 전기 공급

<img width="177" alt="image" src="https://github.com/user-attachments/assets/9683141e-a7e2-4ae8-b6d4-8095d63a5589" />




### 1. os 설치

라즈베리4 모델 b / 64bit bullseye desktop 버젼

- 현재 Raspberry Pi OS는 기본 데스크톱 환경만 포함된 Standard Desktop 버전



### 2. 라즈베리파이 os설치 후 네트워크 관리방법 변경

dhcpcd -> networkManager 로 변경

관리 범위: dhcpcd는 기본적으로 IP 주소 할당과 네트워크 인터페이스의 설정을 관리하는 반면,
NetworkManager는 여러 종류의 네트워크 인터페이스(Wi-Fi, 유선, VPN 등)를 포괄적으로 관리하는 데 사용됩니다



### 4. nginx 설치, 설정
```bash
sudo apt-get install nginx

sudo nano /etc/nginx/nginx.conf

http {
	client_max_body_size 0;
}

이유 : 클라이언트가 전송하는 데이터 크기를 제한하지 않아서 대용량 파일 업로드나 특정 상황에서 데이터를 제한 없이 전송할 수 있도록 하기 위해서

/etc/nginx/nginx.conf 파일에서 include /etc/nginx/modules-enabled/*.conf; 설정


sudo nano /etc/nginx/conf.d/localhost.conf

이유 : HTTP 요청과 WebSocket 요청을 처리하는 웹 서버를 설정


sudo service nginx restart
```

### 4. mariadb 설치

```bash
sudo apt-get install mariadb-server

mariadb 계정 등록 변경

sudo mysql -u root
set password for root@'localhost'=PASSWORD('dnlzlqkrtm');
flush privileges;
create database hizib;
exit

```

- MariaDB와 Nginx는 전통적으로 시스템의 서비스로 설치되며, 가상환경에 설치되지 않습니다.

### 5. virtualenv, virtualenvwraaper 설치

- ./profile ./bashrc 설정, virtualenvwrapper.sh 위치 주의 /usr/share/virtualenvwrapper/virtualenvwrapper.sh


### 6. www, python, sound, shell, font, json, css, js, Workspace, index.html, click, html 압축
```bash
tar -czvf kiosk.tar.gz www python sound shell font json css js Workspace index.html

# sftp 소스 다운
sftp pi@192.168.0.161

get kiosk.tar.gz

get /home/pi/kiosk.tar.gz /home/pi
```

### 디렉토리 구조 무시하고 현재 경로에 압축해제
- tar --strip-components=2 -xvzf /home/pi/work/kiosk.tar.gz -C /home/pi

### 7. 라즈베리 파이의 디스플레이 설정은 config.txt 파일에서 조정할 수 있습니다. 이 파일은 라즈베리 파이의 부팅 시 시스템 설정을 적용

sudo nano /boot/config.txt

### 8. ibus는 여러 언어의 입력을 지원하는 입력기 시스템 ibus
```bash
ibus 설치확인
dpkg -l | grep ibus-hangul

ps aux | grep ibus

```

### 9. 화면 보호기 끄기, 터치 민감도 설정





### 10. 네트워크 와이파이 자동연결





### 11. tty usb 연결 설정





### 12. tornado 설치, 실행





### 13. service 파일 설정
```bash

sudo nano /lib/systemd/system/tornado.service

/home/pi/www/shell/tornado.sh

tornado.sh 정의

/home/pi/.virtualenvs/elcsoft/bin/python /home/pi/www/python/webserver.py
```

### 14. 자동실행 설정
```bash

/etc/xdg/lxsession/LXDE-pi/autostart

@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@chromium-browser --kiosk --autoplay-policy=no-user-gesture-required --check-for-update-interval=31536000 http://127.0.0.1

sudo reboot
```


### 15. 의존성 패키지 제외하고 패키지 설치
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

# pip install opencv-python 오래걸림
# pip install face-recognition	설치 어려움
# 가상환경에 공간을 따로주는 방법 찾아봐야함

```

### 16. webserver 실행 해서 잘 돌아가는지 확인


### 17. 화상통화, 날씨, 달력, 문열기 흐름, mqtt 공부



