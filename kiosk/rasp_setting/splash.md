#### 시작할때 splash 이미지 바꾸기

```bash

# /home/pi/www/image 경로의 이미지를 기본설정 경로로 복사
sudo cp /home/pi/www/image/splash.png /usr/share/plymouth/themes/pix/splash.png

# 테마가 적용되도록 Plymouth 설정을 업데이트

sudo plymouth-set-default-theme pix
sudo update-initramfs -u

```
