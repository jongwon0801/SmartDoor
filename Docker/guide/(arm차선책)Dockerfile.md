#### 설치 가능한 패키지 미리 설치
```less
# apt 전역 설치
numpy, scipy, opencv-python은 apt-get을 통해 시스템 패키지로 설치

# numpy, scipy, opencv-python 의존성 필요한 패키지 뺴고 먼저 설치
dlib, face-recognition, face-recognition-models, cryptography를 제외 하고 설치
```

```less
FROM python:3.9-slim

WORKDIR /app/www

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libffi-dev \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    cmake \
    gcc \
    gfortran \
    pkg-config \
    libsm-dev \
    libxext-dev \
    libgtk-3-dev \
    libboost-python-dev \
    libboost-thread-dev \
    rustc \
    cargo \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    libblas-dev \
    liblapack-dev \
    python3-numpy \
    python3-scipy \
    python3-opencv \ 
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir setuptools wheel setuptools_rust

# 먼저 cryptography 패키지를 바이너리로 설치 시도
RUN pip install --no-cache-dir --only-binary=:all: cryptography==41.0.7 || true

RUN grep -v -E "numpy|scipy|opencv-python|dlib|face-recognition|face-recognition-models|cryptography" /app/requirements.txt > /app/requirements_filtered.txt

RUN pip install --no-cache-dir \
    -r /app/requirements_filtered.txt \
    --no-deps \
    --prefer-binary

COPY ./www/ .

CMD ["python", "python/webserver.py"]
```


#### 상단 패키지 설치 완료 이후 누락된 패키지 설치
```less
dlib, face-recognition, face-recognition-models,
cryptography 설치위해서 (libssl-dev 추가)

RUN에 패키지 추가하면 이후 패키지들도 캐싱안하고 처음부터 빌드한다
```

```less
FROM python:3.9-slim

WORKDIR /app/www

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libffi-dev \
    libssl-dev \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    cmake \
    gcc \
    gfortran \
    pkg-config \
    libsm-dev \
    libxext-dev \
    libgtk-3-dev \
    libboost-python-dev \
    libboost-thread-dev \
    rustc \
    cargo \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    libblas-dev \
    liblapack-dev \
    python3-numpy \
    python3-scipy \
    python3-opencv \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir setuptools wheel setuptools_rust

# cryptography 패키지 설치 (버전 지정)
RUN pip install --no-cache-dir cryptography==41.0.7
RUN pip install dlib==20.0.0

# 필터링: numpy, scipy, opencv-python, dlib, face-recognition, face-recognition-models, cryptography 제외
RUN grep -v -E "numpy|scipy|opencv-python|dlib|face-recognition|face-recognition-models|cryptography" /app/requirements.txt > /app/requirements_filtered.txt

# 필터링된 requirements 설치 (의존성 설치 없이)
RUN pip install --no-cache-dir \
    -r /app/requirements_filtered.txt \
    --no-deps \
    --prefer-binary

# dlib과 face-recognition 관련 패키지 별도 설치 (버전 지정 및 의존성 설치 없이)
RUN pip install --no-cache-dir --no-deps face-recognition-models==0.3.0 face-recognition==1.3.0
RUN pip install --no-cache-dir opencv-python-headless

COPY ./www/ .

CMD ["python", "python/webserver.py"]
```



#### docker-compose.yml (디바이스 경로추가)
```less
version: '3'
services:
  tornado:
    build: .
    container_name: smartdoor_app
    privileged: true  # 하드웨어 접근 권한 부여 (거의 필수적입니다)
    ports:
      - "8080:8080"  
    restart: unless-stopped
    volumes:
      # 애플리케이션 코드 마운트
      - ./www:/app/www

      # 설정 파일 마운트 (읽기 전용: :ro)
      - "/boot/config.txt:/boot/config.txt:ro"
      - "/etc/udev/rules.d/99-com.rules:/etc/udev/rules.d/99-com.rules:ro"
      - "/usr/share/X11/xorg.conf.d/40-libinput.conf:/usr/share/X11/xorg.conf.d/40-libinput.conf:ro"
      
    # udev 규칙에 따라 생성되는 심볼릭 링크 디바이스들을 컨테이너에 마운트
    # /dev/input/event* 에 대한 접근을 위해서 /dev/input도 필요할 수 있습니다.
    # KERNELS=="fe201a00.serial" -> /dev/hione (UART5)
    # X11 libinput에서 필요할 수 있는 입력 디바이스들
    devices:
      - "/dev/ttyUSB_PIR:/dev/ttyUSB_PIR"
      - "/dev/hione:/dev/hione" 
      - "/dev/cam_inside:/dev/cam_inside"
      - "/dev/cam_outside:/dev/cam_outside"
      - "/dev/input:/dev/input"

    # (필요한 경우) 호스트 네트워크 모드 사용 (일부 디바이스 통신에 유용할 수 있음)
    # network_mode: "host" 
```

