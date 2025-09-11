#### in out config
```less
# 기본 설정 (기존 설정이 있다면 유지)
default_config:

# 프론트엔드 테마 설정
frontend:
  themes: !include_dir_merge_named themes

modbus:
  - name: modbus_hub
    type: serial
    port: /dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AK3XEFC4-if00-port0
    baudrate: 9600
    bytesize: 8
    method: rtu
    parity: N
    stopbits: 1
    
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
        
      - name: "OUT 3"
        slave: 1
        address: 2
        write_type: holding
        command_on: 0x0100
        command_off: 0x0200
    
    binary_sensors:
      - name: "IN 1"
        slave: 1
        address: 192
        input_type: holding
        bit_number: 0
        scan_interval: 10
        device_class: signal

# 자동화, 스크립트, 씬 설정 (나머지는 그대로 유지)
automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml
```

