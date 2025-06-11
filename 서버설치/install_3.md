#### 현재 디렉토리 숨김파일 빼고 압축
```less
cd /home/hizib

sudo tar czvf hizib_backup.tar.gz --exclude='.*' *
```

#### Mac에서 받기
```less
scp ubuntu@13.124.155.19:/home/hizib/hizib_backup.tar.gz /Users/jongwon/biz/

scp /Users/jongwon/biz/hizib_backup.tar.gz hizib@192.168.0.73:/home/hizib/

tar xzvf hizib_backup.tar.gz
```

#### Mqtt 브로커 주소 수정
```less
sudo nano mqtt.py 

# broker 정보
broker_address = "192.168.0.73"

sudo nano mqtt_reply.py

# broker 정보
broker_address = "192.168.0.73"
```

