#### 라즈베리파이에서 RS-485 통신을 위한 RD SEL 설정

#### 1. config.txt에서 UART 활성화
```less
/boot/config.txt 파일에 다음 설정 추가:

enable_uart=1
dtoverlay=uart3
```
#### 2. GPIO 핀 설정
```less
RD SEL 제어를 위한 GPIO 핀을 설정해야 합니다
터미널에서 다음 명령어로 GPIO 핀을 출력 모드로 설정:
gpio -g mode [핀번호] out
```
#### 3. RS-485 방향 제어 스크립트 작성
송신/수신 모드 전환을 위한 스크립트 작성:
```less
import RPi.GPIO as GPIO
import time

RD_SEL_PIN = [사용할 핀번호]

GPIO.setmode(GPIO.BCM)
GPIO.setup(RD_SEL_PIN, GPIO.OUT)

# 수신 모드 (LOW)
def set_receive_mode():
    GPIO.output(RD_SEL_PIN, GPIO.LOW)

# 송신 모드 (HIGH)
def set_transmit_mode():
    GPIO.output(RD_SEL_PIN, GPIO.HIGH)
```
#### 4. 데이터 송수신 시 적절한 타이밍으로 RD SEL 제어
```less
송신 전에 송신 모드로 설정
송신 완료 후 수신 모드로 전환
통신 속도에 따라 적절한 지연 시간 설정
```
#### 5. 시스템 시작 시 자동 설정
```less
시스템 부팅 시 자동으로 설정되도록 /etc/rc.local에 초기화 코드 추가
```





























































