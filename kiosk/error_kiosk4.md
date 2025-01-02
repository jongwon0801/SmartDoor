### 부팅 실패 원인 체크

```bash


크롬 실행
chromium-browser --kiosk --no-sandbox --disable-gpu http://127.0.0.1

sudo nano /etc/xdg/lxsession/LXDE-pi/autostart

sudo nano ~/.xsession-errors

sudo systemctl status lightdm

sudo nano /var/log/Xorg.0.log

sudo nano /boot/config.txt

sudo Xorg -configure

cat /var/log/Xorg.1.log







sudo nano /boot/config.txt

[all]
# 기존 설정들...

# HDMI 출력 강제 설정
hdmi_force_hotplug=1
hdmi_drive=2














```
