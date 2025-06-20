#### FTP 정보
```less
sftp wikibox2020@wikismartdoor.com

IP : 210.114.6.139

# ftp, db 계정
id : wikibox2020
pw : wikiboxftp2323
```

#### Mac 에서 카페24 호스팅 소스 scp로 다운로드
```less
scp -r wikibox2020@wikismartdoor.com:/wikibox2020/www /Users/jongwon/Smartdoor/hosting
```

#### 폴더 생성
```less
mkdir -p /home/hizib/homepage
```

#### Mac에 있는 www 폴더 api2서버로 복사
```less
scp -r /Users/jongwon/Smartdoor/hosting/www hizib@192.168.0.73:/home/hizib/homepage/
```

#### 도메인 A 레코드 추가
```less
카페 24에서 wikismartdoor.com 도메인에 A 레코드 homepage. 추가

서브 도메인 : homepage.wikismartdoor.com
IP       : 175.211.153.28

175.211.153.28 (회사 공인 IP)
api2.hizib.wikibox.kr (192.168.0.73 서버)
```

#### /etc/nginx/conf.d/homepage.conf

```less
server {
    listen 80;
    server_name homepage.wikismartdoor.com;

    root /home/hizib/homepage/www/home;
    index index.php index.html;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}



```

#### 특정 파일 검색
```less
grep -rl "dbconfig.php"

find . -type f -name "*.sql"
```


#### dbconfig.php 경로
```less
/home/hizib/homepage/www/home/data/dbconfig.php
```

#### DB, 계정 생성
```less
# 디비접속
sudo mysql -u root -p

pw : wikibox


CREATE DATABASE wikibox2020 CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE USER 'wikibox2020'@'localhost' IDENTIFIED BY 'wikiboxftp2323';

GRANT ALL PRIVILEGES ON wikibox2020.* TO 'wikibox2020'@'localhost';

FLUSH PRIVILEGES;

EXIT;
```

#### .sql 파일 임포트
```less
mysql -u root -p wikibox2020 < /home/hizib/homepage/www/home/install/gnuboard5.sql

mysql -u root -p wikibox2020 < /home/hizib/homepage/www/home/adm/sql_write.sql

mysql -u root -p wikibox2020 < /home/hizib/homepage/www/home/adm/sms_admin/sms5.sql
```

#### 이미지 경로 수정
```less
vscode 에서 cmd f home -> replace 공백

src="/home/img/box02_icon01.png" 경로변경
-> src="/img/box02_icon01.png"
```




































