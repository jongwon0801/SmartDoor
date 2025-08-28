#### ttyAMA0
```less
라즈베리파이의 내장 UART(Universal Asynchronous Receiver/Transmitter) 하드웨어 시리얼 포트입니다.
하드웨어적으로 구현된 시리얼 통신으로, GPIO 핀(주로 GPIO 14, 15)을 통해 직접 연결됩니다.

속도와 안정성이 높습니다.
주로 /boot/config.txt에서 enable_uart=1과 같은 설정으로 활성화됩니다.
```

#### Uart 1 활성화
```less
라즈베리파이 4에서는 기본적으로 UART0만 활성화되어 있음

sudo nano /boot/config.txt

파일 맨 아래에 다음 내용 추가하기

[all]
enable_uart=1
dtoverlay=uart1
```

#### grops 설정
```less
# ttyAMA0는 root와 dialout 그룹만 접근 가능합니다.
# 사용자를 dialout 그룹에 추가
sudo usermod -a -G dialout $USER

# 현재 사용자가 속한 그룹을 확인
groups

# 더 자세한 정보
# dialout 그룹이 목록에 있다면 성공적으로 추가된 것
id

# 특정 사용자의 그룹을 확인
groups $USER
id $USER

# 시리얼 포트 설정 확인
stty -F /dev/ttyAMA0

# minicom 설정 확인
sudo minicom -s

sudo reboot
```

#### gpu_mem=128 옵션
```less
gpu_mem=128의 의미: 시스템 메모리(RAM) 중에서 128MB를 GPU 전용으로 사용하겠다고 할당하는 것을 뜻합니다.

어떤 경우에 필요한가요?

그래픽 위주 사용: 라즈베리파이를 데스크톱처럼 활용하여 웹 브라우징, 동영상 재생, 이미지/사진 편집 등 그래픽 작업이 많은 경우에 유용합니다.
특정 GUI 애플리케이션: 고해상도 화면을 사용하거나, 그래픽 집약적인 애플리케이션을 실행할 때 성능 향상을 기대할 수 있습니다.
HW 가속이 필요한 경우: 비디오 인코딩/디코딩 등 GPU 하드웨어 가속이 필요한 작업 시 유용할 수 있습니다.
```

#### 포트 이름 확인
```less
# 라즈베리파이의 하드웨어 UART 포트
ls -l /dev/ttyAMA*

# USB를 통해 연결된 시리얼 장치들
ls -l /dev/ttyACM*


# uart 추가 안될 경우
sudo nano /boot/cmdline.txt
```

#### ttyACM0
```less
ACM은 "Abstract Control Model"의 약자로, USB를 통해 연결된 시리얼 장치를 의미합니다.
USB 시리얼 변환기나 아두이노와 같은 USB 장치가 연결될 때 생성됩니다.

드라이버를 통해 소프트웨어적으로 구현되는 가상 시리얼 포트입니다.
연결/분리될 때마다 이름이 변경될 수 있습니다.
```

#### UART 매핑 확인
```less
# UART 매핑 확인
# 시리얼 포트 매핑을 확인해보세요. 종종 /dev/serial1이 UART1에 매핑되기도 합니다.
ls -la /dev/serial*

# dmesg 로그 확인
# 커널이 UART 장치를 어떻게 인식했는지 확인
dmesg | grep tty

# dtoverlay 설정 확인
# 사용 가능한 UART 오버레이 목록을 확인
sudo dtoverlay -a | grep uart

# config.txt 설정 확인
sudo nano /boot/config.txt

sudo dmesg | grep uart

ls -l /dev/serial*
```

#### 미니 UART 비활성화
```less
기존 시스템: 8250.nr_uarts=0 - 이 설정은 8250 드라이버의 UART 개수를 0으로 설정하여 미니 UART를 비활성화합니다.
현재 시스템: 8250.nr_uarts=1 - 이 설정은 8250 드라이버의 UART 개수를 1로 설정하여 미니 UART를 활성화합니다.

라즈베리파이에서 미니 UART는 ttyS0로 나타나고, PL011 UART는 ttyAMA0, ttyAMA1 등으로 나타납니다.
```

#### 미니 UART를 비활성화하고 PL011 UART만 사용
```less
/boot/cmdline.txt 파일에서 8250.nr_uarts=1을 8250.nr_uarts=0으로 변경하고 재부팅

# 8250.nr_uarts=0을 추가
console=tty1 root=PARTUUID=2ee1ad41-02 rootfstype=ext4 fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles 8250.nr_uarts=0
```

#### 현재 인식된 시리얼 장치의 커널 이름 확인
```less
ls -l /sys/class/tty/*/device/driver

# 확인된 정보로 udev 규칙 파일 생성
sudo nano /etc/udev/rules.d/99-serial.rules

# 파일에 다음 내용 추가 (ttyAMA0에 대한 규칙):
KERNELS=="fe201000.serial", SYMLINK+="hione"

# udev 규칙 다시 로드
sudo udevadm control --reload-rules
sudo udevadm trigger

# 심볼릭 링크 확인:
ls -l /dev/hione









