#### autostart 키오스크 모드 실행전에 와이파이 설정 먼저 하도록 변경
```bash
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart

@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash

# 네트워크 설정 도구 실행 (예: NetworkManager 또는 Raspberry Pi 설정 도구)
@nm-applet

# 네트워크 설정 후 키오스크 모드로 실행
@/home/pi/start-kiosk.sh

# 기존 Chromium 실행은 주석 처리됨
# @chromium-browser --kiosk --autoplay-policy=no-user-gesture-required --check-for-update-interval=31536000 http://127.0.0.1
# @chromium-browser http://127.0.0.1
```

#### 홈 디렉토리에 start-kiosk.sh 셸 생성
```bash
Sudo nano ~/start-kiosk.sh


#!/bin/bash

# 네트워크 연결 확인
while ! ping -c 1 -W 1 8.8.8.8; do
    echo "Waiting for network..."
    sleep 5
done

# Chromium 키오스크 모드 실행
chromium-browser --kiosk --autoplay-policy=no-user-gesture-required --check-for-update-interval=31536000 http://127.0.0.1
```

#### 키오스크 실행 셸 권한추가, 파일 소유자 변경
```bash
Sudo chmod +x ~/start-kiosk.sh

ls -l /home/pi/start-kiosk.sh

-rwxr-xr-x 1 root root 289  1월 23 15:00 /home/pi/start-kiosk.sh

현재 /home/pi/start-kiosk.sh 파일의 소유자가 root로 설정되어 있습니다.
이는 일반 사용자(pi)가 스크립트를 실행할 때 권한 문제가 발생할 가능성을 의미합니다.

sudo chown pi:pi /home/pi/start-kiosk.sh
```
