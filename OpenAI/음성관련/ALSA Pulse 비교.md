#### 1. ALSA (Advanced Linux Sound Architecture)
```less
리눅스 커널의 저수준 오디오 드라이버 및 인터페이스

하드웨어(사운드 카드, USB 오디오 장치 등)와 직접 통신

실제 소리 재생을 담당하는 가장 기본 계층

aplay -l, arecord -l 같은 명령어로 ALSA 하드웨어 디바이스 목록 확인 가능
```

```less
ALSA에서 직접 연결된 하드웨어 디바이스 목록을 출력합니다.

예: USB 마이크, 내장 오디오, HDMI 출력 등

arecord -l     # 입력 (마이크)
aplay -l       # 출력 (스피커)
```

#### 2. PulseAudio
```less
사용자 공간의 사운드 서버 (Sound Server)

ALSA 위에 올라가서 여러 응용프로그램에서 오디오 입출력을 관리

여러 소리를 섞거나, 네트워크 오디오 전송, 볼륨 조절, 장치 전환 등을 처리

ALSA 디바이스를 추상화해 앱들이 편하게 사용하도록 함

pactl, pacmd 명령으로 PulseAudio 상태 및 장치 제어 가능
```

```less
PulseAudio는 기본적으로 ALSA 위에서 작동하는 사운드 서버입니다.

시스템에 존재하는 ALSA 장치를 인식하여 가상 장치(pulse, default, dmix 등) 로 관리합니다.

PulseAudio는 ALSA 장치를 자동으로 "소스(Source)" 또는 "싱크(Sink)" 로 래핑하여 사용자에게 제공합니다.

pactl list sources short      # 입력 장치 (마이크)
pactl list sinks short        # 출력 장치 (스피커)
```

```less
arecord -l / aplay -l에서 보이는 ALSA 장치는 대부분 PulseAudio에서도 자동으로 등록되고 사용할 수 있습니다.

다만 PulseAudio 설정이 비활성화되어 있거나, 특정 장치를 "무시"하게 설정한 경우엔 예외가 있을 수 있습니다.
```


#### 3. 시스템 기본 오디오 출력
```less
리눅스에서 "시스템 기본 오디오 출력"은 보통 PulseAudio 기준의 기본 출력장치 (default sink) 의미

PulseAudio가 여러 ALSA 하드웨어 장치(스피커, HDMI, USB 오디오 등)를 관리할 때,
사용자가 기본으로 설정해 놓은 출력장치를 의미함

기본 출력장치를 바꾸면, 대부분의 앱들은 그 장치로 소리를 출력
```


#### 정리
```less
실제 소리는 ALSA가 장치를 제어해서 냄

PulseAudio가 여러 ALSA 장치 위에서 오디오 흐름과 믹싱 관리

시스템 기본 오디오 출력은 PulseAudio 기준 기본 장치(sink) 설정임
```








