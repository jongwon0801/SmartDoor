#### pir 테스트

SUBSYSTEM=="tty", ATTRS{idVendor}=="04d8", ATTRS{idProduct}=="000a", SYMLINK+="ttyUSB_PIR"


udevadm info

udevadm info -a -n /dev/ttyUSB_PIR

Bus 001 Device 009: ID 04d8:000a Microchip Technology, Inc. CDC RS-232 Emulation Demo
Bus 001 Device 010: ID 04d8:000a Microchip Technology, Inc. CDC RS-232 Emulation Demo









