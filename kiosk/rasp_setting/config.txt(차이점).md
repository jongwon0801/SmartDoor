#### /boot/config.txt
#### 차이점

```bash
# defalut 라즈베리파이 os 설정
hdmi_force_hotplug=1: 모든 포트에 대해 HDMI 강제 활성화. 단일 포트 장치에서 주로 사용.

ex)
hdmi_force_hotplug:1=1  # HDMI 포트 1 강제 활성화
hdmi_force_hotplug:0=1  # HDMI 포트 0 강제 활성화

# 192.168.0.161 (부산), 192.168.0.139 (회사)
hdmi_force_hotplug:0=1: 다중 포트 장치에서 특정 포트(HDMI0)를 강제 활성화.



# 192.168.0.161 (부산)

[all]
gpu_mem=128

#enable_uart=1
#dtoverlay=uart0
#dtoverlay=uart1
#dtoverlay=uart2
#dtoverlay=uart3
#dtoverlay=uart4
#dtoverlay=uart5


# 192.168.0.139 (회사)

[all]
gpu_mem=128

#enable_uart=1
#dtoverlay=uart0
#dtoverlay=uart1
#dtoverlay=uart2
#dtoverlay=uart3
#dtoverlay=uart4
dtoverlay=uart5
# dtoverlay=uart5 gpio uart5 5의 기능 활성화



```
