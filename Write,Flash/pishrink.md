✅ 1단계: pishrink 설치 (라즈베리파이 또는 리눅스 환경에서)

```less
sudo apt update
sudo apt install git -y
git clone https://github.com/Drewsif/pishrink.git
cd pishrink
chmod +x pishrink.sh
```

pishrink.sh가 준비 완료!

✅ 2단계

```less
diskutil list

/dev/disk4 (external, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      GUID_partition_scheme                        *256.1 GB   disk4
   1:                        EFI EFI                     209.7 MB   disk4s1
   2:                  Apple_HFS 외장하드           255.7 GB   disk4s2

ls /Volumes

ls "/Volumes/외장하드"

scp "/Volumes/외장하드/testB.img" pi@192.168.0.164:~/pishrink/
```

✅ 3단계: pishrink 실행

cd ~/pishrink

sudo ./pishrink.sh ~/myimage.img

완료되면 myimage.img → myimage.img (작아진 상태)로 덮어쓰기됨

원본 보존하고 싶으면

sudo ./pishrink.sh -z ~/myimage.img


💡 pishrink의 효과는?
32GB 이미지가 보통 2~5GB 정도로 압축됨

빈 공간 제외하고 실제 사용중인 파티션만 남기니까 효율 굿


