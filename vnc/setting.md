### 방화벽 설정 확인


### macOS: "시스템 설정 > 보안 및 개인정보 보호 > 손쉬운 사용 > vnc viewer 권한 부여
<img width="475" alt="image" src="https://github.com/user-attachments/assets/9cef4b98-4170-4e64-a67a-0650e7f00403" />

**1. VNC 서버 설치 여부 확인**

SSH로 라즈베리 파이에 접속하여 VNC 서버가 설치되었는지 확인하려면 아래 명령어를 사용하세요.

```bash
dpkg -l | grep realvnc
```

**2. SSH로 라즈베리 파이에 접속한 후, VNC 서버가 활성화되어 있는지 확인**

```bash
ssh pi@192.168.0.50

sudo raspi-config

#Interface Options → VNC를 선택하고 Enable합니다

#VNC 서버 서비스가 제대로 실행 중인지 확인
sudo systemctl status vncserver-x11-serviced.service
```
<img width="253" alt="image" src="https://github.com/user-attachments/assets/d767de0b-f65a-49f8-b6d5-0f49c188c1eb" />

**3. VNC Viewer 에서 라즈베리 접속

raspberry 4 : 192.168.0.50<br>
username : pi<br>
passwd   : pi<br>

kiosk 서버 : 192.168.0.161<br>
username : pi<br>
passwd   : elcsoft<br>









