# 위키박스 SSH 및 배포 명령어

### 압축해서 서버로 보내기 (배포)


서버 접속
```bash
ssh ubuntu@api.hizib.wikibox.kr   # 비밀번호: elcsoft
```

서버 내 작업
ubuntu 디렉토리로 이동

```bash
cd ubuntu
```


실행 권한 확인
```bash
ls -l deploy.sh
```

파일 삭제
```bash
sudo rm -f googlehome
```

폴더 삭제 (내용물 포함)
```bash
sudo rm -rf googlehome
```

폴더 생성
```bash
mkdir googlehome
```

### 가상환경 설치

가상환경 생성

```bash
python3 -m venv myenv
```

가상환경 실행
```bash
source myenv/bin/activate
```

서버 셸 스크립트 실행
```bash
./deploy.sh
```

로그 실시간 보기

```bash
tail -f app.log
```

압축 파일 생성

```bash
zip -r googlehome.zip requirements.txt wiki-smartdoor-6066-58f1a4951f27.json deploy.sh templates app.py config.json
```

로컬 서버에서 원격 서버로 파일 전송
```bash
scp /Users/jongwon/work/googlehome.zip ubuntu@api.hizib.wikibox.kr:/home/ubuntu/googlehome/
```

원격 서버에서 파일 확인

```bash
ls /home/ubuntu/googlehome/
```

해당 경로로 이동

```bash
cd /home/ubuntu/googlehome
```

압축 해제

```bash
unzip googlehome.zip
```


실행 권한 확인 및 추가

```bash
ls -l deploy.sh
```

실행 권한 추가
```bash
chmod +x deploy.sh
```

Nginx 기본 설정 파일 수정

```bash
sudo nano /etc/nginx/sites-available/default
```

백그라운드 실행 중인 앱 조회
```bash
ps aux | grep 'python3 app.py'
```

Nginx 기본 설정 파일 수정

```bash
vi /etc/nginx/nginx.conf
```

Conf 파일 강제 삭제

```bash
sudo rm -f googlehome.conf
```

Conf 파일 생성

```bash
sudo nano /etc/nginx/conf.d/googlehome.conf
```

Conf 파일 경로 (여러 호스트들을 정의 conf)

```bash
cd /etc/nginx/conf.d/
```

Nginx 설정 수정 후 재시작

```bash
vi /etc/nginx/nginx.conf

Nginx 설정 파일 문법 검사 및 재시작
```bash
sudo nginx -t   # 설정 파일 문법 검사
sudo systemctl restart nginx  # Nginx 재시작
```
