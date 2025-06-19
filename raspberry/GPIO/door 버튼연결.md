#### # wikismartdoor.py
```less
# wikismartdoor.py
import time
import os
import button
import logger
import RPi.GPIO as GPIO  # 버튼 핀 상태 직접 확인용

def on_button_pressed(channel):
    logger.Logger._LOGGER.info("🟢 버튼 눌림 감지됨")
    start_time = time.time()

    # 버튼이 눌린 상태 유지되는 동안 대기
    while GPIO.input(channel) == GPIO.LOW:
        time.sleep(0.1)

    press_duration = time.time() - start_time
    logger.Logger._LOGGER.info(f"버튼 누름 지속 시간: {press_duration:.2f}초")

    if press_duration >= 3:
        logger.Logger._LOGGER.info("🔴 시스템 종료 요청됨 (3초 이상 버튼 누름)")
        os.system("sudo shutdown now")
    else:
        logger.Logger._LOGGER.info("🟡 시스템 재부팅 요청됨 (짧게 버튼 누름)")
        os.system("sudo reboot")

try:
    button.setup_button(on_button_pressed)
    logger.Logger._LOGGER.info("✅ 버튼 이벤트 기반 초기화 완료")

    # 루프는 아무 일도 안 하지만 계속 살아 있어야 인터럽트 유지됨
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    logger.Logger._LOGGER.info("⛔ 프로그램 종료됨 (KeyboardInterrupt)")

finally:
    button.cleanup()
    logger.Logger._LOGGER.info("🧹 GPIO 정리 완료 및 프로그램 종료")
```


#### button.py
```less
# button.py
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




