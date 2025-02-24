/home/pi/www/shell/screen.sh

#!/usr/bin/env bash
echo "$1"
export DISPLAY=:0.0
#export XDG_RUNTIME_DIR=/var/run/user/1000
xset -display $DISPLAY dpms force $1
#if [ "$1" = "off" ]
#then
#       /home/pi/.virtualenvs/elcsoft/bin/python /home/pi/www/python/msgbox.py websocket -msg '{"request":"sendKiosk","response":"screenOff"}'
#fi
