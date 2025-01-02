### chromium-browser 실행

```bash

chromium-browser --kiosk http://127.0.0.1

# error
Invalid MIT-MAGIC-COOKIE-1 key[15617:15617:0102/061446.224666:ERROR:ozone_platform_x11.cc(244)] Missing X server or $DISPLAY
[15617:15617:0102/061446.225068:ERROR:env.cc(258)] The platform failed to initialize.  Exiting.

Invalid MIT-MAGIC-COOKIE-1 key 오류는 X11 디스플레이 서버에 대한 인증 문제로 발생할 수 있습니다. 이 문제를 해결하려면 다음 단계를 수행하세요.

1. xhost 명령을 통해 디스플레이 권한 설정

디스플레이 권한을 설정하여 pi 사용자에게 접근을 허용

xhost +SI:localuser:pi


2. DISPLAY 환경 변수 설정

DISPLAY 환경 변수가 올바르게 설정되어 있는지 확인하세요. pi 사용자로 X 세션을 시작할 때 기본적으로 설정됩니다.

export DISPLAY=:0


3. xauth 설정 확인

X11 인증을 설정하는 xauth 명령어를 사용하여 pi 사용자의 .Xauthority 파일에서 올바른 키를 사용하도록 설정할 수 있습니다.

먼저, pi 사용자의 .Xauthority 파일에서 인증 정보를 확인합니다.

xauth list

그런 다음, root 사용자도 동일한 인증 정보를 사용하도록 설정할 수 있습니다.

sudo xauth merge ~pi/.Xauthority

이렇게 하면 root 사용자도 pi 사용자의 X 서버에 접근할 수 있습니다.


4. Chromium 실행

이제 위의 단계를 모두 완료한 후, 다시 Chromium을 실행합니다.

chromium-browser --kiosk http://127.0.0.1
```

### 이후 진행

```bash

# error
[18941:18941:0102/062758.957976:ERROR:gpu_init.cc(577)] Passthrough is not supported, GL is egl, ANGLE is 
[18941:19011:0102/062801.545420:ERROR:v4l2_utils.cc(513)] Could not open /dev/video10: Permission denied (13)


1. Passthrough is not supported (GL is egl, ANGLE is...)

이 오류는 Chromium이 GPU 가속 기능을 사용하려 할 때 발생할 수 있습니다.
이 메시지는 GPU 관련 기능이 활성화되지 않았거나 호환되지 않음을 나타내며, 보통 무시해도 괜찮습니다.
이 오류는 성능에 큰 영향을 미치지 않는 경우가 많습니다. 하지만 GPU 가속을 끄고 실행하려면 --no-sandbox 옵션을 사용할 수 있습니다.

2. Could not open /dev/video10: Permission denied (13)

이 오류는 Chromium이 /dev/video10 장치를 열려고 시도했지만 권한이 없어서 발생한 문제입니다.
/dev/video10은 비디오 장치로, 웹캠이나 다른 비디오 장치와 관련이 있을 수 있습니다.


해결 방법
1. --no-sandbox 옵션 추가 GPU와 관련된 문제는 성능에 큰 영향을 미치지 않지만,
--no-sandbox 옵션을 사용하여 일부 GPU 관련 오류를 우회할 수 있습니다.

chromium-browser --kiosk --no-sandbox http://127.0.0.1


2. 비디오 장치 권한 설정 비디오 장치에 대한 권한 문제를 해결하려면, pi 사용자에게 적절한 권한을 부여해야 합니다.
아래 명령어로 비디오 장치에 접근할 수 있는 권한을 설정해 보세요

sudo usermod -aG video pi

그런 다음, 시스템을 재부팅하여 권한 변경이 적용되도록 합니다.


3. 권한 확인 후 다시 실행 위 두 가지 해결 방법을 적용한 후, 다시 Chromium을 실행해 보세요.

chromium-browser --kiosk --no-sandbox http://127.0.0.1

# error
[19236:19236:0102/062841.451325:ERROR:gpu_init.cc(577)] Passthrough is not supported, GL is egl, ANGLE is 


4. GPU 가속 비활성화: GPU 가속이 필요하지 않다면, --disable-gpu 옵션을 추가하여 GPU 가속을 완전히 비활성화할 수 있습니다.

chromium-browser --kiosk --no-sandbox --disable-gpu http://127.0.0.1


```
