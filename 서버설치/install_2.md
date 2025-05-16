#### certbot 설치

```less
# 최신 버전 대안 (Ubuntu 24.04 이상)
sudo apt update
sudo apt install certbot python3-certbot-nginx

# certbot
Nginx 웹 서버에서 자동으로 SSL 인증서를 설치·갱신할 수 있게 해주는 Certbot의 Nginx 플러그인

# 공인 도메인을 사용해야 SSL 인증서를 발급받을 수 있습니다.
sudo certbot --nginx -d api.hizib.wikibox.kr
```

#### ubuntu, hizib 계정 만들기
```less
sudo adduser ubuntu

sudo usermod -aG sudo ubuntu

sudo usermod -aG sudo hizib

sudo chmod 755 /home/ubuntu

sudo adduser hizib

sudo chmod 755 /home/hizib

# pi 유저 삭제
sudo deluser --remove-home pi
```

#### Mosquitto 설치
```less
sudo apt install mosquitto mosquitto-clients

sudo systemctl enable mosquitto.service

sudo systemctl restart mosquitto.service
```


#### 설정 변경
```less
id : hizib
pw : wikibox
```
```less
# 사용자(hizib) 와 비밀번호(wikibox) 생성
sudo mosquitto_passwd -c /etc/mosquitto/pwfile hizib

Password: wikibox
Reenter password: wikibox
```

```less
sudo chmod 640 /etc/mosquitto/pwfile

# 읽기 권한은 mosquitto 사용자만 갖도록 제한 (보안 강화)
sudo chown mosquitto:mosquitto /etc/mosquitto/pwfile
```

#### Mosquitto 설정파일 수정
```less
# Mosquitto 설정파일 수정
sudo nano /etc/mosquitto/mosquitto.conf

# 내용에 아래 두 줄 추가
password_file /etc/mosquitto/pwfile
allow_anonymous false

password_file: 사용자 인증을 위한 파일 경로 지정
allow_anonymous false: 익명 접속 차단 — 사용자/비밀번호 필수

sudo systemctl restart mosquitto
```

#### 비즈뿌리오 설치

```less
# Mac -> 서버로 압축파일 복사
비즈클라이언트 DB연동 통합발송모듈 v4.07(UTF8 지원) biz_client_v4007.zip
scp /Users/jongwon/biz/biz_client_v4007.zip hizib@192.168.0.73:/home/hizib/

mkdir bizppurio

sudo apt install unzip

sudo unzip biz_client_v4007.zip

```






