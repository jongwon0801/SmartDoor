#### certbot 설치

```less
# 최신 버전 대안 (Ubuntu 24.04 이상)
sudo apt update
sudo apt install certbot python3-certbot-nginx

# certbot
Nginx 웹 서버에서 자동으로 SSL 인증서를 설치·갱신할 수 있게 해주는 Certbot의 Nginx 플러그인


# 공인 도메인을 사용해야 SSL 인증서를 발급받을 수 있습니다.
sudo certbot --nginx -d api2.hizib.wikibox.kr
```

#### 🔐 발급 결과 요약
```less
도메인: api2.hizib.wikibox.kr

인증서 위치:

전체 체인: /etc/letsencrypt/live/api2.hizib.wikibox.kr/fullchain.pem

개인 키: /etc/letsencrypt/live/api2.hizib.wikibox.kr/privkey.pem

자동 갱신: 설정됨 (cron 또는 systemd timer에 의해 관리됨)

Nginx 설정 파일 수정됨: /etc/nginx/conf.d/hizib.conf에 HTTPS 적용됨

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

#### sudoer 권한을 사용자에게 부여
```less
sudo visudo

하단에 추가
hizib ALL=(ALL) NOPASSWD:ALL

사용자 hizib는 모든 사용자 권한으로 모든 명령어를 sudo로 실행 가능.
비밀번호 없이 실행 가능함
```

#### Mosquitto 설치
```less
sudo apt install mosquitto mosquitto-clients

sudo systemctl enable mosquitto.service

sudo systemctl restart mosquitto.service
```


#### mqtt 설정 변경
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

# 내용에 아래 세 줄 추가

listener 1883
password_file /etc/mosquitto/pwfile
allow_anonymous false

listener 1883
password_file: 사용자 인증을 위한 파일 경로 지정
allow_anonymous false: 익명 접속 차단 — 사용자/비밀번호 필수

sudo systemctl restart mosquitto
```

#### python paho-mqtt설치
```less
sudo apt install python3-paho-mqtt
```

#### DB user(hizib) 생성
```less
# 루트 계정으로 로그인했는지 확인
SELECT USER(), CURRENT_USER();

# 사용자 생성
CREATE USER 'hizib'@'%' IDENTIFIED BY 'wikibox';

# 권한 부여 (다른 사용자에게 권한 부여 GRANT OPTION은 생략)
GRANT ALL PRIVILEGES ON *.* TO 'hizib'@'%';

# 반영
FLUSH PRIVILEGES;

# 모든 사용자 보기
SELECT user, host FROM mysql.user;
```

#### 워크밴치 설정
```less
# mariaDB 외부 접속 허용
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf

bind-address = 0.0.0.0

sudo systemctl restart mariadb
```


#### 비즈뿌리오 설치

```less
https://www.bizppurio.com/help/download?qnaSelect=M
비즈클라이언트 DB연동 통합발송모듈 v4.07(UTF8 지원) 2025-04-25  /  biz_client_v4007.zip

# Mac -> 서버로 압축파일 복사
scp /Users/jongwon/Smartdoor/server_Test/biz_client_v4007.zip hizib@192.168.0.73:/home/hizib/bizppurio/

mkdir bizppurio

sudo apt install unzip

sudo unzip biz_client_v4007.zip
```

#### root 유저로 DB 로그인
```less
sudo mysql -u root -p
pw : wikibox

SELECT User, Host FROM mysql.user;
+-------------+-----------+
| User        | Host      |
+-------------+-----------+
| hizib        | %        |
| mariadb.sys | localhost |
| mysql       | localhost |
| root        | localhost |
+-------------+-----------+
```

#### hizib 유저로 DB 로그인
```less
mysql -u hizib -p

id : hizib
pw : wikibox
```

```less
# mysql 버젼 확인
mysql -u root -p -e "SELECT VERSION();"

MariaDB는 우분투 버전에 따라 기본으로 설치되는 버전이 다릅니다.
우분투의 APT 패키지 저장소에서 제공하는 기본 MariaDB 버전이 다르기 때문입니다.


+------------------+
| VERSION()        |
+------------------+
| 11.4.5-MariaDB-1 |
+------------------+

+-----------------------------------+
| VERSION()                         |
+-----------------------------------+
| 10.11.13-MariaDB-0ubuntu0.24.04.1 |
+-----------------------------------+

/home/hizib/bizppurio/config/uds.conf

UDS_IP = biz.ppurio.com
UDS_SEND_PORT = 18300
UDS_RECV_PORT = 18400
UDS_ID = hizibtest
UDS_PW = wiki0800*
USE_SSL = Y

DBNAME = MYSQL

DBURL = jdbc:mysql://localhost:3306/hizib?useUnicode=true&characterEncoding=utf-8&useSSL=false&allowPublicKeyRetrieval=true
DBUSER = hizib
DBPASS = wikibox
```
#### DBURL 옵션
| 옵션                             | 설명                                          | 필요 여부                             |
| ------------------------------ | ------------------------------------------- | --------------------------------- |
| `useUnicode=true`              | 유니코드 문자 지원 (한글 등)                           | ✅ 거의 항상 필요                        |
| `characterEncoding=utf-8`      | 문자 인코딩을 UTF-8로 지정                           | ✅ 한글 깨짐 방지                        |
| `useSSL=false`                 | SSL 없이 접속 (로컬/내부망에서 일반적)                    | ✅ SSL 미사용 시 필요 (경고 방지)            |
| `allowPublicKeyRetrieval=true` | 서버에서 공개키로 비밀번호 암호화 허용 (MySQL 8 이상일 때 주로 필요) | 🔶 **MySQL 8 이상이면 필요**, 아니면 생략 가능 |


#### 실행권한 부여

```less
/home/hizib/bizppurio/script

ls -al

sudo chmod 755 *

ls -al
```

#### 자바 설치
```less
sudo apt update
sudo apt install openjdk-21-jre-headless

java -version
```

#### 파일 소유권 변경
```less
sudo chown -R hizib:hizib /home/hizib/bizppurio

# 내부적으로 파일 접근 또는 경로 처리에 root 소유권이 문제가 될 수 있습니다.

# 변경 이전
-rw-r--r-- 1 root root 12650 Jun  2 01:15 uds.confx

# 변경 이후
-rw-rw-r--  1 hizib hizib 12309 Jun 17 02:39 uds.confx
```

#### 전송 시간 문제 해결 방법

sudo nano /home/hizib/bizppurio/script/biz_start

```less
#!/bin/sh

proc=`ps -ef | grep biz_client | grep -v vi |grep -v grep | grep -v sh`
if [ X"$proc" != X"" ]; then
        echo "Already Invoked"
        exit
fi

cd ..
java -Duser.timezone=GMT+09:00 -jar biz_client.jar config/uds &
```



