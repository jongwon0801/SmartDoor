
### 전체 구성

<img width="688" alt="image" src="https://github.com/user-attachments/assets/c2fc57e9-a564-443a-adec-c92d3003b20a" />

- 통신 방식 : 시리얼 통신, 비동기 통신

- 시리얼 통신은 직렬 연결이라는 뜻을 가지고 있으며, 직렬 연결은 한번 에 하나의 비트단위로 1(High)과 0(Low)의 신호로 데이터를 전송하는 통신 방법

- 비동기 통신은 클럭 신호를 사용하지 않기 때문에 통신에 필요한 선의 수가 더 적음, 하지만 통신 속도 측면에서는 동기 통신방식이 효율이 더 좋다
- 비동기 통신을 사용할 때에는 통신에 참여하는 두 주체가 서로 대등한 관계에서 일대일 통신을 한다.

통신 표준 : RS-485

UART(범용 비동기화 송수신기: Universal asynchronous receiver/transmitter)는 병렬 데이터의 형태를 직렬 방식으로 전환하여 데이터를 전송하는 컴퓨터 하드웨어

### 비동기(Asynchronous) 통신

- 비동기 통신은 동기를 맞추기 위한 별도의 클럭 신호 없이 데이터를 주고 받는 방법
- 클럭 신호가 없기 때문에 송신자는 한 바이트의 데이털르 전송하기 직전에 통신의 시작을 알리는 시작 비트를 먼저 보내 데이터의 전송이 시작된다는 것을 수신자에게 알림
- 시작 비트를 보낸 다음부터 데이터를 한 비트씩 보내고 마지막에는 통신의 끝을 알리는 정지 비트를 보내 통신이 끝났음을 알림

### gpio

<img width="370" alt="image" src="https://github.com/user-attachments/assets/ba172d5f-5059-4ff3-912d-af633202f2ea" />


### 스마트도어 스크린

<img width="335" alt="image" src="https://github.com/user-attachments/assets/9d573b71-5432-465c-b8dd-333470290ee0" />

### pir 센서
- 센서 감지로 카메라가 켜짐 (얼굴인식 기능위해 필요)
- 적외선 PIR센서(PIR, Passive Infrated Sensor)는말그대로수동적외선센서로써적외선을통해 사람의 움직임(모션, motion)을 감지하는센서

<img width="82" alt="image" src="https://github.com/user-attachments/assets/c4d6ca72-1c28-41a8-9324-27795141115a" />

### usb 포트
sd card 라즈베리파이에 직접 연결 안해도 된다

<img width="148" alt="image" src="https://github.com/user-attachments/assets/3c665cf0-ad18-4c7c-aa0a-ae6bad9a964f" />

### 파워
- 전기 공급

<img width="177" alt="image" src="https://github.com/user-attachments/assets/9683141e-a7e2-4ae8-b6d4-8095d63a5589" />


### os 버젼

라즈베리4 모델 b / 64bit bullseye desktop 버젼

- 현재 Raspberry Pi OS는 기본 데스크톱 환경만 포함된 Standard Desktop 버전



### 네트워크 관리방법 변경

dhcpcd -> networkManager 로 변경

관리 범위: dhcpcd는 기본적으로 IP 주소 할당과 네트워크 인터페이스의 설정을 관리하는 반면,
NetworkManager는 여러 종류의 네트워크 인터페이스(Wi-Fi, 유선, VPN 등)를 포괄적으로 관리하는 데 사용됩니다



### nginx 설치

nginx 설치 이유

- 백엔드 서버의 부하 분산: 정적 파일 제공과 WebSocket 관리를 분리.
- 보안 강화: Reverse Proxy로 HTTPS 및 IP 제한 관리.
- 확장성과 유연성: 프로젝트가 커지더라도 쉽게 확장 가능.
- 성능 최적화: 저사양 환경에서도 효율적으로 운영.
- 에러 처리 및 사용자 경험: 안정적인 서비스 제공.
```bash

http {
	client_max_body_size 0;
}

이유 : 클라이언트가 전송하는 데이터 크기를 제한하지 않아서 대용량 파일 업로드나 특정 상황에서 데이터를 제한 없이 전송할 수 있도록 하기 위해서



sudo nano /etc/nginx/conf.d/localhost.conf

이유 : HTTP 요청과 WebSocket 요청을 처리하는 웹 서버를 설정


```

### 데이터베이스 mariadb

- 무료 오픈 소스로 비용을 절감할 수 있음.
- MySQL과의 호환성을 유지하면서도 추가 기능 활용 가능.
- 성능과 확장성이 뛰어나 IoT 프로젝트에 적합.
- 저사양 환경에서도 안정적으로 작동.
- JSON 데이터 처리와 보안 기능이 유용.

- MariaDB와 Nginx는 전통적으로 시스템의 서비스로 설치되며, 가상환경에 설치되지 않습니다.

### virtualenv, virtualenvwraaper 설치

이유 : Python 환경을 격리하여 프로젝트별로 독립된 환경을 제공하기 위해서

- ./profile ./bashrc 설정, virtualenvwrapper.sh 위치 주의 /usr/share/virtualenvwrapper/virtualenvwrapper.sh


### 라즈베리 파이의 디스플레이 설정은 config.txt 파일에서 조정할 수 있습니다.
- 이 파일은 라즈베리 파이의 부팅 시 시스템 설정을 적용
```bash

sudo nano /boot/config.txt
```



### 디스플레이 설정을 조정하는 이유
```bash
#### 해상도 설정

디스플레이 장치가 자동으로 올바른 해상도를 인식하지 못하거나, 특정 해상도를 강제로 사용해야 하는 경우.
예: 프로젝트에서 특정 UI(스마트 도어락 상태 표시, 제어 화면 등)를 구현할 때, 정확한 해상도가 필요.

#### 오버스캔 조정

일부 디스플레이에서는 화면의 가장자리가 잘리거나 여백이 생길 수 있습니다. 이를 수정하기 위해 오버스캔을 조정합니다.
예: 전체 화면을 정확히 표시하기 위한 조정.

#### 디스플레이 출력 장치 맞춤

HDMI, DSI, 또는 Composite 출력 장치와 같은 디스플레이 모드를 선택해야 하는 경우.
예: 특정 디스플레이 장치(예: 소형 터치스크린, 모니터)에 맞게 설정.

#### 전력 소비 최적화

디스플레이 출력이 필요하지 않은 프로젝트(예: 헤드리스 서버 모드)에서 불필요한 전력을 절약하기 위해 디스플레이 출력을 비활성화.

#### 터치 디스플레이 지원

터치스크린 디스플레이를 사용할 경우, 정확한 입력을 위해 좌표 설정을 조정.

#### FPS 및 주사율 설정

비디오나 애니메이션과 같은 고속 그래픽을 처리하는 프로젝트에서는 주사율(FPS)을 조정하여 더 나은 성능을 보장.
```

### 네트워크 와이파이 자동연결

재부팅 시 자동으로 와이파이를 연결 못하는 현상이 발생 -> 자동으로 와이파이를 잡도록 수정


### tty usb 연결 설정

/dev/ 경로에 tty usb alias, 연결 설정을 해주지 않으면 webserver가 정상적으로 켜지지 않음



### tornado 설치, 실행

백엔드 웹 어플리케이션 tornado 설치 실행 재부팅시 자동으로 켜지게 하기 위해서 service 파일 따로 설정 필요



### 의존성 패키지 제외하고 패키지 설치
```bash

oauthlib==3.1.0

설명: OAuth 1.0 및 2.0 프로토콜을 구현한 라이브러리로, 인증 및 권한 부여 처리.
용도: OAuth 인증 흐름을 구현하여 외부 API와의 안전한 인증을 관리.
requests==2.25.1

설명: HTTP 요청을 간편하게 처리할 수 있는 라이브러리로, GET, POST 등 다양한 HTTP 메서드를 지원.
용도: 외부 API 호출 및 서버 간 데이터 전송에 사용.
requests-oauthlib==1.0.0

설명: requests와 oauthlib를 통합하여 OAuth 인증을 처리하는 라이브러리.
용도: OAuth 인증 방식의 API 요청을 간단하게 처리.
PyJWT==1.7.1

설명: JWT(JSON Web Token)을 인코딩 및 디코딩하는 라이브러리.
용도: 사용자 인증 및 권한 부여를 위한 JWT 토큰 생성 및 검증.

paho-mqtt==2.1.0

설명: MQTT 프로토콜을 구현한 라이브러리로, IoT 장치 간 메시지 전송을 처리.
용도: 스마트 도어락과 같은 IoT 장치에서 MQTT 기반의 메시지 송수신.

numpy==1.19.5

설명: 고성능 수치 연산을 위한 라이브러리로, 배열 및 행렬 연산을 효율적으로 처리.
용도: 수학적 계산이나 데이터 처리 작업에 사용.

pycryptodome==3.20.0

설명: 다양한 암호화 알고리즘(AES, RSA 등)을 제공하는 라이브러리.
용도: 데이터 암호화 및 보안을 강화하기 위한 암호화 작업에 사용.

pyserial==3.5b0

설명: Python에서 시리얼 통신을 처리하는 라이브러리.
용도: 스마트 도어락에서 시리얼 포트를 통한 하드웨어 통신.

pyOpenSSL==20.0.1

설명: Python용 OpenSSL 라이브러리로, SSL/TLS 통신을 지원.
용도: 보안 연결(HTTPS) 및 암호화된 통신 처리.
pylint==2.7.2

설명: Python 코드 품질 검사를 위한 도구로, 코드 스타일을 검사하고 오류를 찾는 데 사용.
용도: 코드 품질 유지 및 자동화된 코드 리뷰.


# pip install opencv-python 오래걸림
# pip install face-recognition	설치 어려움
# 가상환경에 공간을 따로주는 방법 찾아봐야함

```

### 어플리케이션을 실행하면 처음에 기기 등록

- 제품기기번호 입력해 8자리 숫자로 입력 필요

https://petstore.swagger.io/

https://api.hizib.wikibox.kr/smartdoor.yaml 

<img width="517" alt="image" src="https://github.com/user-attachments/assets/7eba043b-d908-4797-b772-fa6c85790557" />

- mysql db 정보를 서버에서 받아오는지 로컬로 저장하는지 확인 필요

- 서버에 저장된 번호랑 겹치지 않게 기기번호 등록


### 날씨 가져오는 기능 제대로 작동 안되는 현상 수정


### 화상통화, 달력, 문열기, 문닫기, mqtt 동작 원리 파악 



