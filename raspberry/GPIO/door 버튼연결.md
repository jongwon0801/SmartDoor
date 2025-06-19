#### wikismartdoor.py tornado 이벤트 루프에 등록
```less
# 백그라운드로 계속 실행할 것들
    def run(self):
        # 네트워크 연결이 안되면 웹소켓으로 네트워크 연결 요청
        if not network.isInternet():
            msg = {"request": "setupWifi", "data": network.getWifies()}
            self.sendWebsocket(msg)
        else:
            self.syncDataAll()
        # threading.Thread(target=self.syncDataAll, daemon=True).start()
        threading.Thread(target=self.mqtt.run, daemon=True).start()
        threading.Thread(target=self.polling, daemon=True).start()
        threading.Thread(target=self.pir_inside.run, daemon=True).start()
        threading.Thread(target=self.pir_outside.run, daemon=True).start()

        # 버튼 초기화
        self.initialize_button()
```

#### wikismartdoor.py
```less
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

def initialize_button():
    button.setup_button(on_button_pressed)
    logger.Logger._LOGGER.info("✅ 버튼 이벤트 기반 초기화 완료")

def cleanup_button():
    button.cleanup()
    logger.Logger._LOGGER.info("🧹 GPIO 정리 완료 및 프로그램 종료")

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




