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

#### /home/hizib 권한 부여
```less
sudo chmod 755 /home/hizib
```

#### Mqtt 브로커 주소 수정
```less
sudo nano mqtt.py 

# broker 정보
broker_address = "175.211.153.28"

sudo nano mqtt_reply.py

# broker 정보
broker_address = "175.211.153.28"
```

#### /home/hizib/lib.php
```less
<?php
//db설정
$_lib['db']['master'] = new stdClass();
$_lib['db']['master'] -> type = "mysql";
$_lib['db']['master'] -> host = "localhost";
$_lib['db']['master'] -> port = 3306;
$_lib['db']['master'] -> name = "hizib";
$_lib['db']['master'] -> user = "hizib";
$_lib['db']['master'] -> passwd = "wikibox";
$_lib['db']['master'] -> charset = "utf8";
$_lib['db']['master'] -> autocommit = 1;

$_lib['db']['slave'] = new stdClass();
$_lib['db']['slave'] -> type = "mysql";
$_lib['db']['slave'] -> host = "localhost";
$_lib['db']['slave'] -> port = 3306;
$_lib['db']['slave'] -> name = "hizib";
$_lib['db']['slave'] -> user = "hizib";
$_lib['db']['slave'] -> passwd = "wikibox";
$_lib['db']['slave'] -> charset = "utf8";
$_lib['db']['slave'] -> autocommit = 1;

//mqtt
$_lib['mqtt']['host'] = "175.211.153.28";
$_lib['mqtt']['port'] = "1883";
$_lib['mqtt']['user'] = "hizib";
$_lib['mqtt']['passwd'] = "wikibox
";
//$_lib['mqtt']['host'] = "118.67.142.61";

//특별 path 설정
$_lib['directory']['www'] = '/home/hizib';				//일반 사이트
$_lib['directory']['m'] = '/home/hizib';				//m 사이트
$_lib['directory']['master'] = '/home/hizib';			//관리자 사이트
$_lib['directory']['api'] = '/home/hizib';				//api 사이트
$_lib['directory']['app'] = '/home/hizib';				//APP 사이트

//특별 url 설정
$_lib['url']['www'] = '//www.hizib.wikibox.kr';			//일반 사이트
$_lib['url']['m'] = '//m.hizib.wikibox.kr';				//m 사이트
$_lib['url']['master'] = '//master.hizib.wikibox.kr';	//관리자 사이트
$_lib['url']['api'] = '//api.hizib.wikibox.kr';			//api 사이트
$_lib['url']['app'] = 'https://api.hizib.wikibox.kr/download';	//APP 사이트

//기본적인 정의
$_lib['website'] = new stdClass();
$_lib['website'] -> name = "WIKI Smartdoor";
$_lib['website'] -> nickname = "위키 스마트도어";
$_lib['website'] -> callback = "15774594";
$_lib['website'] -> email = "webmaster@wikibox.kr";
$_lib['website'] -> domain = "hizib.wikibox.kr";

$_lib['directory']['root'] = '/home/hizib/';
$_lib['directory']['php'] = '/home/hizib/php';
$_lib['directory']['python'] = '/home/hizib/python';
$_lib['directory']['library'] = $_lib['directory']['php'].'/library';
$_lib['directory']['default'] = $_lib['directory']['root'].'/www';

$_lib['directory']['home'] = $_lib['directory']['www'];

//기본언어 설정
$_lib['language'] = 'ko,en';

//아고라설정
$_lib['agora']['appID'] = "8a8331548d8c4b88a76952d9b103cbad";
$_lib['agora']['appCertificate'] = "33e81f0573a64f9b895a9d2341e4361b";

//Azure 안면인식 설정
$_lib['azure']['appkey'] = "33e81f0573a64f9b895a9d2341e4361b";

//faceplusplus
$_lib['faceplusplus']['apikey'] = "dQsdsb--qjBV-eGNnSwC3-qVc5XLn40o";
$_lib['faceplusplus']['apiscret'] = "TcH4v9nQPjNMOCx5w1yJmYUBHeiitZss";

//naver
$_lib['ncloud']['accessKey'] = 'TTaMlvfgSD23fz3hh6wd';
$_lib['ncloud']['secretKey'] = 'bpPqe72iGkBajHL4h3noqGNqiRakch9eh9HvmC1Q';
$_lib['ncloud']['serviceId'] = [];
$_lib['ncloud']['serviceId']['push'] = 'ncp:push:kr:263983027579:wikibox';
$_lib['ncloud']['serviceId']['sms'] = 'ncp:sms:kr:263983040365:watchbook';
$_lib['ncloud']['serviceId']['bizmsg'] = 'ncp:kkobizmsg:kr:2639830:wikibox';

//라이브러리 가져오기
include_once($_lib['directory']['library'].'/lib.php')
?>

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



