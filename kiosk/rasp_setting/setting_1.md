#### ssh 설정
```bash
sudo raspi-config

Interface Options → SSH (yes 설정)

sudo systemctl status ssh
```


#### ssh 접속 이전 기록 삭제

```bash
nano /Users/jongwon/.ssh/known_hosts

```

#### 버젼 확인

```bash
"System Options" -> "Boot / Auto Login"  ->  "Desktop" 항목이 보이면 데스크탑 버전이 설치된 것입니다.


# 출력값이 armv7l이면 32비트, aarch64이면 64비트
uname -m

cat /etc/os-release

```
#### ibus 한글 입력기 설치

- 출력: 한글 출력은 폰트와 로케일 설정에 의해 결정됩니다. (따라서 IBus 없이도 가능)
- 입력: 한글 입력은 키보드 입력기(예: IBus, Fcitx 등)가 있어야 가능합니다.

<img width="329" alt="image" src="https://github.com/user-attachments/assets/d0ad6884-1d62-4ad6-a297-9646566a5065" />

```bash
sudo apt update

sudo apt install ibus ibus-hangul ibus-gtk3

ibus-daemon -drx

#설치되어 있는지 확인
dpkg -l | grep ibus

#실행 중인지 확인
ps aux | grep ibus


```
- ibus: IBus 입력기 기본 패키지
- ibus-hangul: 한글 입력을 위한 IBus 엔진
- ibus-gtk3: GTK3 기반의 IBus 지원

#### 터치 스크린 설정
```bash

sudo apt update
sudo apt full-upgrade


nano /usr/share/X11/xorg.conf.d/40-libinput.conf 

sudo systemctl restart lightdm

```


#### 해상도 설정

```bash

# 모니터가 자동으로 감지되지 않을 때 HDMI 출력이 항상 활성화되므로, 모니터나 TV가 HDMI 신호를 제대로 인식
# 모니터 없이 원격으로 Raspberry Pi를 설정할 때 외부 모니터 화면을 확인 가능
hdmi_force_hotplug=1

#HDMI 장치(모니터, TV 등)에서 비디오와 오디오를 모두 출력하고자 할 때 사용
hdmi_drive=2

```






