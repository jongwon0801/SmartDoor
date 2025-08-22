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

# cryptography 패키지 설치 - 이전에는 || true로 실패를 무시했지만 이제 제대로 설치
RUN pip install --no-cache-dir cryptography==41.0.7

# 필터에서 dlib, face-recognition 관련 패키지를 제외하지 않도록 수정
# 시스템 패키지로 이미 설치된 numpy, scipy, opencv-python만 제외
RUN grep -v -E "numpy|scipy|opencv-python" /app/requirements.txt > /app/requirements_filtered.txt

# 필터링된 requirements 설치
RUN pip install --no-cache-dir \
    -r /app/requirements_filtered.txt \
    --prefer-binary

# dlib과 face-recognition 관련 패키지를 명시적으로 설치
RUN pip install --no-cache-dir dlib face-recognition face-recognition-models

COPY ./www/ .

CMD ["python", "python/webserver.py"]
```





