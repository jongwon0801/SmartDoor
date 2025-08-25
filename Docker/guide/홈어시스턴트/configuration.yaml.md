#### 원래 config
```less
# Loads default set of integrations. Do not remove.
default_config:

# Load frontend themes from the themes folder
frontend:
  themes: !include_dir_merge_named themes
  trusted_proxies:
    - 127.0.0.1
    - localhost
    - 192.168.0.42

automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml
```

#### 접속주소
```less
http://192.168.0.42:8123/lovelace/0
```




