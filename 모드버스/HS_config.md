#### configration.yaml
```less
# 기본 설정 (기존 설정이 있다면 유지)
default_config:

# 프론트엔드 테마 설정
frontend:
  themes: !include_dir_merge_named themes

# HTTP 설정
http:
  cors_allowed_origins:
    - "http://192.168.0.3"
    - "http://127.0.0.1"
    - "http://localhost"
    - "http://192.168.0.42"
    - "http://192.168.1.3"

# 모드버스 허브 설정 (센서 정의 제외)
modbus:
  - name: "modbus_hub"
    type: serial
    method: rtu
    port: /dev/ttyUSB0
    baudrate: 9600
    stopbits: 1
    bytesize: 8
    parity: N

# 자동화, 스크립트, 씬 설정
automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml
```

#### ttyUSB 존재 확인
```less
ls -l /dev/ttyUSB0

dmesg | grep ttyUSB

[    5.541264] usb 1-1.1.2: FTDI USB Serial Device converter now attached to ttyUSB0
```

#### Home Assistant가 /dev/ttyUSB0에 접근할 수 있도록 권한을 설정
```less
root 면 안해도됨
```




