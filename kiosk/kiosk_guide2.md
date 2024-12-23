### 가상환경 활성화
```bash
source /home/pi/.virtualenvs/elcsoft/bin/activate

# 가상환경 비활성화
deactivate

# (elcsoft) pi@raspberrypi:~ $
```

### kiosk 서버에서 버젼 txt 파일생성
```bash
pip freeze > requirements1.txt


```

### package 설치 requirement.txt kiosk에 설치된거
```bash
pip install requests

pip install pillow

cd ~/www/python/
pip install -r requirements.txt


# 캐시삭제
pip cache purge

```








