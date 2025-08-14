#### 1. GPIO 신호와 센서 동작
```less
| 항목                      | 설명                                       |
| ----------------------- | ---------------------------------------- |
| **GPIO 입력**             | HIGH / LOW 상태에 따라 이벤트 처리 (예: `print` 출력) |
| **Relay / 장치 동작**       | GPIO HIGH / LOW 상태로 장치 ON/OFF 제어         |
| **PULL UP / PULL DOWN** | 입력 핀 기본 상태 안정화용 (floating 방지)            |
| **상시 폐쇄형 센서**           | 평상시 LOW → 이벤트 시 HIGH (RISING 감지)         |
| **상시 개방형 센서**           | 평상시 HIGH → 이벤트 시 LOW (FALLING 감지)        |
```

#### 2. GPIO 핀 상태 관련
```less
GPIO HIGH/LOW → Value 판단

Command / 상태 확인: 프로그램에서 GPIO 상태 읽어 이벤트 처리

BCM 번호 기준 사용 → 코드에서 GPIO.setmode(GPIO.BCM)
```

#### 3. 센서 핀 구성 및 연결
```less
| 센서 핀                    | 라즈베리파이 연결                               |
| ----------------------- | --------------------------------------- |
| **VCC**                 | 5V 또는 3.3V (센서 전원)                      |
| **GND**                 | GND (접지)                                |
| **DO (Digital Output)** | GPIO 입력 (HIGH/LOW로 상태 감지)               |
| **TX / RX (Serial)**    | 센서 UART 통신 시 연결 (VCC/GND + TX/RX 교차 연결) |
```
```less
DO 핀 → HIGH/LOW 신호로 이벤트 감지

TX/RX → UART 통신 시 사용 (Serial 센서)
```

#### 4. 이벤트 감지 요약
```less
| 센서 타입  | 평상시  | 이벤트  | GPIO 조건     |
| ------ | ---- | ---- | ----------- |
| 상시 폐쇄형 | LOW  | HIGH | RISING 이벤트  |
| 상시 개방형 | HIGH | LOW  | FALLING 이벤트 |
```
```less
풀업(PUD_UP) → 기본 HIGH

풀다운(PUD_DOWN) → 기본 LOW

💡 정리:
풀업은 “기본 HIGH, 신호 연결 시 LOW”가 맞습니다. 풀다운은 “기본 LOW, 신호 연결 시 HIGH”입니다.

센서가 OFF일 때 HIGH인 상태를 유지하고 싶으면 풀업,
OFF일 때 LOW로 유지하고 싶으면 풀다운을 사용하면 됩니다.
```

#### 정리
```less
GPIO 상태(HIGH/LOW) → 이벤트/동작

풀업/풀다운으로 기본 상태 안정화

센서 핀 배선: VCC/GND/DO(TX/RX) → 라즈베리파이 GPIO 연결
```









