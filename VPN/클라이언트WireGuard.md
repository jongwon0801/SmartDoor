#### 클라이언트 VPN WireGuard 설치

✅ 1단계: 클라이언트에 WireGuard 설치
```less
sudo apt update
sudo apt install wireguard -y
```

✅ 2단계 클라이언트에서 키 생성
```less
sudo -i
cd /etc/wireguard

umask 077

sudo wg genkey | tee client_private.key | wg pubkey > client_public.key
```

```less
client_private.key: 클라이언트 비밀키

client_public.key: 클라이언트 공개키 (서버에 알려줘야 함)
```

✅ 3단계 클라이언트 설정 파일 만들기

```less
# 개인 키 복사
sudo cat /etc/wireguard/client_private.key
iA+aFpyoYrZAsFpLooTVhWwX08oIhKVKFfAsGauyH0k=

sudo nano /etc/wireguard/wg0.conf

[Interface]
PrivateKey = iA+aFpyoYrZAsFpLooTVhWwX08oIhKVKFfAsGauyH0k=    # 클라이언트_비밀키_내용
Address = 10.0.0.2/24          # 클라이언트의 VPN 내부 IP (서버와 같은 대역)
DNS = 8.8.8.8

[Peer]
PublicKey = LEeBQ70RtCepo5jtYwS+3ZgaDMxKH2+stp/20U+SWl8=    # 서버_공개키_내용
Endpoint = 175.211.153.28:51820                            # 서버_퍼블릭_IP:51820
AllowedIPs = 10.0.0.0/24
PersistentKeepalive = 25

```

✅ 4단계 서버에 클라이언트 정보 추가
```less
[Peer]
PublicKey = DoKpwfJvT3IcXZhyLDYGY3p/59IUKU8L9n9DjuipGBE=
AllowedIPs = 10.0.0.2/32
```

```less
10.0.0.2/32는 오직 하나의 IP (클라이언트 VPN IP)만 지정

10.0.0.0/24는 256개의 IP 전체를 클라이언트에 넘긴다는 뜻이므로 절대 설정하면 안 됩니다
```

✅ 5단계 서버 설정 재적용 (서버 클라이언트 설정바뀌면 둘다 하나만 바뀌면 바뀐곳만)
```less
sudo wg-quick down wg0
sudo wg-quick up wg0
```

✅ 6단계 클라이언트에서 VPN 연결 시작
```less
sudo wg-quick up wg0

자동 시작 등록 (옵션):
sudo systemctl enable wg-quick@wg0
```

<img width="539" alt="image" src="https://github.com/user-attachments/assets/1766b01b-a9aa-481e-81bc-ff5c5e4d425f" />


✅ 7단계 테스트
```less
클라이언트에서 핑 테스트:
ping 10.0.0.1   # 서버의 VPN IP

서버에서 핑 테스트:
ping 10.0.0.2   # 클라이언트의 VPN IP
```



