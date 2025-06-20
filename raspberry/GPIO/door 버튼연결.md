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
        os.system("sudo /sbin/shutdown now")
    else:
        logger.Logger._LOGGER.info("🟡 시스템 재부팅 요청됨 (짧게 버튼 누름)")
        os.system("sudo /sbin/reboot")

def initialize_button():
    try:
        button.setup_button(on_button_pressed)
        logger.Logger._LOGGER.info("✅ 버튼 이벤트 기반 초기화 완료")
    except Exception as e:
        logger.Logger._LOGGER.error(f"❌ 버튼 초기화 실패: {e}")

def cleanup_button():
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



