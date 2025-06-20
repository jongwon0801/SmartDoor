#### RPI4 (블루)에서 단일 테스트
```less
import RPi.GPIO as GPIO
import time
import os

# GPIO 핀 번호 설정 (예: BCM 기준 GPIO17 -> 핀번호 11번)
BUTTON_PIN = 17

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def shutdown():
    print("Shutting down...")
    os.system("sudo shutdown now")

def reboot():
    print("Rebooting...")
    os.system("sudo reboot")

try:
    while True:
        # 버튼이 눌리면 (LOW 신호 감지)
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Button pressed")
            start_time = time.time()
            
            # 버튼이 다시 HIGH로 올라올 때까지 대기
            while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                time.sleep(0.1)
            
            press_duration = time.time() - start_time
            print(f"Pressed for {press_duration:.2f} seconds")

            if press_duration >= 3:
                shutdown()
            else:
                reboot()

        time.sleep(0.1)

except KeyboardInterrupt:
    print("종료")

finally:
    GPIO.cleanup()

```
#### 192.168.0.42 단일 테스트
```less
# test_button.py

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        val = GPIO.input(24)
        print("버튼 상태:", "눌림 (LOW)" if val == GPIO.LOW else "안눌림 (HIGH)")
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
```

#### ⚙️ 배선 가이드
```less
GPIO17 (핀 11) — 스위치 한쪽

GND — 스위치 다른 쪽

내부 풀업 설정(pull_up_down=GPIO.PUD_UP)으로 외부 저항 불필요

버튼 누르면 GPIO 핀이 LOW로 떨어짐
```

❗주의사항
```less
반드시 sudo로 실행해야 합니다 (os.system("sudo reboot") 등은 루트 권한 필요).

shutdown 또는 reboot 실행 전에 충분히 로그를 찍거나 LED 등으로 사용자 피드백을 주는 것이 좋습니다.

파이썬 실행 시 KeyboardInterrupt로 정상 종료 가능하게 처리되어 있습니다.
```

✅ 푸시버튼 모듈 핀 설명

| 핀 이름    | 기능                                     |
| ------- | -------------------------------------- |
| **VCC** | 전원 공급 (보통 3.3V 또는 5V)                  |
| **GND** | 그라운드                                   |
| **OUT** | 버튼 입력 신호 출력 (눌렀을 때 LOW 또는 HIGH 신호 출력됨) |

대부분 이 모듈은 내부 풀업 저항이 있어서, 버튼을 누르면 OUT이 LOW로 떨어지고, 떼면 HIGH 상태입니다.


✅ 라즈베리파이 연결 방법 (예: GPIO17 사용 시)

| 푸시버튼 핀  | 라즈베리파이 연결 핀 (핀 번호 / 기능)                                 |
| ------- | ------------------------------------------------------- |
| **VCC** | 1번 핀 (3.3V) 또는 2번 핀 (5V)<br>➡︎ 보통 **3.3V (1번 핀)** 사용 권장 |
| **GND** | 6번, 9번, 14번 등 아무 GND 핀                                  |
| **OUT** | 예: **11번 핀 (GPIO17)**                                   |

```less
푸시버튼 모듈 → 라즈베리파이

VCC           →   3.3V (핀 1번)
GND           →   GND (핀 6번)
OUT           →   GPIO17 (핀 11번)
```

#### 🔧 핀번호 참고 (일부)

| 핀번호 | 기능     | 설명                  |
| --- | ------ | ------------------- |
| 1   | 3.3V   | VCC용 전원             |
| 2   | 5V     | 고전압 전원 (일부 센서에만 사용) |
| 6   | GND    | 그라운드                |
| 11  | GPIO17 | 일반 입력 핀             |

#### 🔎 확인 팁
```less
모듈이 버튼을 누르면 OUT이 LOW로 떨어지는 타입인지, 아니면 HIGH로 올라가는 타입인지 멀티미터나 LED로 확인해도 좋습니다.

보통은 pull-up 되어 있어서 누르면 LOW 신호를 출력합니다. (→ 코드에서 GPIO.PUD_UP을 설정)
```

#### gpio 패키지설치
```less
sudo apt update
sudo apt install python3-rpi.gpio
```

#### 로그 파일로 남기고 싶다면
```less
# 실행 시 로그를 파일로 저장
sudo python3 my_script.py > /home/pi/mylog.txt 2>&1
```

#### script 내부에 남기기
```less
import logging

# 로그 설정
logging.basicConfig(filename='/home/pi/button_log.txt',
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# 사용 예시
logging.info("Button pressed")
```





