#### sudo nano /etc/nginx/conf.d/hizib.conf

```less
server {
    listen 80;
    server_name 192.168.0.73;

    charset utf-8;
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

        # 중요! PHP가 무시되지 않도록 try_files 사용
        try_files $uri $uri/ /index.php?$args;
    }

    # 오류 페이지 설정
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }

    # PHP 파일 처리
    location ~ \.php$ {
        root           /home/hizib;
        fastcgi_pass   unix:/var/run/php/php8.4-fpm.sock;
        fastcgi_index  index.php;
        fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
        include        fastcgi_params;
    }

    # HTML 파일은 정적으로 제공
    location ~ \.(html|htm)$ {
        root /home/hizib;
    }
}

```
