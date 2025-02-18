#### sudo nano /etc/nginx/conf.d/localhost.conf

```bash

server {
        listen 80;
        server_name 127.0.0.1 localhost;

        charset utf-8;
        #access_log /var/log/nginx/host.access.log  main;

        location / {
                root /home/pi/www;
                index index.html index.htm;
        }

        location ^~ /ws/ {
                rewrite ^/ws/(.*)$ /ws/$1 break;
                proxy_pass http://127.0.0.1:8080/ws/$1;
                proxy_http_version      1.1;
                proxy_set_header        upgrade $http_upgrade;
                proxy_set_header        Connection "upgrade";
                proxy_set_header        Host $host;
        }

        #error_page 404 /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
                root /usr/share/nginx/html;
        }

}

```
