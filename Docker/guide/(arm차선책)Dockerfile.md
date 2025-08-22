#### ARM 아키텍처에 최적화된 Python 3.9 slim 이미지 사용
```less
FROM python:3.9-slim

WORKDIR /app/www

# 필수 기본 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libffi-dev \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 컴파일러 및 빌드 도구 설치
RUN apt-get update && apt-get install -y \
    cmake \
    gcc \
    gfortran \
    pkg-config \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 과학 계산 라이브러리 설치 (NumPy 문제 해결을 위한 핵심 부분)
RUN apt-get update && apt-get install -y \
    libblas-dev \
    liblapack-dev \
    python3-numpy \
    python3-scipy \
    libatlas-base-dev \  
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# requirements.txt 복사
COPY requirements.txt /app/

# pip 업그레이드 및 빌드 도구 설치
RUN pip install --upgrade pip
RUN pip install --no-cache-dir setuptools wheel setuptools_rust

# requirements.txt에서 NumPy와 SciPy를 제외하고 새 파일 생성
RUN grep -v "numpy\|scipy" /app/requirements.txt > /app/requirements_filtered.txt

# 필터링된 패키지 설치 (--prefer-binary 플래그 강조)
RUN pip install --no-cache-dir \
    -r /app/requirements_filtered.txt \
    --prefer-binary \
    --no-build-isolation

# 애플리케이션 파일 복사
COPY ./www/ .

# 애플리케이션 실행
CMD ["python", "python/webserver.py"]]
```
