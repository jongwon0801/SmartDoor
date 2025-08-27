#### Uart 5 활성화
```less
라즈베리파이 4에서는 기본적으로 UART0만 활성화되어 있고, UART1은 비활성화 상태

sudo nano /boot/config.txt

파일 맨 아래에 다음 내용 추가하기

[all]
# UART5 활성화를 위한 설정
dtoverlay=uart5

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
```

#### uart 추가 안될 경우
```less
sudo nano /boot/cmdline.txt
```
























