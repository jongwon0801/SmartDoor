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
```

#### nginx 설정
```less
sudo apt-get update
sudo apt install nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

#### nginx 설치
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
        fastcgi_pass   unix:/var/run/php/php8.4-fpm.sock;
        fastcgi_index  index.html;
        fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
        include        fastcgi_params;
        #include snippets/fastcgi-php.conf;
    }
}

```
#### 설정 블록이 어느 파일에 있는지 확인
```less
grep -r "server_name api1.hizib.wikibox.kr" /etc/nginx/

/etc/nginx/conf.d/hizib.conf:    server_name api1.hizib.wikibox.kr;

curl -I http://api1.hizib.wikibox.kr/
```

#### sudo nano /etc/nginx/nginx.conf

```less
#include /etc/nginx/sites-enabled/*; 주석처리
```

#### /etc/php/8.4/fpm/pool.d/www.conf
```less
security.limit_extensions = .php .php3 .php4 .php5 .php7 .html .htm
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


#### php 설치

```less
# php -v 명령어가 PHP 8.4를 설치하라고 안내
php -v

# Ubuntu 시스템에서 소프트웨어 속성 관리와 관련된 도구들을 설치하는 명령어. 이 도구는 외부 리포지터리(PPA)를 추가하거나 관리할 때 유용
sudo apt-get install -y software-properties-common

sudo apt-get update

sudo apt install php8.4-cli

# PHP 8.4에서 json 확장이 별도의 패키지로 제공되지 않으며 PHP의 기본 확장에 포함
php -m | grep json

# 다른 PHP 모듈들이 설치되어 있는지 확인
php -m

sudo apt install php8.4-curl php8.4-gd php8.4-mbstring php8.4-mysql php8.4-soap php8.4-intl php8.4-zip php8.4-xml php8.4-xmlrpc php8.4-cli php8.4-xsl
```

#### FPM 설치

```less
# FPM은 FastCGI Process Manager의 약자로, PHP를 웹 서버와 효율적으로 연결해주는 PHP 실행 엔진

sudo apt install php8.4-fpm

systemctl status php8.4-fpm

브라우저 → Nginx → PHP-FPM → PHP 코드 실행 → 결과 반환
```

#### php.ini 설정 변경
```less
sudo nano /etc/php/8.4/fpm/php.ini

nano에서는 Ctrl + W 누르고 short_open_tag 입력한 뒤 Enter

//short_open_tag를 검색해서 on으로 설정 변경
; 있으면 주석처리, 없어야함
short_open_tag=On

//memory_limit를 검색해서 256M로 변경
memory_limit = 256M

//upload_max_filesize를 검색해서 1024M로 변경
upload_max_filesize = 1024M

//max_file_uploads를 검색해서 20으로 변경
max_file_uploads = 20

//date.timezone를 검색해서 Asia/Seoul로 설정
date.timezone = Asia/Seoul

sudo systemctl restart php8.4-fpm

sudo systemctl enable php8.4-fpm
```

#### PHP 8.4-FPM의 기본 소켓 경로

```less
# 버젼이 바뀌면 소켓 경로 변경해야함
sudo nano /etc/php/8.4/fpm/pool.d/www.conf

listen = /run/php/php8.4-fpm.sock
```

#### 재시작
```less
sudo systemctl restart php8.4-fpm.service
```


#### 태그 수정
```less
sudo nano /home/hizib/php/library/class/DBConn.php

<? 이걸 <?php 이거로 변경
```

#### #[\AllowDynamicProperties] 속성 사용 (PHP 8.2 이상에서만 가능)
```less
sudo nano /home/hizib/php/library/class/DBConn.php

#[\AllowDynamicProperties]
class DBConn {

sudo nano /home/hizib/php/library/class/Component.php

#[\AllowDynamicProperties]
class Component {
```

#### composer 설치 (php 설치 되어있을 경우)
```less
1. Composer 설치 스크립트 다운로드 및 실행

cd ~
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"

2. Composer 전역 설치

sudo php composer-setup.php --install-dir=/usr/local/bin --filename=composer

3. 설치 스크립트 삭제, 버젼 확인
rm composer-setup.php

composer --version
```

#### php-jwt 최신 버전으로 업데이트
```less
Deprecated 경고는 **PHP 8.1+ 또는 8.2+**에서 자주 발생하는 현상입니다.
문제는 firebase/php-jwt 라이브러리가 nullable 타입을 명시하지 않고 파라미터를 선언했기 때문입니다.

composer require firebase/php-jwt:^6.10
```


