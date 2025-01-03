### 부팅 실패 원인 체크

```bash

python /home/pi/python/webserver.py

/home/pi/shell/tornado.sh

sudo nano /lib/systemd/system/tornado.service

sudo nano /etc/xdg/lxsession/LXDE-pi/autostart

chromium-browser --kiosk --autoplay-policy=no-user-gesture-required --check-for-update-interval=31536000 http://127.0.0.1


크롬 실행
chromium-browser --kiosk --no-sandbox --disable-gpu http://127.0.0.1

sudo nano ~/.xsession-errors

sudo systemctl status lightdm

sudo nano /var/log/Xorg.0.log

sudo nano /boot/config.txt

sudo Xorg -configure

cat /var/log/Xorg.1.log

/etc/X11/xorg.conf


sudo nano /boot/config.txt


```
