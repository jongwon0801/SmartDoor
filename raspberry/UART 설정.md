#### Uart 1 활성화
```less
라즈베리파이 4에서는 기본적으로 UART0만 활성화되어 있음

sudo nano /boot/config.txt

파일 맨 아래에 다음 내용 추가하기

[all]
enable_uart=1
dtoverlay=uart1

sudo usermod -a -G dialout $USER

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
# 포트 이름 확인
ls -l /dev/ttyAMA*

# 권한 설정
sudo usermod -a -G dialout $USER

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






















