#### 현재 디렉토리 숨김파일 빼고 압축
```less
cd /home/hizib

sudo tar czvf hizib_backup.tar.gz --exclude='.*' *
```

#### Mac에서 명령어 실행
```less
#  Mac에서 명령어 쳐서 클라우드 파일 받기
scp ubuntu@13.124.155.19:/home/hizib/hizib_backup.tar.gz /Users/jongwon/Smartdoor/server_Test

# 맥에서 테스트 서버로 복사
scp /Users/jongwon/Smartdoor/server_Test/hizib_backup.tar.gz hizib@192.168.0.73:/home/hizib/

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

#### 로컬 문에서 서버 접속 주소 수정
```less
grep -r "api.hizib.wikibox.kr" ./

~/www/js/jquery.elc.hizib.garbage.js
~/www/js/jquery.elc.hizib.ws.receive.js
~/www/kiosk/js/jquery.elc.hizib.garbage.js
~/www/kiosk/js/jquery.elc.hizib.ws.receive.js
~/www/kiosk/python/elcsoft/component.py
~/www/kiosk/python/elcsoft/model/code.py
~/www/kiosk/python/elcsoft/model/smartdoor_group.py
~/www/kiosk/python/elcsoft/controller/smartdoor_vod.py
~/www/kiosk/python/elcsoft/controller/smartdoor_guestkey.py
~/www/kiosk/python/elcsoft/controller/smartdoor_schedule.py
~/www/kiosk/python/elcsoft/controller/user.py
~/www/kiosk/python/elcsoft/controller/smartdoor_notice.py
~/www/kiosk/python/elcsoft/controller/smartdoor_log.py
~/www/kiosk/python/elcsoft/controller/smartdoor_message.py
~/www/kiosk/python/elcsoft/controller/smartdoor_item.py
~/www/kiosk/python/elcsoft/controller/smartdoor_group.py
~/www/kiosk/python/elcsoft/controller/smartdoor.py
~/www/kiosk/python/elcsoft/controller/vod.py
~/www/kiosk/python/elcsoft/controller/smartdoor_user.py
~/www/kiosk/python/elcsoft/controller/smartdoor_cmd.py
~/www/kiosk/python/weather.py
~/www/kiosk/html/user/view.html
~/www/python/elcsoft/component.py
~/www/python/elcsoft/model/code.py
~/www/python/elcsoft/model/smartdoor_group.py
~/www/python/elcsoft/controller/smartdoor_vod.py
~/www/python/elcsoft/controller/smartdoor_guestkey.py
~/www/python/elcsoft/controller/smartdoor_schedule.py
~/www/python/elcsoft/controller/user.py
~/www/python/elcsoft/controller/smartdoor_notice.py
~/www/python/elcsoft/controller/smartdoor_log.py
~/www/python/elcsoft/controller/smartdoor_message.py
~/www/python/elcsoft/controller/smartdoor_item.py
~/www/python/elcsoft/controller/smartdoor_group.py
~/www/python/elcsoft/controller/smartdoor.py
~/www/python/elcsoft/controller/vod.py
~/www/python/elcsoft/controller/smartdoor_user.py
~/www/python/elcsoft/controller/smartdoor_cmd.py
~/www/html/user/view.html



```



