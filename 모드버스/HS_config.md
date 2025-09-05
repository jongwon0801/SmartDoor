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

# 모드버스 설정
modbus:
  - name: "modbus_hub"
    type: serial
    method: rtu
    port: /dev/ttyUSB0
    baudrate: 9600
    stopbits: 1
    bytesize: 8
    parity: N
    sensors:
      - name: "Living Room Temperature"
        unit_of_measurement: "°C"
        slave: 1
        address: 100
        input_type: holding
        count: 1
        data_type: int16

# 디지털 입력 센서 설정 (IN1~IN8)
binary_sensor:
  - platform: modbus
    scan_interval: 1
    hub: modbus_hub
    registers:
      - name: "Input 1"
        address: 0
        input_type: discrete_input
      - name: "Input 2"
        address: 1
        input_type: discrete_input
      - name: "Input 3"
        address: 2
        input_type: discrete_input
      - name: "Input 4"
        address: 3
        input_type: discrete_input
      - name: "Input 5"
        address: 4
        input_type: discrete_input
      - name: "Input 6"
        address: 5
        input_type: discrete_input
      - name: "Input 7"
        address: 6
        input_type: discrete_input
      - name: "Input 8"
        address: 7
        input_type: discrete_input

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




