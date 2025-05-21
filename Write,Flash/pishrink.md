#### pishrink 쓰는이유

```less
1. 디스크 유틸리티에서 dmg 파일 읽기/쓰기로 만들면 부팅디스크가 생성안됨
(GUID 파티션, 맥 os 저널링 일때만 부팅디스크 만들어졌음 (읽기/쓰기 기준)
읽기 전용으로 해야 부팅디스크 파일시스템 상관없이 만들어짐 !! (중요) 

2. dmg or img 이미지의 크기가 sd카드(32G) 용량을 넘어감
(이유 : 빈공간 까지 이미지로 만들어버림)
-> 에처로 굽기 실패(sd 카드의 용량이 32 기가인데 이미지가 32기가가 넘어감)

3. dd 명령어로 img 형태로 외장하드(usb 드라이브)에 집어넣음
(이유 : dmg 파일은 pishrink 불가능)

4. 라즈베리파이에 pishrink 설치하고 exFAT 관련 패키지 설치
(이유 : usb 삼성 드라이브 파일시스템 MBR, exFAT)
-> 라즈베리파이에 usb 연결 후 pishrink 실행해서 용량줄이기

5. 용량 줄인 img는 32G -> 13G 이므로 32G, 16G sd 카드에 구울 수 있음

6. 읽기 전용으로 파일시스템 GUID 파티션, 맥 os 저널링 아닌경우에 부팅디스크 생성됨
```

#### pishrink 설치 (라즈베리파이 또는 리눅스 환경에서)

```less
sudo apt update
sudo apt install git -y
git clone https://github.com/Drewsif/pishrink.git
cd pishrink
chmod +x pishrink.sh
```

pishrink.sh가 준비 완료!

```less

# 라즈베리 파티션 확장
sudo raspi-config -> Advanced Options -> Expand Filesystem

# 외장하드 라즈베리파이에 꽂기
```

#### 라즈베리에서 외장하드 마운트 경로
```less
/media/pi/SAMSUNG USB

lsblk

NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda           8:0    0 238.5G  0 disk 
└─sda1        8:1    0 238.5G  0 part 
mmcblk0     179:0    0 119.4G  0 disk 
├─mmcblk0p1 179:1    0  41.8M  0 part /boot
└─mmcblk0p2 179:2    0 119.3G  0 part /

# 외장 드라이브 마운트
sudo mount /dev/sda1 /media/pi/SAMSUNG\ USB
mount: /media/pi/SAMSUNG USB: unknown filesystem type 'exfat'.

# 외장하드가 exFAT 파일 시스템을 사용하고 있어서 마운트가 실패
# exFAT 파일 시스템을 라즈베리파이에서 사용하려면, 해당 파일 시스템을 지원하는 패키지를 설치
(외장하드 파일시스템 : MBR, exFAT (읽기전용), sd카드 파일시스템은 에처로 구울때 재생성되므로 상관없음)
sudo apt update
sudo apt install exfat-fuse exfat-utils

# 다시 마운트
sudo mount /dev/sda1 /media/pi/SAMSUNG\ USB

# 드라이브 확인
ls /media/pi/SAMSUNG\ USB
정은b.dmg  정은치엘로B.img

# 드라이브 파일 크기 확인
ls -lh /media/pi/SAMSUNG\ USB
합계 45G
-rwxrwxrwx 1 root root 15G  4월 21 23:26 정은b.dmg
-rwxrwxrwx 1 root root 30G  4월 21 23:51 정은치엘로B.img

# pishrink 경로
/home/pi/pishrink/pishrink.sh

# usb에 있는 img 파일 줄이기
sudo ./pishrink.sh /media/pi/SAMSUNG\ USB/정은치엘로B.img

```

```less
# 외장 드라이브 마운트 (RPI4는 알아서 된다)
sudo mount /dev/sda1 /media/pi/외장
mount: /media/pi/외장: /dev/sda1 already mounted on /media/pi/외장.

sudo ./pishrink.sh /media/pi/외장/Smartdoor161_Add_IOT_20250501.img

sudo ./pishrink.sh /media/pi/외장/부산doorwifi수정_20250521.img

Raspberry Pi 3에서는 exFAT 파일 시스템을 지원하려면 **exfat-fuse** 와 exfat-utils 패키지를 설치해야 했습니다.
이것은 기본적으로 지원되지 않아서, 수동으로 설치해야 했습니다.

**Raspberry Pi 4 (Bullseye 64-bit)**에서는 exFAT 파일 시스템 지원이 기본적으로 내장되어 있어,
별도의 패키지 설치 없이 바로 exFAT 드라이브를 사용할 수 있습니다
```


💡 pishrink의 효과는?
32GB 이미지가 보통 2~5GB 정도로 압축됨

빈 공간 제외하고 실제 사용중인 파티션만 남기니까 효율 굿


