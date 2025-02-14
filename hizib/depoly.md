#### ssh 접속 기록 삭제

```bash
sudo nano ~/.ssh/known_hosts

```
#### 위키박스 서버 SSH 접속

#### 서버 접속
```bash
ssh ubuntu@api.hizib.wikibox.kr   # 비밀번호: elcsoft
```

#### 키오스크 서버 SSH 점속
```bash
ssh pi@192.168.0.161   # 비밀번호: elcsoft
```

#### 라즈베리4 기기 SSH 점속
```bash
ssh pi@192.168.0.50   # 비밀번호: pi
```

#### ubuntu 디렉토리로 이동

```bash
cd ubuntu
```

파일 삭제
```bash
sudo rm -f googlehome
```

폴더 삭제 (내용물 포함)
```bash
sudo rm -rf googlehome
```

#### 폴더 생성
```bash
mkdir googlehome
```

<br><br>
---
#### 가상환경 설치

#### 가상환경 생성

```bash
python3 -m venv myenv
```

#### 가상환경 실행
```bash
source myenv/bin/activate
```
---

#### 압축 과정

#### 압축 파일 생성

```bash
zip -r googlehome.zip requirements.txt wiki-smartdoor-6066-58f1a4951f27.json deploy.sh templates app.py config.json
```

#### 로컬 서버에서 원격 서버로 파일 전송
```bash
scp /Users/jongwon/work/googlehome.zip ubuntu@api.hizib.wikibox.kr:/home/ubuntu/googlehome/
```

#### 원격 서버에서 파일 확인

```bash
ls /home/ubuntu/googlehome/
```

#### 해당 경로로 이동

```bash
cd /home/ubuntu/googlehome
```

#### 압축 해제

```bash
unzip googlehome.zip
```

---
## 서버 실행
#### 실행 권한 확인 및 추가

```bash
ls -l deploy.sh
```

#### 실행 권한 추가
```bash
chmod +x deploy.sh
```


#### 서버 셸 스크립트 실행
```bash
./deploy.sh
```

#### 로그 실시간 보기

```bash
tail -f app.log
```

#### 백그라운드 실행 중인 앱 조회
```bash
ps aux | grep 'python3 app.py'
```


---
#### Ngnix 설정 변경(여기선 안쓰지만 도메인 사서 할때 설정 필요)
#### Nginx 기본 설정 파일 수정

```bash
sudo nano /etc/nginx/sites-available/default
```
#### Conf 파일 생성

```bash
sudo nano /etc/nginx/conf.d/googlehome.conf
```

#### Nginx 기본 설정 파일 수정

```bash
vi /etc/nginx/nginx.conf
```

#### Conf 파일 강제 삭제

```bash
sudo rm -f googlehome.conf
```

---
#### Ngnix virtual directory 설정

#### Conf 파일 경로 (여러 호스트들을 정의 conf)

```bash
cd /etc/nginx/conf.d/
```

#### hizib.conf 파일에 /googlehome location 추가

```bash
vi hizib.conf
```

```bash
location /googlehome {
        proxy_pass http://127.0.0.1:5000;  # Flask의 /googlehome으로 직접 전달
        proxy_set_header Host $host;
    }
```
---
#### Ngnix 재시작

#### Nginx 설정 수정 후 재시작
```bash
vi /etc/nginx/nginx.conf
```

```bash
sudo nginx -t   # 설정 파일 문법 검사
sudo systemctl restart nginx  # Nginx 재시작
```
