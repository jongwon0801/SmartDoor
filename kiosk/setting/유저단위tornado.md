#### pi 유저로 ssh 로그인
```less
✅ 1. sudo su -l pi

의미:
root 권한으로 pi 사용자 로그인 셸을 엽니다. -l은 로그인 셸을 의미하여, 마치 pi로 로그인한 것처럼 환경 변수까지 모두 설정합니다.

왜 사용하는가:
SSH나 sudo 세션에서는 일반적으로 pi 사용자의 systemd user 서비스 환경(DBus 등) 이 완전히 초기화되지 않기 때문에, 제대로 된 환경을 갖춘 셸로 진입하기 위해 사용합니다.
```

```less
✅ 2. echo $DBUS_SESSION_BUS_ADDRESS

의미:
현재 사용자 세션의 DBus 주소를 출력합니다.
unix:path=/run/user/1000/bus

이 값이 있다는 뜻은, 현재 pi 유저의 user-level systemd 서비스를 제어할 수 있다는 뜻입니다.

❗ 이 값이 없으면 systemctl --user는 작동하지 않습니다.
```

```less
✅ 3. export XDG_RUNTIME_DIR=/run/user/$(id -u)

의미:
XDG_RUNTIME_DIR은 systemd --user 및 많은 데스크탑/세션 환경에서 세션 임시 파일 경로로 사용되는 환경변수입니다.

$(id -u)는 현재 사용자(pi)의 UID를 반환합니다. 보통 1000.

따라서 이 명령은 아래와 같아집니다:
export XDG_RUNTIME_DIR=/run/user/1000

왜 필요한가:
어떤 경우에는 XDG_RUNTIME_DIR이 자동으로 설정되지 않아서, systemctl --user가 작동하지 않습니다.
DBUS_SESSION_BUS_ADDRESS와 함께 둘 다 필요한 경우가 많습니다.
```

```less
✅ 4. systemctl --user status tornado.service

의미:
현재 로그인한 유저 (pi)의 user-level systemd 서비스 중 tornado.service의 상태를 확인합니다.

이 명령은 오직:

DBUS_SESSION_BUS_ADDRESS와

XDG_RUNTIME_DIR
가 설정된 환경에서만 정상 작동합니다.
```

🧪 **pi 사용자 환경 진입 및 PulseAudio 관련 확인 절차**

| 명령어 | 설명 |
|--------|------|
| `sudo su -l pi` | **진짜 pi 사용자 로그인 환경**으로 진입 (login shell) |
| `echo $DBUS_SESSION_BUS_ADDRESS` | DBus 세션 주소 확인 (세션 존재 여부 확인) |
| `export XDG_RUNTIME_DIR=/run/user/1000` | 런타임 디렉토리 수동 설정 (필요 시) |
| `systemctl --user status pulseaudio` | **pi 유저의 PulseAudio 서비스 상태 확인** |












