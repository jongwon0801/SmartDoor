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
    libsm-dev \
    libxext-dev \
    libgtk-3-dev \
    libboost-python-dev \
    libboost-thread-dev \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 과학 계산 및 이미지/AI 관련 라이브러리 설치 (핵심 수정!)
# python3-opencv 추가: ARM에서 opencv-python 컴파일 문제를 해결
# python3-dlib 추가: dlib도 apt로 설치 시도 (없으면 다음 단계에서 pip 시도)
RUN apt-get update && apt-get install -y \
    libblas-dev \
    liblapack-dev \
    python3-numpy \
    python3-scipy \
    python3-opencv \ # 이 줄을 추가합니다.
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# requirements.txt 복사
COPY requirements.txt /app/

# pip 업그레이드 및 빌드 도구 설치
RUN pip install --upgrade pip
RUN pip install --no-cache-dir setuptools wheel setuptools_rust

# !!!!! 중요 수정 !!!!!
# requirements.txt에서 apt-get으로 설치하는 패키지들을 모두 제외합니다.
# numpy, scipy, opencv-python, dlib, face-recognition, face-recognition-models 등
# dlib과 face-recognition은 apt-get에 없는 경우 pip로 설치해야 합니다.
# 이 경우 아래 필터링에서 dlib과 face-recognition 관련 항목을 제거해야 합니다.
RUN grep -v -E "numpy|scipy|opencv-python|dlib|face-recognition|face-recognition-models" /app/requirements.txt > /app/requirements_filtered.txt

# 필터링된 패키지 설치 (!!!! --no-deps 가 중요합니다. !!!!)
RUN pip install --no-cache-dir \
    -r /app/requirements_filtered.txt \
    --no-deps \
    --prefer-binary

# 애플리케이션 파일 복사
COPY ./www/ .

# 애플리케이션 실행
CMD ["python", "python/webserver.py"]
```
