### 키오스크 실행 테스트
```bash
1. 네트워크 문제 확인

로그인 후 네트워크 연결이 제대로 이루어지지 않으면 일부 서비스가 실패할 수 있습니다.

ping google.com

2. X11 세션 문제

Raspberry Pi가 부팅 시 X11 세션을 시작하는데, 그 과정에서 문제가 발생했을 수 있습니다.
logout이 표시되는 이유는 X 세션이 제대로 시작되지 않았거나 세션 충돌이 발생했기 때문일 수 있습니다.

cat /var/log/Xorg.0.log


3. autostart 설정 오류

# autostart 설정이 잘못되었거나, chromium-browser가 제대로 실행되지 않았을 수 있습니다.

cat ~/.xsession-errors

4. 로그인 후 자동화 문제

만약 자동으로 chromium을 띄우려고 했지만, chromium이나 다른 서비스가 충돌하여 로그아웃되는 경우일 수 있습니다.
tornado 서비스가 제대로 시작되지 않았거나, 다른 프로세스가 충돌할 수 있습니다.

sudo journalctl -u tornado.service

5. 디스플레이 매니저 관련 문제

Raspberry Pi의 디스플레이 매니저나 세션 관리자가 제대로 작동하지 않으면 이런 문제가 발생

sudo systemctl status lightdm
sudo systemctl status lxsession


6. 크롬 브라우저 실행 문제

크롬 브라우저가 설치되었으나 제대로 실행되지 않는 경우
chromium-browser 명령어를 터미널에서 직접 실행해보면 오류 메시지 나타남

chromium-browser --kiosk http://127.0.0.1

```
