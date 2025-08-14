#### 불꽃 센서 테스트 모듈

```less
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

FLAME_PIN = 17  # 불꽃 센서 GPIO 번호

# 입력 설정, 풀업으로 안정화 (불꽃 감지 시 LOW)
GPIO.setup(FLAME_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        if GPIO.input(FLAME_PIN) == GPIO.LOW:  # 불꽃 감지 시 LOW 출력
            print("🔥 불꽃 감지!")
        else:
            print("안전")
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()

```


#### 출력논리 확인방법()
```less
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
FLAME_PIN = 17
GPIO.setup(FLAME_PIN, GPIO.IN)

try:
    while True:
        print("FLAME_PIN 상태:", GPIO.input(FLAME_PIN))
        time.sleep(0.2)
except KeyboardInterrupt:
    GPIO.cleanup()
```
```less
평상시: HIGH (1)

불꽃 감지 시: LOW (0)

이 경우 PUD_UP을 써도 되고, 감지 조건을 GPIO.LOW로 쓰면 됩니다.
```














