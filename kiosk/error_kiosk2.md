### X11 서버, chromium-browser 실행 테스트

```bash

1. X11 서버 확인

X11 서버가 제대로 실행되고 있는지 확인.
X11 서버가 실행되고 있지 않으면, 크롬 브라우저를 실행할 수 없습니다. Raspberry Pi에서 GUI 환경이 실행되고 있는지 확인해보세요.
ps aux | grep Xorg


2. $DISPLAY 환경 변수 설정
chromium-browser는 $DISPLAY 환경 변수를 통해 X11 서버와 연결됩니다.
$DISPLAY가 제대로 설정되지 않은 경우, chromium이 실행되지 않습니다. $DISPLAY를 수동으로 설정해볼 수 있습니다.

export DISPLAY=:0
chromium-browser --kiosk http://127.0.0.1

3. 부팅 시 X11 세션을 정상적으로 시작
Raspberry Pi가 부팅 시 X11 세션을 제대로 시작하지 않는 문제일 수 있습니다.
autostart 설정이 잘못된 경우나, 디스플레이 매니저가 제대로 작동하지 않으면 이러한 문제가 발생할 수 있습니다.

sudo systemctl status lightdm

lightdm 서비스가 실행되지 않는다면, 이를 다시 시작하거나 startx 명령어로 수동으로 X11 서버를 시작할 수 있습니다.

sudo systemctl start lightdm

4. ~/.xsession-errors 로그 확인

GUI 세션에 문제가 있을 수 있으므로, ~/.xsession-errors 로그 파일에서 문제의 원인을 찾을 수 있습니다.
 이 파일에 오류나 경고가 기록되어 있을 수 있습니다.

cat ~/.xsession-errors


5. 디스플레이 매니저 재설정

Raspberry Pi에서 GUI 환경이 정상적으로 시작되지 않으면, 디스플레이 매니저나 세션 관련 설정에 문제가 있을 수 있습니다.
lightdm이나 lxsession이 제대로 시작되지 않았을 수 있으니, 이를 재설정하거나 확인해보세요.

sudo systemctl restart lightdm



```
