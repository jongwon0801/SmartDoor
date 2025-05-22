#### /home/pi/www/shell/speaker.sh

```less
#!/usr/bin/env bash

# 기본 명령어 설정
command="cvlc --play-and-exit $2 --alsa-audio-device $1 --gain=$3"

# $3 인자가 제공되면 -aout=$3 추가
if [ -n "$4" ]; then
    command="$command --aout=$4"
fi

# 최종 명령어 출력
echo "실행할 명령어: $command"

# 명령어 실행
eval $command
```

🎯 목적
```less
VLC의 CLI 버전인 cvlc를 이용하여 오디오 파일을 재생합니다.

특정 사운드 장치(--alsa-audio-device)를 지정해서 출력합니다.

볼륨 게인 조절(--gain)을 합니다.

옵션으로 --aout (audio output 방식)도 추가할 수 있습니다.
```
```less
command="cvlc --play-and-exit $2 --alsa-audio-device $1 --gain=$3"
```

| 인자 | 의미                          |
|-------|------------------------------|
| $1    | 오디오 장치명 (예: hw:1,0)    |
| $2    | 재생할 오디오 파일 경로         |
| $3    | 게인 값 (볼륨 조정, 예: 1.0)    |
| $4    | (선택) aout 값 (예: alsa, pulse, jack) |

```less
if [ -n "$4" ]; then
    command="$command --aout=$4"
fi
```

--aout은 VLC가 어떤 출력 백엔드를 쓸지 정하는 옵션입니다.

ALSA를 명시하거나, 필요시 PulseAudio 등을 지정할 수 있습니다.


```less
eval $command
```

문자열로 된 전체 명령어를 실행합니다.

🟦 예시 실행
```less
./speaker.sh hw:1,0 /home/pi/audio/hello.wav 1.2 alsa
```

→ 아래 명령어가 실행됩니다
```less
cvlc --play-and-exit /home/pi/audio/hello.wav --alsa-audio-device hw:1,0 --gain=1.2 --aout=alsa
```


✅ 장점
```less
VLC 엔진 사용이므로 폭넓은 포맷 지원

단일 명령으로 실행 가능해 간편

외부 제어 없이 파일 하나만 재생하고 종료
```

❌ 단점
```less
VLC 프로세스를 새로 실행해야 해서 속도나 반응성은 떨어질 수 있음

재생 중 상태 확인이나 중지 제어가 불가능하거나 어렵다

재생 속도 조절이 안 됨 (--rate 옵션은 CLI에서 제한적)
```

🟨 결론: 이걸 사용하는 이유

speaker.sh 스크립트는

📦 단순하게 VLC로 음성 한 줄만 재생하고 끝낼 때 매우 유용합니다.

💡 추천
```less
✅ 단타 음성 안내 (예: "문이 열렸습니다", "등록되었습니다")에 이 방법을 사용

🚫 긴 재생 목록, 반복, 속도 조절이 필요한 경우에는 Python vlc API 버전 사용
```












