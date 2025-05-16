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

#### php 포스트맨 접속 거부
```less
sudo nano /var/log/nginx/hizib.error.log


location ~ \.php$ {
    root           /home/hizib;
    fastcgi_pass   unix:/var/run/php/php8.4-fpm.sock;
    fastcgi_index  index.php;
    fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
    include        fastcgi_params;
}

location ~ \.(html|htm)$ {
    root /home/hizib;
    # 정적 파일이라 별도 fastcgi_pass 필요 없음
}








```
