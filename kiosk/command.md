#### nginx 로그 (hizib서버, 라즈베리 nginx) 두개 확인 / 케이스별로 요청 시작위치 판단해서 브라우저 로그랑 같이확인

```bash
# 접속 로그
tail -f /var/log/nginx/access.log

# 에러 로그
tail -f /var/log/nginx/error.log

```

#### tornado 로그

```bash

# Tornado HTTP 요청과 WebSocket 메시지를 기록
cd /home/pi/log

# tornado.service 위치 (안에 tornado.sh로 webserver.py 재실행)
nano /lib/systemd/system/tornado.service

# tornado 서비스 재실행
sudo systemctl restart tornado.service

# 상태보기
sudo systemctl status tornado.service

# systemd 새 서비스 적용
sudo systemctl daemon-reload


```
