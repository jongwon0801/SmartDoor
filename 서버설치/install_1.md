#### ubuntu os 설치
```less
sudo apt update
sudo apt upgrade
```

#### ubuntu 버젼확인
```less
lsb_release -a

Distributor ID:	Ubuntu
Description:	Ubuntu 25.04
Release:	25.04
Codename:	plucky

-> 이 버젼으로 설치 결과 fpm 7.4 설치 불가
-> fpm 8.2 부터 문법 엄격해짐
-> php 소스 바꿔야할 부분 늘어남
-> 우분투 lts 24.04.2 로 변경
```
#### ubuntu 버젼확인
```less
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 24.04.2 LTS
Release:	24.04
Codename:	noble
```
#### nginx 설치
```less
sudo apt-get update
sudo apt install nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

#### nginx conf.d 설정
```less
sudo nano /etc/nginx/conf.d/hizib.conf

server {
listen 80;
    server_name api2.hizib.wikibox.kr;

    charset utf-8;
    #access_log  /var/log/nginx/hizib.access.log  main;
    error_log /var/log/nginx/hizib.error.log;

    location /image {
        alias /home/hizib/image;
    }

    location / {
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, DELETE, PATCH, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'Content-Type, Authorization';
            add_header 'Access-Control-Max-Age' 86400;
            return 204;
        }

        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Content-Type' 'application/json' always;
        root /home/hizib;
        index index.html index.htm index.php;
        if (!-e $request_filename) {
                rewrite ^(.*)$ /index.html;
        }
    }

    #error_page 404 /404.html;


    # redirect server error pages to the static page /50x.html
    #
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }

    location ~ \.(php|html|htm)$ {
        root           /home/hizib;
        fastcgi_pass   unix:/var/run/php/php7.4-fpm.sock;
        fastcgi_index  index.html;
        fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
        include        fastcgi_params;
        #include snippets/fastcgi-php.conf;
    }
}

```
#### nginx 에러 로그
```less
sudo tail -n 50 /var/log/nginx/hizib.error.log
```

#### 설정 블록이 어느 파일에 있는지 확인
```less
grep -r "server_name api2.hizib.wikibox.kr" /etc/nginx/

/etc/nginx/conf.d/hizib.conf:    server_name api2.hizib.wikibox.kr;

curl -I http://api2.hizib.wikibox.kr/
```

#### sudo nano /etc/nginx/nginx.conf

```less
#include /etc/nginx/sites-enabled/*; 주석처리
```

#### php 7.4 설치
```less
sudo apt-get install -y software-properties-common

sudo add-apt-repository ppa:ondrej/php

sudo apt-get update

sudo apt-get install -y php7.4

sudo apt-get install -y php7.4-{curl,gd,mbstring,mysql,soap,json,intl,zip,xml,xmlrpc,cli,xsl}
```

#### 아파치 제거
1. Apache 관련 패키지 확인
```less
dpkg -l | grep apache2
```

2. Apache 완전히 제거
```less
sudo apt purge apache2 apache2-utils apache2-bin apache2.2-common

sudo apt autoremove
```


#### php.ini 설정 변경
```less
sudo nano /etc/php/7.4/fpm/php.ini

//short_open_tag를 검색해서 on으로 설정 변경
; short_open_tag=Off
short_open_tag=On

//memory_limit를 검색해서 256M로 변경
memory_limit = 256M


//upload_max_filesize를 검색해서 1024M로 변경
upload_max_filesize = 1024M

//max_file_uploads를 검색해서 20으로 변경
max_file_uploads = 20

//date.timezone를 검색해서 Asia/Seoul로 설정
date.timezone = Asia/Seoul
```

#### /etc/php/7.4/fpm/pool.d/www.conf 설정변경
```less
sudo nano /etc/php/7.4/fpm/pool.d/www.conf

listen = /var/run/php/php7.4-fpm.sock

# 맨앞에 ; 없애야함
security.limit_extensions = .php .html .htm
```

#### php 재가동
```less
sudo systemctl restart php7.4-fpm.service
```

#### mariadb 설치

```less
sudo apt install mariadb-server
sudo systemctl start mariadb
sudo systemctl enable mariadb

# enter 누르다가 비밀번호 설정
sudo mariadb-secure-installation

sudo mysql -u root -p
비밀번호 : wikibox
```



