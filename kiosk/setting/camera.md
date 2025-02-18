### 카메라 단일 테스트

#### 카메라 레즈베리파이 연결 체크

- https://webrtc.github.io/samples/  ->  Choose camera resolution  ->  Video source 에서 카메라 테스트

```bash

# 연결된 usb 디바이스를 확인

cd /dev/

lsusb

# 외부 카메라
Bus 001 Device 009: ID 0c45:0415 Microdia USB 4K Live Camera

# 내부 카메라
Bus 001 Device 012: ID 1e45:8022 Suyin HD Camera
```

```bash
sudo nano ~/www/python/config.json

# 외부 카메라
"outsideCamDeviceName": "USB 4K Live Camera"

# 내부 카메라
"insideCamDeviceName": "HD Camera", 


```
