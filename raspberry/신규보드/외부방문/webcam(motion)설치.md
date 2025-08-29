#### 웹서버 직접 안띄우고 motion 애플리케이션 사용
```less
#motion 설치
sudo apt update
sudo apt install motion
```

#### motion 설정 파일 수정
```less
sudo nano /etc/motion/motion.conf
```

#### 파일 내용을 아래처럼 찾아 수정합니다. (Ctrl+W로 검색할 수 있습니다)
```less
daemon on -> daemon off (백그라운드 실행 대신 포그라운드 실행)

stream_localhost on -> stream_localhost off (외부 IP에서도 스트림 접근 허용)

stream_port 8081 (기본값인 8081번 포트 사용. 원하면 변경 가능)

movie_quality 75 (스트림 품질. 기본값)

# framerate=10: 초당 10장의 이미지를 보여주어 더 부드러운 영상을 제공
framerate 5 (프레임 속도, 기본 2fps. 더 빠르게 보고 싶으면 15-30 정도로 늘려보세요.)

width 640(320)
height 480(240) (카메라 해상도 설정. 원하면 변경)

저장 후 닫기
```

#### 로그 디렉토리 생성 및 권한 설정:
```less
sudo mkdir -p /var/log/motion
sudo chown motion:motion /var/log/motion
sudo chmod 755 /var/log/motion
```

#### 로그 파일 생성 및 권한 설정:
```less
sudo touch /var/log/motion/motion.log
sudo chown motion:motion /var/log/motion/motion.log
sudo chmod 644 /var/log/motion/motion.log
```

#### 다시 Motion 서비스 시작:
```less
sudo systemctl start motion

또는 만약 백그라운드 데몬으로 실행하지 않고 바로 터미널에서 실행하려면,

sudo motion 이라고 입력합니다.
```

#### 재부팅 후 자동 시작 설정
```less
sudo systemctl is-enabled motion

# disabled로 나온다면
sudo systemctl enable motion

```

##### 맥북에서 주소창으로 접속
```less
http://[라즈베리 파이 IP 주소]:8081
```
