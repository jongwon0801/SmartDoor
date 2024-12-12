## Raspberry Pi Imager를 사용하여 Raspberry Pi OS 설치 
<br>
https://www.raspberrypi.com/software/

### Imager 다운 -> raspberry Pi 4 (디바이스) / raspberry Pi OS (32bit) (운영체제) / 저장소 (bootfs) 설치 

<img width="652" alt="image" src="https://github.com/user-attachments/assets/b8738cc2-e4a0-41f9-897f-7599ca578b7e">


### macOS에서는 직접적으로 리눅스용 패키지 설치가 어렵기 때문에, SD 카드에 있는 리눅스 루트 파일 시스템을 마운트하고, 그 위에서 설정을 진행해야 합니다.

1. SD 카드 파일 시스템 확인
SD 카드에 우분투나 라즈비안 OS 이미지를 구운 상태에서, macOS에서 파일 시스템을 확인합니다:

diskutil list

https://www.raspberrypi.com/software/operating-systems/
