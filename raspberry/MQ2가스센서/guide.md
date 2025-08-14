#### 핀 설명
```less
| 핀                       | 용도                                          |
| ----------------------- | ------------------------------------------- |
| **VCC**                 | 전원 (+5V 보통)                                 |
| **GND**                 | 접지                                          |
| **AO** (Analog Output)  | 아날로그 신호 출력 (0\~5V) → 가스 농도 연속 값             |
| **DO** (Digital Output) | 디지털 신호 (HIGH/LOW) → 특정 임계값 초과 시 HIGH/LOW 출력 |
```

#### 특징
```less
# AO (Analog)

가스 농도에 따라 연속적인 전압 출력

라즈베리파이는 아날로그 입력 없음 → 사용하려면 ADC 모듈 필요 (예: MCP3008)
```

```less
# DO (Digital)

모듈에 있는 **가변저항(포텐셔미터)**으로 임계값 설정

가스 농도가 임계값 이상이면 HIGH / 이하이면 LOW

라즈베리파이는 GPIO 입력으로 바로 읽기 가능
```


#### AO(Analog Output)의 역할
```less
1. 연속적인 가스 농도 값 제공

AO는 0~5V 전압으로 현재 공기 중 가스 농도를 나타냅니다.

예: 가스가 많으면 전압이 높아지고, 적으면 낮아집니다.

2. 정밀한 농도 측정 가능

DO는 단순히 “임계값 이상인지 아닌지”만 알려주지만,

AO는 정확히 얼마만큼 농도가 올라갔는지 알 수 있습니다.

3. 사용 예

연속적으로 농도 변화 모니터링

경고 임계값을 여러 단계로 나누고 싶을 때

로깅/그래프 작성, 자동 환기 시스템 제어 등
```


#### AO(Analog Output)
```less
센서 내부 가열소자와 가스 센서 전극이 만들어내는 저항 변화 → 연속적인 전압 변화

라즈베리파이는 ADC(MCP3008)를 통해 전압 값을 읽음

“현재 가스 농도가 얼마인지” 정보를 실시간으로 줌
```

#### DO(Digital Output)
```less
모듈 내부에 **비교기(Comparator)**가 있음

DO 핀은 AO 전압을 **설정된 임계값(threshold)**과 비교

AO 전압 ≥ 임계값 → DO HIGH

AO 전압 < 임계값 → DO LOW

즉, DO는 AO를 센서 내부 회로가 스스로 판단해서 디지털로 변환한 신호
```

#### 모듈 테스트 코드
```less
from gpiozero import MCP3008, DigitalInputDevice
import time

# MQ-2 센서 연결
mq2_ao = MCP3008(channel=0)         # AO → MCP3008 CH0
mq2_do = DigitalInputDevice(17)     # DO → GPIO 17번

try:
    while True:
        # AO 값 읽기
        gas_level = mq2_ao.value  # 0.0 ~ 1.0
        print(f"가스 농도 (AO): {gas_level:.3f}")

        # DO 값 확인
        if mq2_do.value:  # HIGH 상태
            print("⚠️ 가스 농도 임계값 초과! (DO HIGH)")
        else:
            print("가스 농도 정상 범위 (DO LOW)")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("종료합니다.")
```








