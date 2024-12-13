### 라즈베리 기기랑 같은 와이파이에 접속
```bash
wikibox/tmshdnxmfl
```
### 라즈베리 기기로 원격 접속
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

## Raspberry Pi Imager를 사용하여 Raspberry Pi OS 설치 
<br>
https://www.raspberrypi.com/software/

### Imager 다운 -> raspberry Pi 4 (디바이스) / raspberry Pi OS Bullseye(Legacy, 32-bit) (운영체제) / 저장소 (bootfs) 설치 

<img width="652" alt="image" src="https://github.com/user-attachments/assets/b8738cc2-e4a0-41f9-897f-7599ca578b7e">
