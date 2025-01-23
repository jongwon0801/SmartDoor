#### sudo nano /etc/udev/rules.d/99-com.rules

```bash

# 192.168.0.161 부산

# PWM export results in a "change" action on the pwmchip device (not "add" of a new device), so match actions other t>
SUBSYSTEM=="pwm", ACTION!="remove", PROGRAM="/bin/sh -c 'chgrp -R gpio /sys%p && chmod -R g=u /sys%p'"
# default 상태에서 두줄 추가
SUBSYSTEM=="tty", ATTRS{idVendor}=="1d6b", ATTRS{idProduct}=="0002", SYMLINK+="hione"
SUBSYSTEM=="tty", ATTRS{idVendor}=="04d8", ATTRS{idProduct}=="000a", SYMLINK+="ttyUSB_PIR"

# 192.168.0.139 회사

# PWM export results in a "change" action on the pwmchip device (not "add" of a new device), so match actions other th>
SUBSYSTEM=="pwm", ACTION!="remove", PROGRAM="/bin/sh -c 'chgrp -R gpio /sys%p && chmod -R g=u /sys%p'"
SUBSYSTEM=="tty", ATTRS{idVendor}=="04d8", ATTRS{idProduct}=="000a", SYMLINK+="ttyUSB_PIR"
SUBSYSTEM=="video4linux", SUBSYSTEMS=="usb", ATTRS{idVendor}=="1e45", ATTRS{idProduct}=="8022", SYMLINK+="cam_inside"
SUBSYSTEM=="video4linux", SUBSYSTEMS=="usb", ATTRS{idVendor}=="0c45", ATTRS{idProduct}=="0415", SYMLINK+="cam_outside">

# uart-5 의 attribute
KERNELS=="fe201a00.serial", SYMLINK+="hione"


```
