### 키오스크 서버 ssh 접속
```bash
ssh pi@192.168.0.161
```

### 접속 가능한 라즈베리 기기 아이피 찾기
```bash
ping raspberrypi.local


sudo apt clean
sudo apt autoremove -y

sudo apt update
sudo apt upgrade
```
### nginx 설치

sudo apt-get install nginx

### mariadb 설치

```bash
sudo apt-get install mariadb-server
```

### mariadb 계정 등록 변경
```bash
SET PASSWORD FOR root@'localhost' = PASSWORD('dnlzlqkrtm');
```
```bash
FLUSH PRIVILEGES;
```
```bash
CREATE DATABASE hizib;
```
```bash
EXIT;
```

### 디렉토리 생성 디렉토리가 없다면, 아래 명령어로 디렉토리를 생성합니다:

```bash
sudo mkdir -p /home/pi/www/python/
```

### requirements.txt 생성 디렉토리가 준비되었으면, pip freeze 명령어를 실행하여 의존성 목록을 파일로 저장할 수 있습니다:

```bash
sudo bash -c 'pip freeze > /home/pi/www/python/requirements.txt'
```
### requirements.txt 권한 확인 rw-r-r 644
```bash
ls -l /home/pi/www/python/requirements.txt
```

### python 폴더로 이동, git clone
```bash
cd /home/pi/www/python/

git clone https://devtools.ncloud.com/2639830/wiki_smartdoor_kiosk.git

```

```bash
# 디렉토리 이동
cd /home/pi/www/python/

# elcsoft 가상 환경 생성
python3 -m venv elcsoft

# 가상 환경 활성화
# /home/pi/www/python/elcsoft에서 가상 환경을 활성화한 후,
source /home/pi/www/python/elcsoft/bin/activate

# 다른 디렉토리로 이동해도 가상 환경은 활성화된 상태로 유지됩니다.
cd /home/pi/www/python/
```
### 서버 파일 압축
```bash
tar -czvf pi_zip.tar.gz /home/pi/
```
- c: 아카이브 생성.
- z: gzip으로 압축.
- v: 진행 상황 표시.
- f: 파일 이름 지정.
### sftp 명령어로 압축파일 전송
```bash
mkdir work

cd work

sftp pi@192.168.0.161

get pi_zip.tar.gz

get /home/pi/pi_zip.tar.gz /home/pi
```
- /home/pi/pi_zip.tar.gz: FTP 서버나 원격 시스템에서 다운로드할 파일 경로입니다. 즉, FTP 서버에서 pi_zip.tar.gz 파일을 찾을 위치입니다.
- /home/pi: 로컬 시스템에서 저장할 경로입니다. 즉, 이 명령은 FTP 서버의 /home/pi/pi_zip.tar.gz 파일을 로컬 시스템의 /home/pi 디렉토리에 다운로드하겠다는 의미입니다.



### 라즈베리에 기기 압축해제
```bash
tar -xvzf /home/pi/work/pi_zip.tar.gz -C /home/pi

tar -xzvf archive.tar.gz
```
- tar:
- tar는 파일을 묶고 압축하거나 압축 해제하는 데 사용되는 명령어입니다.
- tar는 기본적으로 파일 아카이브 도구로, 압축을 수행하려면 다른 도구(예: gzip, bzip2)와 결합해야 합니다.

- -x (extract):
- 압축을 해제하는 옵션입니다.
즉, .tar.gz 파일을 풀어냅니다.

- -z (gzip):
- 파일이 gzip 형식으로 압축되었음을 나타내는 옵션입니다.
.tar.gz 파일은 tar로 묶은 후, gzip으로 압축된 파일입니다. 이 옵션은 gzip 압축을 해제하도록 tar에게 지시합니다.

- -v (verbose):
- verbose는 "자세한"을 의미합니다. 이 옵션을 사용하면 압축 해제 진행 상황을 출력합니다.
즉, 어떤 파일들이 압축 해제되는지 목록으로 보여줍니다.

- -f (file):
- 압축을 해제할 파일을 지정하는 옵션입니다.
- f 뒤에 오는 인자는 압축 파일의 이름이어야 합니다.
예를 들어, archive.tar.gz가 압축을 해제할 파일입니다.


### 다시 압축을 풀 때 디렉토리 구조를 무시하고 현재 경로에만 파일을 풀고 싶다면 다음 명령어를 사용하세요:

```bash
tar --strip-components=2 -xvzf /home/pi/work/pi_zip.tar.gz -C /home/pi
```

### --strip-components=2 옵션:
- 압축 파일 내부 디렉토리 구조에서 상위 디렉토리 두 개를 무시합니다.
- 이를 통해 /home/pi/home/pi/... 구조 대신 /home/pi/...에 파일이 풀립니다.

### sftp로 requirement.txt 파일 복사 하기위해 권한 디렉토리, 파일 권한 부여
```bash
sudo chmod 777 /home/pi/www/python/
sudo chmod 777 /home/pi/www/python/requirement.txt
```

### sftp 로 키오스크 서버에서 requirement.txt 파일가져오기
```bash
sftp pi@192.168.0.161

cd /home/pi/www/python

# 192.168.0.161의 requirements.txt 파일을 192.168.0.50의 /home/pi/www/python 경로로 다운로드
get requirements.txt /home/pi/www/python/ 

exit or ctrl + d
```

### 가상환경 생성, 활성화, 패키지 설치
```bash
python3 -m venv elcsoft

source elcsoft/bin/activate

cd /home/pi/www/python/

pip install -r requirements.txt
```

### 가상환경 경로 권한부여, 가상환경 디렉토리의 모든 파일 및 디렉토리의 소유자를 pi 사용자로 변경
```bash
sudo chmod 777 /home/pi/www/python/elcsoft/

sudo chown -R pi:pi /home/pi/www/python/elcsoft/
```

### service 파일 생성
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

### tornado.sh 셸

### 파이썬 내부 가상환경
```bash
/home/pi/shell/tornado.sh
```

```bash
# 가상환경 활성화
source /home/pi/www/python/elcsoft/bin/activate

# webserver.py 실행
python /home/pi/python/webserver.py

# tornado.service 파일 검색
sudo find / -name "webserver.py"
```

### /home/pi/shell/tornado.sh 
- /lib/systemd/system/tornado.service 서비스 파일로 webserver.py 를 실행하기 위해 sh 만듬
```bash
/home/pi/.virtualenvs/elcsoft/bin/python /home/pi/www/python/webserver.py
```

### /home/pi/.virtualenvs/elcsoft/bin/python:

- 이 경로는 Python 가상 환경의 실행 파일을 나타냅니다.
**virtualenv**는 프로젝트마다 독립된 Python 환경을 제공하는 도구로, 시스템의 기본 Python 환경에 영향을 주지 않고, 프로젝트에 필요한 패키지들을 관리할 수 있게 합니다.
- 이 경로는 **elcsoft**라는 이름의 가상 환경 내에 있는 Python 인터프리터를 실행하는 경로입니다. 따라서, 이 명령어는 elcsoft 가상 환경에서 Python 스크립트를 실행하도록 지정합니다.
  
### /home/pi/www/python/webserver.py:

- 이 경로는 실행할 Python 스크립트인 webserver.py의 위치를 나타냅니다.
- 이 스크립트는 웹 서버와 관련된 코드가 포함된 Python 파일일 가능성이 높습니다.
- webserver.py 파일 내에서 웹 서버를 실행하는 코드가 있을 것으로 추측됩니다. 예를 들어, Tornado, Flask, Django 등의 웹 서버 라이브러리를 사용하여 HTTP 요청을 처리하는 서버 코드가 포함되어 있을 수 있습니다.


### 가상환경 설치
```bash
pip install virtualenv
# ls 명령어로 숨겨진 파일 보기
ls -a
# find로 특정 경로 숨겨진 파일 찾기
find /home/pi/ -name ".*"

mkdir -p /home/pi/.virtualenvs/
```

```bash
cd /home/pi/.virtualenvs/

pip show virtualenv

which virtualenv

# 위치 : /home/pi/.local/lib/python3.9/site-packages

```

### ~/.bashrc 파일에 PATH 추가
```bash
nano ~/.bashrc

# 맨아래줄에 밑에 내용 추가
export PATH=$PATH:/home/pi/.local/bin

# 변경사항 적용
source ~/.bashrc

# elcsoft 가상환경 생성
virtualenv /home/pi/.virtualenvs/elcsoft

# 가상환경 활성화
source /home/pi/.virtualenvs/elcsoft/bin/activate

```
### virtualenvwrapper 설치
```bash

# kiosk 버젼
pip install virtualenvwrapper==4.8.4


# virtualenvwrapper 설정
export WORKON_HOME=~/ .virtualenvs
export VIRTUALENVWRAPPER_PYTHON=$(which python3)
source /home/pi/.local/bin/virtualenvwrapper.sh

source ~/.bashrc
```
