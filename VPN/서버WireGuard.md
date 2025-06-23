#### 스마트도어 서버 VPN WireGuard 설치

✅ 1단계: WireGuard 설치
```less
sudo apt update
sudo apt install wireguard -y
```

✅ 2단계: 키 생성 (서버용)
```less
sudo -i
cd /etc/wireguard

umask 077

sudo wg genkey | tee server_private.key | wg pubkey > server_public.key
```
```less
server_private.key: 서버 비밀키

server_public.key: 서버 공개키 (클라이언트와 공유할 것)
```

✅ 3단계: 설정 파일 만들기 (wg0.conf)
```less
# 개인 키 복사
sudo cat /etc/wireguard/server_private.key

sudo nano /etc/wireguard/wg0.conf

[Interface]
Address = 10.0.0.1/24         # 서버 VPN 내부 IP
ListenPort = 51820            # 기본 WireGuard 포트 (UDP)
PrivateKey = 서버_비밀키_내용_여기에_붙여넣기

# 이후 클라이언트 연결할 때 [Peer] 섹션 추가
```


✅ 4단계: 방화벽/포트 오픈
```less
# ufw가 막고 있는지 확인
sudo ufw status verbose
inactive라면 UFW가 아무것도 막고 있지 않음.

# 방화벽 규칙 확인
sudo iptables -L -n

# 서버 내에서 포트 리스닝 상태 확인
sudo ss -tuln
0.0.0.0이면 외부에서 접속 가능, 127.0.0.1이면 로컬 전용이라 외부에서 접근 불가

# TCP 포트 번호 사용 중인 프로세스를 확인하기 위해 사용하는 명령어
ss -tnp | grep <포트번호>

UFW를 사용하는 경우:
sudo ufw allow 51820/udp
```

| 옵션   | 의미                                      |
| ---- | --------------------------------------- |
| `-t` | TCP 포트만 표시                              |
| `-u` | UDP 포트도 포함                              |
| `-l` | 리스닝(Listen) 상태인 소켓만 표시 (서버가 열어놓은 포트)    |
| `-n` | 포트 번호/주소를 숫자로 표시 (ex. 80 → http 해석 안 함) |
| `-p` | 해당 포트를 사용 중인 프로세스 표시                    |


✅ 5단계: WireGuard 서버 시작

```less
sudo wg-quick up wg0

자동 시작 설정 (재부팅 시 자동 실행):
sudo systemctl enable wg-quick@wg0
```

✅ 6단계: 상태 확인
```less
sudo wg show

interface: wg0
  public key: LEeBQ70RtCepo5jtYwS+3ZgaDMxKH2+stp/20U+SWl8=
  private key: (hidden)
  listening port: 51820
```


