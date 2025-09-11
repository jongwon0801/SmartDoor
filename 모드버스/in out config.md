#### in out config
```less
# 기본 설정
default_config:

# 프론트엔드 테마 설정
frontend:
  themes: !include_dir_merge_named themes

# 모드버스 설정
modbus:
  - name: modbus_hub
    type: serial
    port: /dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AK3XEFC4-if00-port0
    baudrate: 9600
    bytesize: 8
    method: rtu
    parity: N
    stopbits: 1
    
    # 출력 스위치 설정
    switches:
      - name: "OUT 1"
        slave: 1
        address: 0
        write_type: holding
        command_on: 0x0100
        command_off: 0x0200
        
      - name: "OUT 2"
        slave: 1
        address: 1
        write_type: holding
        command_on: 0x0100
        command_off: 0x0200
        
      - name: "OUT 8"
        slave: 1
        address: 7
        write_type: holding
        command_on: 0x0100
        command_off: 0x0200
    
    # 입력 센서 설정
    sensors:
      - name: "IN 1"
        slave: 1
        address: 192
        input_type: holding
        data_type: uint16
        scan_interval: 1

# 자동화 설정
automation:
  # IN 1 센서가 켜지면 OUT 1 켜기
  - alias: "IN 1 센서가 켜지면 OUT 1 켜기"
    trigger:
      - platform: numeric_state
        entity_id: sensor.in_1
        above: 0  # 값이 0보다 크면 (입력이 감지되면)
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.out_1

  # IN 1 센서가 꺼지면 OUT 1 끄기
  - alias: "IN 1 센서가 꺼지면 OUT 1 끄기"
    trigger:
      - platform: numeric_state
        entity_id: sensor.in_1
        below: 1  # 값이 1 미만이면 (입력이 없으면)
    action:
      - service: switch.turn_off
        target:
          entity_id: switch.out_1

# 스크립트, 씬 설정
script: !include scripts.yaml
scene: !include scenes.yaml
```

