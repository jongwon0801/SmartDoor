# raspberry pi ip 알아 내는 법 3가지

### 1. 라우터의 관리 페이지에서 라즈베리 파이의 할당된 IP 주소를 확인
```bash
wikibox 192.168.0.1
wikibox  /  wiki0800**

wikibox_lab 192.168.1.1
wikibox  /  tmshdnxmfl
```
![Uploading image.png…]()


### 2. 
# 라즈베리 파이가 네트워크에 연결된 경우, 다른 장치에서 라즈베리 파이를 raspberrypi.local로 핑 테스트를 하면 IP를 알 수 있습니다.
```bash
ping raspberrypi.local

```
### 3. 직접 장치에 모니터 연결해서 터미널 열고 ifconfig 명령어



# 키오스크 서버에서 장치 사양 검토

### 키오스크 서버 ssh 접속
```bash
ssh pi@192.168.0.161 / elcsoft
```
### 운영체제 버젼 확인
```bash
cat /etc/os-release
```
```bash
PRETTY_NAME="Debian GNU/Linux 11 (bullseye)"
NAME="Debian GNU/Linux"
VERSION_ID="11"
VERSION="11 (bullseye)"
VERSION_CODENAME=bullseye
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"
```
```bash
lsb_release -a
```
```bash
Distributor ID:	Debian
Description:	Debian GNU/Linux 11 (bullseye)
Release:	11
Codename:	bullseye
```
### 라즈베리 파이 모델을 확인
```bash
cat /proc/cpuinfo
```
```bash
Model		: Raspberry Pi 4 Model B Rev 1.4
```

---

# OS 설치

## Raspberry Pi Imager를 사용하여 Raspberry Pi OS 설치 
<br>
https://www.raspberrypi.com/software/

### Imager 다운 -> raspberry Pi 4 (디바이스) / raspberry Pi OS Bullseye(Legacy, 32-bit) (운영체제) / 저장소 (bootfs) 설치 

<img width="652" alt="image" src="https://github.com/user-attachments/assets/b8738cc2-e4a0-41f9-897f-7599ca578b7e">







