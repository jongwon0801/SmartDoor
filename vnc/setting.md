### 방화벽 설정 확인


### macOS: "시스템 설정 > 보안 및 개인정보 보호 > 손쉬운 사용 > vnc viewer 권한 부여
<img width="475" alt="image" src="https://github.com/user-attachments/assets/9cef4b98-4170-4e64-a67a-0650e7f00403" />

** 1. VNC 서버 설치 여부 확인 **
SSH로 라즈베리 파이에 접속하여 VNC 서버가 설치되었는지 확인:



dpkg -l | grep realvnc
