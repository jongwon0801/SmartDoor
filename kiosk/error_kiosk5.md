### 모니터 설정

```bash

# X 서버 확인
ps aux | grep X

# X 서버 수동 시작
startx

# GUI 부팅 설정 확인
sudo raspi-config

"System Options" > "Boot / Auto Login" > "Desktop Autologin"

sudo reboot

# 현재 환경의 lxsession 확인
ps aux | grep lxsession

# 실행 중이지 않다면 수동으로 실행해 GUI 환경이 나타나는지 확인
lxsession -s LXDE-pi -e LXDE

# lxsession 자동 실행 설정 확인
# 파일을 확인하여 필요한 항목이 누락되었는지 확인

/etc/xdg/lxsession/LXDE-pi/autostart

@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@chromium-browser --kiosk --autoplay-policy=no-user-gesture-required --check-for-update-interval=31536000 http://127.0.0.1

sudo reboot

# 필요한 패키지 확인 및 재설치

sudo apt-get update

sudo apt-get install --reinstall raspberrypi-ui-mods lxsession lxpanel pcmanfm

sudo apt-get install --reinstall raspberrypi-ui-mods lxsession xserver-xorg xinit
-> /etc/xdg/lxsession/LXDE-pi/autostart -> N을 입력하여 사용자 수정본을 그대로 유지

sudo reboot

# X 서버 로그 확인
cat /var/log/Xorg.0.log

# HDMI 연결 및 디스플레이 설정 확인
sudo nano /boot/config.txt

sudo reboot

```

#### sudo nano /etc/lightdm/lightdm.conf

- 주석 해제 greeter-session=pi-greeter

<img width="186" alt="image" src="https://github.com/user-attachments/assets/fa3a7a4d-7b89-40db-8e2e-c0c425c4b42f" />


/usr/share/dispsetup.sh






