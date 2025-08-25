#### 주소 추가
```less
# Loads default set of integrations. Do not remove.
default_config:

# Load frontend themes from the themes folder
frontend:
  themes: !include_dir_merge_named themes

# HTTP 및 CORS 설정
http:
  cors_allowed_origins:
    - "http://127.0.0.1"
    - "http://localhost"
    - "http://192.168.0.42"

automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml
```
#### 도커 재시작
```less
# 도커 컴포즈 재시작 (플러그인 방식)
docker compose restart homeassistant
```

#### 접속주소
```less
http://192.168.0.42:8123/lovelace/0
```




