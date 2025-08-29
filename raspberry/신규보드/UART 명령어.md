#### dmesg 명령어 확인:
```less
dmesg | grep ttyAMA

이 명령어는 부팅 시 로그에서 각 UART 포트가 어떤 ttyAMA 장치로 매핑되었는지 보여줍니다.
```
#### ls -l /dev 명령어로 상세 확인:
```less
ls -l /dev/ttyAMA*

이 명령어는 ttyAMA 장치들의 세부 정보를 보여줍니다.
```

#### GPIO 핀 기능 확인:
```less
raspi-gpio get 4
raspi-gpio get 5

GPIO 4, 5가 UART3으로 설정되어 있다면, 이 명령어로 확인할 수 있습니다.
```

#### dtoverlay 정보 확인:
```less
dtoverlay -a | grep uart

활성화된 UART 오버레이 정보를 보여줍니다.

일반적으로 라즈베리파이 4 모델에서는:
UART0: 주로 ttyAMA0 또는 ttyS0으로 매핑
UART1: 주로 ttyS1 또는 ttyAMA1로 매핑
UART3: 설정에 따라 ttyAMA0 또는 ttyAMA1로 매핑될 수 있음

만약 /boot/config.txt에서 dtoverlay=uart3로 UART3을 활성화하셨다면, 정확한 매핑을 위 명령어로 확인하시는 것이 가장 정확합니다.

fe201600.serial
```

#### 기본 UART (UART0)
```less
GPIO 14 (TXD0)
GPIO 15 (RXD0)

# 추가 UART 포트
UART1: GPIO 14 (TXD1), GPIO 15 (RXD1) - 일부 모델에서는 다른 핀에 매핑될 수 있음
UART2: GPIO 0 (TXD2), GPIO 1 (RXD2)
UART3: GPIO 4 (TXD3), GPIO 5 (RXD3) - 주인님께서 이미 확인하신 핀
UART4: GPIO 8 (TXD4), GPIO 9 (RXD4)
UART5: GPIO 12 (TXD5), GPIO 13 (RXD5)
```


#### raspi-gpio get
```less
# GPIO 4:

level=1: 현재 핀의 상태가 HIGH(1)입니다

fsel=3, alt=4: 이 핀이 대체 기능 4번으로 설정되어 있음을 의미합니다

func=TXD3: UART3의 송신(Transmit) 핀으로 사용 중입니다

pull=NONE: 내부 풀업/풀다운 저항이 설정되어 있지 않습니다

# GPIO 5:
level=1: 현재 핀의 상태가 HIGH(1)입니다

fsel=3, alt=4: 이 핀이 대체 기능 4번으로 설정되어 있음을 의미합니다

func=RXD3: UART3의 수신(Receive) 핀으로 사용 중입니다

pull=UP: 내부 풀업 저항이 활성화되어 있습니다 (수신 핀은 보통 풀업 저항 사용)

이 설정은 GPIO 4번과 5번 핀이 일반 GPIO 용도가 아닌 UART3 통신용(직렬 통신)으로 현재 구성되어 있음을 보여줍니다.
스마트 도어 프로젝트에서 이 핀들을 통해 외부 장치와 UART 통신을 하고 계신 것으로 보입니다.
```

#### fsel (Function Select): 핀의 "큰 틀" 또는 "카테고리"를 지정합니다.
```less
fsel=0: GPIO Input (범용 입력)
fsel=1: GPIO Output (범용 출력)
fsel=2: Alt Function 0 (특정 대체 기능 그룹 0)
fsel=3: Alt Function 1 (특정 대체 기능 그룹 1)
fsel=4: Alt Function 2 (특정 대체 기능 그룹 2)

... 등등 이 fsel 값은 해당 GPIO 핀이 '범용 입출력 모드'인지, 아니면 '대체 기능 모드'인지,
그리고 어떤 '대체 기능 그룹'에 속하는지를 결정합니다.

즉, 핀이 사용할 기능의 종류를 크게 나누는 역할입니다. fsel=3은 이 핀이 대체 기능 모드로 설정되었으며,
특정 "대체 기능 그룹 1"을 사용하겠다고 선언하는 것입니다.

alt (Alternate Function): fsel로 지정된 큰 틀 안에서 "정확히 어떤 기능"을 사용할지 세부적으로 지정합니다.
```

```less
각 GPIO 핀은 여러 개의 대체 기능을 가질 수 있습니다.
예를 들어, 어떤 핀의 fsel=3 그룹에는 UART, SPI, I2C 기능이 모두 있을 수 있습니다.

이때, alt=4는 해당 대체 기능 그룹 내에서 구체적으로 4번 기능을 사용하겠다고 알려주는 것입니다.
이 경우, 대체 기능 그룹 1 (fsel=3) 내의 4번 기능이 TXD3/RXD3 (UART3)과 매핑되어 있는 것입니다.
```

#### 요약하자면:
```less
fsel=3: "이 핀은 범용 GPIO가 아니라 대체 기능을 쓸 거고, **특정 그룹 (예: 그룹 1)**에서 찾으렴."
alt=4: "그 특정 그룹 (fsel=3) 안에서 정확히 4번 기능인 UART3 (TXD3/RXD3)을 써라."

따라서 fsel=3은 해당 핀이 범용 입출력 모드가 아닌 대체 기능 모드이며,
그중에서도 특정 그룹에 속한다는 큰 범주를 나타내고, alt=4는 그 대체 기능 그룹 내에서 실제 어떤 특수 기능을 사용할지를 구체적으로 선택하는 것입니다.
둘은 서로 다른 레벨의 정보를 제공하여 핀의 기능을 명확히 정의합니다.
```

