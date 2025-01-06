### 1. os 설치

라즈베리4 모델 b / 64bit bullseye desktop 버젼

```bash
if dpkg -l | grep -E 'libreoffice|wolfram' > /dev/null; then
    echo "Desktop Environment with Recommended Applications (Full version)"
else
    echo "Standard Desktop Environment (without Recommended Applications)"
fi
```

- Full 버전에는 libreoffice 및 wolfram 패키지가 포함되지만, 해당 패키지가 설치되어 있지 않으므로 Full 버전이 아닙니다.
- 현재 Raspberry Pi OS는 기본 데스크톱 환경만 포함된 Standard Desktop 버전입니다.


### 2. 전체 프로그램 업데이트

```bash
sudo apt clean
sudo apt autoremove -y

sudo apt update
sudo apt upgrade
```

### 3. 라즈베리파이 os설치 후 네트워크 관리방법 변경

```bash
sudo raspi-config

networkManager 로 변경

관리 범위: dhcpcd는 기본적으로 IP 주소 할당과 네트워크 인터페이스의 설정을 관리하는 반면,
NetworkManager는 여러 종류의 네트워크 인터페이스(Wi-Fi, 유선, VPN 등)를 포괄적으로 관리하는 데 사용됩니다

```

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
# 디렉토리 구조 무시하고 현재 경로에 압축해제
- tar --strip-components=2 -xvzf /home/pi/work/kiosk.tar.gz -C /home/pi

### 7. 라즈베리 파이의 디스플레이 설정은 config.txt 파일에서 조정할 수 있습니다. 이 파일은 라즈베리 파이의 부팅 시 시스템 설정을 적용

sudo nano /boot/config.txt

### 8. ibus는 여러 언어의 입력을 지원하는 입력기 시스템 ibus
```bash
ibus 설치확인
dpkg -l | grep ibus-hangul

ps aux | grep ibus

```

### 9. 화면 보호기 끄기







### 10. 네트워크 와이파이 자동연결








### 11. tty alias 설정







