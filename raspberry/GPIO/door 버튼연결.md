#### __init__ 제일 하단에 추가

```less
def __init__(self, *args, **kwargs):

# 버튼 초기화
self.initialize_button()
logger.Logger._LOGGER.info("버튼 초기화 완료")
```


#### wikismartdoor.py
```less
import time
import os
import button
import logger
import RPi.GPIO as GPIO  # 버튼 핀 상태 직접 확인용

def on_button_pressed(self, channel):
    logger.Logger._LOGGER.info("🟢 버튼 눌림 감지됨")
    start_time = time.time()

    while GPIO.input(channel) == GPIO.LOW:
        time.sleep(0.1)

    press_duration = time.time() - start_time
    logger.Logger._LOGGER.info(f"버튼 누름 지속 시간: {press_duration:.2f}초")

    if press_duration >= 3:
        logger.Logger._LOGGER.info("🔴 시스템 종료 요청됨 (3초 이상 버튼 누름)")
        os.system("sudo /sbin/shutdown now")
    else:
        logger.Logger._LOGGER.info("🟡 시스템 재부팅 요청됨 (짧게 버튼 누름)")
        os.system("sudo /sbin/reboot")


def initialize_button(self):
    try:
        button.setup_button(self.on_button_pressed)  # ✅ 수정된 부분
        logger.Logger._LOGGER.info("✅ 버튼 이벤트 기반 초기화 완료")
    except Exception as e:
        logger.Logger._LOGGER.error(f"❌ 버튼 초기화 실패: {e}")


def cleanup_button(self):
    try:
        button.cleanup()
        logger.Logger._LOGGER.info("🧹 GPIO 정리 완료 및 프로그램 종료")
    except Exception as e:
        logger.Logger._LOGGER.error(f"❌ GPIO 정리 중 오류 발생: {e}")
```


#### button.py
```less
import RPi.GPIO as GPIO

BUTTON_PIN = 24  # 또는 23 (BCM 기준)

def setup_button(callback):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # 버튼 눌림 시 falling edge 이벤트 등록 (채터링 방지 bouncetime)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=callback, bouncetime=300)
    print(f"[GPIO] 버튼 이벤트 등록 완료 (PIN {BUTTON_PIN})")

def cleanup():
    GPIO.cleanup()
    print("🧹 GPIO 정리 완료")
```

#### 유저 단위 서비스 실행 시 오류
```less
유저 단위 systemd 서비스로 Tornado 웹서버를 실행 중이면서,
버튼으로 os.system("sudo reboot") / shutdown이 안 되는 이유는
➡ pi 유저는 기본적으로 sudo 비밀번호 없이 reboot 권한이 없기 때문입니다.
```


#### sudo 없이도 reboot 가능하게 설정
```less
1단계. sudoers 파일 편집

sudo visudo

# pi 유저가 비밀번호 없이 shutdown, reboot 명령을 실행할 수 있도록 허용
pi ALL=(ALL) NOPASSWD: /sbin/shutdown, /sbin/reboot
```


#### 2단계. 코드에서 정확한 명령 사용
```less
os.system("sudo /sbin/reboot")

os.system("sudo /sbin/shutdown now")
```



