#### 라즈베리파이 음성 녹음
```less
# USB 연결 확인
lsusb
```

```less
# 입력 장치 목록(마이크) 출력. 만약 아무것도 안 뜨면, 커널 드라이버가 안 잡힌 것
arecord -l

실제로 연결되어 있는 캡처(녹음) 하드웨어 장치 목록을 보여줍니다.
만약 아무것도 안 뜨면, 커널 드라이버가 안 잡힌 것

card 2: Camera [USB 4K Live Camera], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

```less
arecord -L

hw:CARD=Device,DEV=0
plughw:CARD=Device,DEV=0

```

| 명령어        | 의미                               | 언제 쓰나                                   |
|---------------|------------------------------------|---------------------------------------------|
| `arecord -l`  | 실제 연결된 녹음 장치 목록 출력    | 카드/디바이스 번호 확인할 때 사용           |
| `arecord -L`  | ALSA에서 인식한 모든 PCM 장치 목록 | 논리 장치 이름 확인, 설정 디버깅할 때 유용  |

plughw를 쓰면 ALSA가 자동으로 포맷 변환(예: 샘플레이트나 채널 수)을 해주기 때문에 일반적으로 hw:보다 plughw: 사용을 추천


```less
# 녹음 테스트
arecord -D plughw:5,0 -f cd -d 3 test.wav

-D plughw:5,0 : 카드 5, 디바이스 0 (USB PnP Sound Device)

-f cd : CD 품질 (16bit, 44.1kHz, 스테레오)

-d 3 : 3초 녹음

test.wav : 현재 작업 디렉토리에 저장되는 파일 이름

# 녹음된 파일 재생
aplay test.wav
```

🔍 차이 설명

✅ plughw:5,0

```less
숫자 기반 표현

arecord -l 명령에서 나오는 card 번호와 device 번호를 사용

arecord -l
card 5: Device_1 [...], device 0: USB Audio [...]

그래서 plughw:5,0 이 나옵니다.
```

✅ plughw:CARD=Device,DEV=0

```less
이름 기반 표현

arecord -L 명령에서 나오는 카드 이름(CARD=...)과 장치 이름(DEV=...) 기반

이름은 시스템이 인식한 장치의 명칭을 따릅니다 (Device, Camera, Headphones, 등)
```

| 표현                         | 장점                           | 비고                                                    |
|------------------------------|--------------------------------|----------------------------------------------------------|
| `plughw:5,0`                 | 짧고 직관적                    | 장치 번호는 시스템 재부팅 시 바뀔 수 있음 ⚠️             |
| `plughw:CARD=Device,DEV=0`   | 더 명시적이고 안정적           | udev나 ALSA 이름 변경 시 일관성 유지됨                  |


✅ 추천
스크립트/자동화에선 이름 기반 (CARD=...) 이 더 안정적입니다.

테스트용이나 일시적 명령엔 plughw:5,0이 더 빠르고 간편합니다.













