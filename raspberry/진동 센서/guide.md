#### 핀 번호
```less
[진동 센서]     [라즈베리파이]
VCC  -------->  5V (2번)
GND  -------->  GND (6번)
DO   -------->  GPIO17
```

#### RPi.GPIO 라이브러리가 설치
```less
sudo apt update
sudo apt install python3-rpi.gpio

# 설치 확인
python3 -c "import RPi.GPIO as GPIO; print(GPIO.VERSION)"

# pip 가상환경 안에 설치
pip install RPi.GPIO
```

#### 상시 폐쇄형 센서 특성
```less
평상시: 회로 닫힘 → DO 핀 LOW

진동 발생: 회로 열림 → DO 핀 HIGH
```

#### GPIO.IN
```less
GPIO.IN은 Raspberry Pi에서 GPIO 핀을 입력(input)으로 사용하겠다는 의미입니다.

Raspberry Pi의 GPIO 핀은 크게 두 가지 용도로 사용할 수 있어요:

입력 (Input) – 센서, 버튼 등 외부 신호를 읽을 때

출력 (Output) – LED, 모터 등 외부 장치를 제어할 때
```

#### 1. 풀업/풀다운이 필요한 이유
```less
GPIO 입력핀은 전기적으로 부동(floating) 상태가 될 수 있음

센서가 연결되지 않았거나 회로가 열려있을 때
→ GPIO가 LOW인지 HIGH인지 알 수 없는 상태
→ 잡음 때문에 계속 값이 튀거나 진동 감지처럼 잘못 읽힘
```


#### 2. 풀업(PULL UP) vs 풀다운(PULL DOWN)

```less
| 설정                                | 의미                                |
| --------------------------------- | --------------------------------- |
| **PUD\_UP**                       | 평상시 HIGH → 센서가 LOW로 바뀌면 감지할 수도 있음 |
| **PUD\_DOWN**                     | 평상시 LOW → 센서가 HIGH로 바뀌면 감지 가능     |
| **코드의 if GPIO.input()==HIGH/LOW** | 이벤트를 언제 감지할지 선택하는 조건              |

```

#### 비교
```less
| 센서 타입  | 평상시 상태 | 이벤트 상태 | 권장 설정     |
| ------ | ------ | ------ | --------- |
| 상시 개방형 | HIGH   | LOW    | PUD\_DOWN |
| 상시 폐쇄형 | LOW    | HIGH   | PUD\_UP   |
```

#### 3. 꼭 써야 하나?
```less
센서가 외부에서 이미 명확하게 HIGH/LOW를 출력하면 필수는 아님

하지만 대부분 잡음 방지 및 안정성 때문에 쓰는 게 권장됨
```
#### 모듈 테스트
```less
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

VIB_PIN = 17  # 진동 센서

# 입력 설정, 풀다운으로 안정화
GPIO.setup(VIB_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        if GPIO.input(VIB_PIN) == GPIO.HIGH:  # 진동 발생 시
            print("진동 감지!")
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()

```

#### 스마트도어에 삽일 할때 참고
```less
import RPi.GPIO as GPIO
import time

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)

VIB_PIN = 17  # 진동 센서 DO 핀

# 입력 핀 설정, 풀업 사용 (평상시 LOW → HIGH 변화 감지)
GPIO.setup(VIB_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 이벤트 콜백 함수
def vib_detected(channel):
    print("진동 감지!")

# RISING 이벤트 감지 (LOW → HIGH)
GPIO.add_event_detect(VIB_PIN, GPIO.RISING, callback=vib_detected, bouncetime=200)

try:
    print("센서 모니터링 시작...")
    while True:
        time.sleep(1)  # CPU 부담 줄이기

except KeyboardInterrupt:
    GPIO.cleanup()
    print("종료")
```



