#### pir 테스트
```less
#sudo nano /etc/udev/rules.d/99-com.rules

SUBSYSTEM=="tty", ATTRS{idVendor}=="04d8", ATTRS{idProduct}=="000a", SYMLINK+="ttyUSB_PIR"
```

#### 디바이스 상세 속성 보기
```less
udevadm info (디바이스 경로 지정 필요)

udevadm info -a -n /dev/ttyUSB_PIR
```

#### lsusb
```less
Bus 001 Device 009: ID 04d8:000a Microchip Technology, Inc. CDC RS-232 Emulation Demo
Bus 001 Device 010: ID 04d8:000a Microchip Technology, Inc. CDC RS-232 Emulation Demo
```








