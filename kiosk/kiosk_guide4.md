### firebase_admin 모듈 설치

```bash
pip3 install firebase-admin

```

### python webserver.py 실행하면서 필요 모듈 설치

- cd /home/pi/www/python
- python webserver.py

```bash
pip install qrcode

pip install opencv-python

pip install pyzbar

pip install PyMySQL

pip install DBUtils

pip install websockets

pip install face-recognition

pip install gTTS

pip install pydub

pip install nmcli

pip install RPi.GPIO

pip install gpiozero

pip install python-vlc

pip install lgpio

## 이후 기기 없어서 에러

nano ~/www/python/pir_outside.py -> pir_outside_fix.py

nano /home/pi/www/python/elcsoft/controller/smartdoor.py -> smartdoor_fix.py

sudo lsof -i :8080 포트 충돌시 확인 후 강제종료
sudo kill 1107 / nano webserver.py -> app.listen(8080) 포트 변경

```

### wikismartdoor.py 파일에서 syncDataAll() 메소드 내의 syncProcess 호출을 제거
<img width="485" alt="image" src="https://github.com/user-attachments/assets/63327ff3-38b3-4e53-bb03-09072a7fdc07" />

<img width="566" alt="image" src="https://github.com/user-attachments/assets/d2054597-2d6c-497d-9502-840a6b6e2ba6" />


















