✅ 현재 상태
랜선 꽂음 (이더넷 연결됨)

192.168.0.164라는 IP는 라우터에서 확인됨 (MAC도 나옴, 즉 실제로 연결은 된 상태)

그런데 ssh pi@192.168.0.164로 접속하면 안 됨

원래 쓰던 SD카드는 접속 잘 됨

새로 구운 SD카드는 IP는 받았는데 SSH 접속도 안 되고 인터넷도 안 됨


1. SSH가 비활성화된 상태


라즈비안 OS를 새로 구우면 기본적으로 SSH 비활성화 상태
```less
- SD카드 굽고
- boot 드라이브 열고
- "ssh"라는 **확장자 없는 빈 파일** 만들기
```

2. SD카드가 마운트된 경로 확인

```less
mount
```
/Volumes/boot 또는 /Volumes/bootfs 등 마운트 경로 확인


3. ssh 파일 만들기

```less
touch /Volumes/boot/ssh
```

boot 파티션 루트에 빈 ssh 파일을 생성






