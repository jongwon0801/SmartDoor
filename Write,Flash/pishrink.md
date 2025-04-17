✅ 1단계: pishrink 설치 (라즈베리파이 또는 리눅스 환경에서)

```less
sudo apt update
sudo apt install git -y
git clone https://github.com/Drewsif/pishrink.git
cd pishrink
chmod +x pishrink.sh
```

pishrink.sh가 준비 완료!

✅ 2단계: Mac에서 .img 만들고 라즈베리파이로 전송

sudo dd if=/dev/rdisk5 of=~/Desktop/myimage.img bs=1m status=progress

라즈베리파이로 scp 명령으로 전송

scp ~/Desktop/myimage.img pi@<라즈베리파이 IP>:~

라즈베리 홈 디렉토리에 myimage.img 생김

✅ 3단계: pishrink 실행

cd ~/pishrink

sudo ./pishrink.sh ~/myimage.img

완료되면 myimage.img → myimage.img (작아진 상태)로 덮어쓰기됨

원본 보존하고 싶으면

sudo ./pishrink.sh -z ~/myimage.img


💡 pishrink의 효과는?
32GB 이미지가 보통 2~5GB 정도로 압축됨

빈 공간 제외하고 실제 사용중인 파티션만 남기니까 효율 굿


