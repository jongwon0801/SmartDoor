#### MotherBoard GPIO 회로 구성

| GPIO 번호 | 기능/설명      |
|:----------|:---------------|
| GPIO2     | I2C_SDA        |
| GPIO4     | LOCK_TX3       |
| GPIO5     | LOCK_RX3       |
| GPIO14    | RS485-TX0      |
| GPIO15    | RS485-RX0      |
| GPIO17    | RS485_RDSEL    |
| GPIO22    | PIR_SENSOR     |
| GPIO25    | SWITCH         |

#### GPIO 
```less
raspi-gpio get

GPIO 28: level=1 fsel=2 alt=5 func=RGMII_MDIO pull=UP
```

#### 옵션 설명
```less
level=1: 현재 핀의 상태가 HIGH(1) 상태입니다. 즉, 전압이 걸려 있는 상태입니다.

fsel=2: Function Select 값이 2로, 이 핀이 대체 기능(Alternative Function)으로 설정되어 있음을 의미합니다.

alt=5: Alternative Function 5번으로 설정되어 있습니다. 라즈베리파이의 각 GPIO 핀은 여러 대체 기능을 가질 수 있습니다.

func=RGMII_MDIO: 현재 이 핀은 RGMII(Reduced Gigabit Media-Independent Interface)의
MDIO(Management Data Input/Output) 기능을 수행하고 있습니다.

이는 이더넷 통신에서 PHY 칩 제어를 위한 관리 인터페이스입니다.

pull=UP: 내부 풀업 저항이 활성화되어 있습니다. 이는 핀이 외부 연결 없이도 HIGH 상태를 유지하도록 해줍니다.
```


#### I2C_SDA (Inter-Integrated Circuit Serial Data)
```less
I2C 통신 프로토콜에서 데이터를 전송하는 핀입니다. 마이크로컨트롤러와 센서, 디스플레이 등의 주변 장치 간 통신에 사용됩니다.
```

#### LOCK_TX3 / LOCK_RX3
```less
TX3: 도어락 제어 관련 데이터를 전송(Transmit)하는 핀

RX3: 도어락으로부터 데이터를 수신(Receive)하는 핀
```

#### RS485-TX0 / RS485-RX0 / RS485_RDSEL
```less
RS485: 산업용 통신 표준으로, 장거리 통신이 가능한 시리얼 통신 방식입니다.

TX0: RS485 통신에서 데이터를 전송하는 핀

RX0: RS485 통신에서 데이터를 수신하는 핀

RDSEL: RS485 통신에서 읽기/쓰기 모드를 선택(Read Select)하는 제어 핀
```

#### PIR_SENSOR
```less
PIR(Passive Infrared) 센서 연결 핀으로, 움직임 감지 센서와 연결되어 주변 환경의 움직임을 감지합니다.
```

#### SWITCH
```less
물리적 스위치나 버튼 입력을 받는 핀입니다. 사용자 입력이나 상태 전환 등에 사용됩니다.
```


















































