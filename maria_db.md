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

### scp 명령어로 전송
```bash
scp pi@remote_host:/home/pi/pi_zip.tar.gz pi@192.168.0.50:/home/pi/
```













