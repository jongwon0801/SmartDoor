### 키오스크 서버 ssh 접속
```bash
ssh pi@192.168.0.161
```

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

### pyhon 폴더로 이동, git clone
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

### sftp 명령어로 압축파일 전송
```bash
mkdir work

cd work

sftp pi@192.168.0.161

get pi_zip.tar.gz
```


### 라즈베리에 기기 압축해제
```bash
tar -xvzf /home/pi/work/pi_zip.tar.gz -C /home/pi
```

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








