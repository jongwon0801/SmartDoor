#### 라즈베리파이 os imager 로 설치

라즈베리4 모델 b / 64bit bullseye desktop 버젼

```bash

# pi@192.168.0.161 / elcsoft 에서 os 버전 확인

if dpkg -l | grep -E 'libreoffice|wolfram' > /dev/null; then
    echo "Desktop Environment with Recommended Applications (Full version)"
else
    echo "Standard Desktop Environment (without Recommended Applications)"
fi
```

- Full 버전에는 libreoffice 및 wolfram 패키지가 포함되지만, 해당 패키지가 설치되어 있지 않으므로 Full 버전이 아닙니다.
- 현재 Raspberry Pi OS는 기본 데스크톱 환경만 포함된 Standard Desktop 버전입니다.

#### ssh 설정(raspberrypi)
```bash
sudo raspi-config

Interface Options → SSH (yes 설정)

sudo systemctl status ssh
```


#### ssh 접속 이전 기록 삭제(mac)

```bash
sudo nano /Users/jongwon/.ssh/known_hosts

```

#### 버젼 확인

```bash
"System Options" -> "Boot / Auto Login"  ->  "Desktop" 항목이 보이면 데스크탑 버전이 설치된 것입니다.


# 출력값이 armv7l이면 32비트, aarch64이면 64비트
uname -m

cat /etc/os-release

```


#### 전체 프로그램 업데이트

```bash
sudo apt clean
sudo apt autoremove -y

sudo apt update
sudo apt upgrade
```

#### 1 ibus 한글 입력기 설치

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

# 한글 글꼴 깨짐 위해 폰트 설치(install 해야함 글꼴 복사로 안됨)
sudo apt install fonts-nanum fonts-unfonts-core


```
- ibus: IBus 입력기 기본 패키지
- ibus-hangul: 한글 입력을 위한 IBus 엔진
- ibus-gtk3: GTK3 기반의 IBus 지원




#### 2 터치 스크린 설정
```bash

sudo apt update
sudo apt full-upgrade


sudo nano /usr/share/X11/xorg.conf.d/40-libinput.conf 

sudo systemctl restart lightdm

Section "InputClass"
        Identifier "libinput touchscreen catchall"
        MatchIsTouchscreen "on"
        #Option "TransformationMatrix" "0 -1 1 1 0 0 0 0 1"
        Option "TransformationMatrix" "0 1 0 -1 0 1 0 0 1"
        MatchDevicePath "/dev/input/event*"
        Driver "libinput"
EndSection

```

#### 기본 형식
- 2D 변환 행렬은 다음과 같은 일반적인 구조를 가집니다

<img width="100" alt="image" src="https://github.com/user-attachments/assets/9cf61950-9ecb-480c-9f63-f5f616c16f14" />

- [a, b]: X 축과 관련된 변환 (회전, 스케일, 기울임 등).
- [d, e]: Y 축과 관련된 변환 (회전, 스케일, 기울임 등).
- [c, f]: X, Y 축의 이동(translation)을 나타냅니다.
- [g, h, i]: 일반적으로 2D 공간에서는 고정된 값(0, 0, 1).


<img width="507" alt="image" src="https://github.com/user-attachments/assets/cdd82400-964f-4d7c-9204-300a9ce8a54f" />

<img width="698" alt="image" src="https://github.com/user-attachments/assets/b183f69c-17b7-4ab9-b45f-686f002b45be" />

### 반시계 회전 공식

<img width="713" alt="image" src="https://github.com/user-attachments/assets/77147e41-ab84-448a-9bdb-cf7e71839406" />



#### 3 해상도 설정

```bash
# 들어가서 아래 두개 주석해제
sudo nano /boot/config.txt

# 모니터가 자동으로 감지되지 않을 때 HDMI 출력이 항상 활성화되므로, 모니터나 TV가 HDMI 신호를 제대로 인식
# 모니터 없이 원격으로 Raspberry Pi를 설정할 때 외부 모니터 화면을 확인 가능
hdmi_force_hotplug=1

#HDMI 장치(모니터, TV 등)에서 비디오와 오디오를 모두 출력하고자 할 때 사용
hdmi_drive=2

[all]
gpu_mem=128

#enable_uart=1
#dtoverlay=uart0
#dtoverlay=uart1
#dtoverlay=uart2
#dtoverlay=uart3
#dtoverlay=uart4
#dtoverlay=uart5

```
#### 네트워크 관리방법 변경 (이거 하면 ssh 끊김)

```bash

sudo raspi-config

Advanced Options -> Network Config -> NetworkManager


관리 범위: dhcpcd는 기본적으로 IP 주소 할당과 네트워크 인터페이스의 설정을 관리하는 반면,
NetworkManager는 여러 종류의 네트워크 인터페이스(Wi-Fi, 유선, VPN 등)를 포괄적으로 관리하는 데 사용됩니다



```
