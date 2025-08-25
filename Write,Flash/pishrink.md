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

6. Mac 에서 디스크 유틸리티로 dmg 파일 만들 경우
읽기 전용으로 해야 파일시스템 GUID 파티션, 맥 os 저널링 아닌경우에 부팅디스크 생성됨

7. 주의 : 포맷이 맥 os 저널링일 경우 라즈베리파이에서 읽기만 되고 쓰기가 불가능
usbdrive 포맷을 exfat에 설계 MBR로 해야 pishrink 가능
```

#### CASE 1 
```less
디스크유틸리티를 이용해서 만든 dmg 이미지의 용량보다
에처로 flash 할 sd카드의 용량이 넉넉할 case

디스크 유틸리티로 이미지만들때 읽기/쓰기 일 경우
포맷 : MAC OS 확장 저널링
설계 : GUID 파티션맵 일 경우만
부팅디스크 만들어짐

디스크 유틸리티로 이미지만들때 읽기 전용 일 경우
포맷 : 상관없음
설계 : 상관없음
만들어도 부팅디스크 만들어짐
```

#### CASE 2
```less
만든 이미지의 용량이 flash할 sd카드의 용량 보다 작아야 할 case
(이미지 만들때 기존 이미지최대용량보다 항상 커짐 32G sd카드 이미지만들면 32G 초과함 )

dd 명령어로 img 확장자의 이미지파일을 만들어야 한다 (dmg는 pishrink 불가능) 1차 주의

이때 만들 img 확장자의 이미지파일을 저장할 usbdrive의 디스크 포맷이 중요하다 2차 주의

pishrink는 라즈베리 파이에서 쓰는 이미지의 빈공간을 줄여주는 도구 인데
usbdrive를 RPI에 꽂았을때

포맷 : EXFAT
설계 : MBR 경우에만 (설계는 GUID 파티션맵 이어도 될 수도 잇음)

/media/pi/usbdrive 에서 마운트가 정상적으로 되고 읽기 뿐만 아니라 쓰기도 가능하다

포맷이 EXFAT가 아닐 경우 에는 읽기만 가능하고 쓰기가 안되서 pishrink를 사용 불가능하다

그리고 라즈베리파이에 usbdrive 꽂을떄는 usb 3.0 포트에 꽂아야한다 (파란색 솜 있는부분)

그래야 데이터 전송 속도가 빠르다 usb2.0과 비교해서 빠르다. 최대 10배의 속도 차이가 난다
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

sudo mount /dev/sda1 "/media/pi/외장 USB"

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

sudo ./pishrink.sh "/media/pi/외장/연구실42Add_Voice_20250605.img"

sudo ./pishrink.sh "/media/pi/usbdrive1/exhibition_after_20250820.img"

sudo ./pishrink.sh "/media/pi/usbdrive1/Add_docker_20250825.img"
```

#### 라즈베리파이에서 읽기 쓰기 마운트 다시 해도 안될 경우
```less
# USB 자체를 읽기/쓰기 가능하게 만들기 (Mac 필요)
diskutil disableJournal /Volumes/usbdrive
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

#### 마운트 안될때
```less
# 읽기 전용 마운트인지 확인
mount | grep /media/pi/usbdrive

/dev/sdb2 on /media/pi/usbdrive type hfsplus (ro,nosuid,nodev,relatime,umask=22,uid=1000,gid=1000,nls=utf8,uhelper=udisks2)

# 만약 ro(read-only)로 마운트되어 있다면, rw(read-write)로 다시 마운트해야 합니다.
sudo umount /media/pi/usbdrive

# 마운트 포인트 존재 여부 확인
ls -ld /media/pi/usbdrive

# 폴더가 없다면 아래 명령어로 생성
sudo mkdir -p /media/pi/usbdrive

# 연결된 블록 장치 목록과 파티션이 출력
lsblk

# 재마운트 명령 (읽기/쓰기 가능하도록)
sudo mount -t hfsplus -o rw,force /dev/sdb2 /media/pi/usbdrive

# 현재 마운트 옵션(읽기 전용인지, 읽기/쓰기인지 등)도 같이 확인
mount | grep /media/pi/usbdrive
/dev/sdb2 on /media/pi/usbdrive type hfsplus (rw,relatime,umask=22,uid=0,gid=0,nls=utf8)

sudo mount -t hfsplus -o rw,force /dev/sdb2 /media/pi/usbdrive
```





