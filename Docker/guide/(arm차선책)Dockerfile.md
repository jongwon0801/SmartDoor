#### ARM 아키텍처에 최적화된 Python 3.9 slim 이미지 사용
```less
FROM --platform=linux/arm64 python:3.9-slim

WORKDIR /app/www

# 시스템 의존성 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgtk-3-dev \
    python3-dev \
    libblas-dev \
    liblapack-dev \
    gcc \
    gfortran \
    pkg-config \
    python3-numpy \
    python3-scipy \
    libffi-dev \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# requirements.txt 복사
COPY requirements.txt /app/

# pip 업그레이드 및 빌드 도구 설치
RUN pip install --upgrade pip
RUN pip install --no-cache-dir setuptools wheel

# requirements.txt에서 NumPy와 SciPy를 제외하고 새 파일 생성
RUN grep -v "numpy\|scipy" /app/requirements.txt > /app/requirements_filtered.txt

# 필터링된 패키지 설치
RUN pip install --no-cache-dir \
    -r /app/requirements_filtered.txt \
    --no-deps \
    --no-build-isolation \
    --prefer-binary

# 애플리케이션 파일 복사
COPY ./www/ .

# 애플리케이션 실행
CMD ["python", "python/webserver.py"]
```
