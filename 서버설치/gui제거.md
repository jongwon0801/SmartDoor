#### 현재 시스템의 기본 부팅 타겟이 무엇인지 확인
```less
systemctl get-default

graphical.target : GUI 환경으로 부팅

multi-user.target : 텍스트 모드로 부팅
```

#### text 모드로 부팅
```less
# 1. 기본 부팅 타겟을 multi-user.target으로 설정
sudo systemctl set-default multi-user.target

# 2. 기본 타겟을 변경한 후, 현재 세션에서 바로 텍스트 모드로 전환
sudo systemctl isolate multi-user.target

# 3. 재부팅 후 확인
sudo reboot
```
