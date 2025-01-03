#### display 표출 에러

```bash

sudo cat /var/log/lightdm/x-0.log

# 패키지 재설치
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install --reinstall xserver-xorg
sudo apt-get install --reinstall raspberrypi-ui-mods


# nano ~/.bashrc 통일
export WORKON_HOME=$HOME/.virtualenvs
#source /home/pi/bin/virtualenvwrapper.sh


# nano ~/.profile 참조 위치는 다른데 파일 내용은 똑같음
원래서버 하단
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
만든서버 하단
source /home/pi/.local/bin/virtualenvwrapper.sh

# 환경 변수를 설정
export XDG_RUNTIME_DIR=/run/user/$(id -u)

# lightdm 또는 X 서버를 재시작
sudo systemctl restart lightdm

# 환경변수 확인
echo $XDG_RUNTIME_DIR








```
















