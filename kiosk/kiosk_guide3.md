### 자동실행

```bash
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart

@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash

@chromium-browser --kiosk --autoplay-policy=no-user-gesture-required --check-for-update-interval=31536000 http://127.0.0.1
#@chromium-browser http://127.0.0.1

```

### 호스트명변경
```bash

sudo nano /etc/hosts

127.0.0.1       localhost
::1             localhost ip6-localhost ip6-loopback
ff02::1         ip6-allnodes
ff02::2         ip6-allrouters

127.0.1.1       raspberrypi
125.209.200.159 server




pkill chromium
cd ~/.config/chromium/
rm -f SingletonLock
rm -f SingletonSocket
sudo reboot

```


#### pkill chromium:

- pkill 명령은 주어진 프로세스 이름을 기반으로 해당 프로세스를 종료합니다.
chromium은 Chromium 브라우저의 실행 파일 이름입니다. 이 명령은 Chromium 브라우저와 관련된 모든 프로세스를 종료합니다.

#### cd ~/.config/chromium/:

- cd 명령은 "change directory"의 약어로, 현재 작업 디렉터리를 변경하는 명령입니다.
~/.config/chromium/은 Chromium 브라우저의 사용자 설정 및 상태 파일들이 저장된 디렉터리입니다. 이 디렉터리로 이동하여 Chromium과 관련된 설정 파일들을 조작할 수 있습니다.

#### rm -f SingletonLock:

- rm 명령은 파일을 삭제하는 명령입니다.
- f 옵션은 "force"로, 파일이 존재하지 않아도 오류를 발생시키지 않고 강제로 삭제합니다.
SingletonLock 파일은 Chromium이 실행 중일 때 다른 Chromium 인스턴스가 실행되지 않도록 잠금을 거는 파일입니다. 이 파일을 삭제하면, 잠금이 해제되어 새로운 Chromium 인스턴스가 실행될 수 있습니다.

#### rm -f SingletonSocket:

- SingletonSocket도 Chromium이 실행 중일 때 사용하는 소켓 파일입니다. 이 파일은 Chromium이 여러 인스턴스에서 충돌하지 않도록 합니다.
이 파일을 삭제함으로써, Chromium이 새로운 인스턴스를 시작할 수 있도록 만듭니다.

#### sudo reboot:

- sudo는 시스템 관리자 권한으로 명령을 실행할 수 있게 해주는 명령어입니다.
- reboot는 시스템을 재부팅하는 명령입니다. 이 명령을 실행하면 시스템이 다시 시작됩니다.

#### 요약:

이 일련의 명령은 Chromium 브라우저를 종료한 후, 잠금 파일(SingletonLock, SingletonSocket)을 삭제하여 Chromium이 새로운 인스턴스를 시작할 수 있도록 하고, 마지막으로 시스템을 재부팅하여 변경 사항이 적용되도록 합니다. 이 작업은 주로 Chromium에서 충돌이나 잠금 문제가 발생했을 때 문제를 해결하기 위해 사용됩니다.




