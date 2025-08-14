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


#### 1. 출력논리 코드로 확인하는 방법
```less
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
FLAME_PIN = 17
GPIO.setup(FLAME_PIN, GPIO.IN)  # 풀업/풀다운 설정 없이

try:
    while True:
        print(GPIO.input(FLAME_PIN))
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()

```

#### 요약
```less
평상시 값이 1(HIGH) 이면 → 센서가 기본적으로 풀업(상시 HIGH)
-> 감지 조건을 GPIO.LOW

평상시 값이 0(LOW) 이면 → 센서가 기본적으로 풀다운(상시 LOW)
-> 감지 조건을 GPIO.HIGH
```

#### 2. 센서 모듈 구조로 확인하는 방법
```less
불꽃센서 모듈에 보통 3핀(VCC, GND, DO) 또는 4핀(아날로그 + 디지털) 출력이 있습니다.

내부에 풀업 저항이 있으면 기본 출력이 HIGH로 유지됩니다.

내부에 풀다운 저항이 있으면 기본 출력이 LOW로 유지됩니다.
```

#### 3. 멀티미터
```less
멀티미터로 DO 핀과 GND 사이 전압을 재보면 더 확실합니다.

평상시 3.3V나 5V → 풀업 방식

평상시 0V → 풀다운 방식
```













