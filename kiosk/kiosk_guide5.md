### tornado.service 실행

```bash

cd /lib/systemd/system

sudo systemctl start tornado.service

sudo systemctl status tornado.service 


# tornado.service / restart 부분은 guide1 이랑 변경함
[Unit]
Description=TornadoWebserver

[Service]
ExecStart=/home/pi/shell/tornado.sh
Restart=on-failure
User=pi
Group=pi

[Install]
WantedBy=multi-user.target

```

### tornado.sh 실행

```bash

cd shell

# tornado.sh
/home/pi/.virtualenvs/elcsoft/bin/python /home/pi/www/python/webserver.py






```
