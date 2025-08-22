#### ARM 아키텍처에 최적화된 Python 3.9 slim 이미지 사용
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
