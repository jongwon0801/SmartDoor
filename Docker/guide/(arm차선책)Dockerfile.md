#### ARM 아키텍처에 최적화된 Python 3.9 slim 이미지 사용
```less
FROM arm64v8/python:3.9-slim

WORKDIR /app/www

# 시스템 의존성 패키지 설치
# build-essential, cmake, gcc, gfortran, pkg-config: 컴파일 도구
# python3-dev: Python 개발 헤더 (Python C API 사용 시 필요)
# libsm6, libxext6, libxrender-dev, libgtk-3-dev: (GUI/이미지 처리 라이브러리 사용 시 필요)
# libblas-dev, liblapack-dev: 과학 계산 라이브러리(NumPy, SciPy)의 저수준 의존성
# python3-numpy, python3-scipy: 시스템 패키지 매니저를 통해 미리 컴파일된 NumPy/SciPy 설치
# libffi-dev: cffi 컴파일에 필요한 라이브러리
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

# --- 변경된 부분: NumPy만 제외하고, cffi는 requirements.txt를 따르도록! ---
# requirements.txt에서 NumPy만 제외하고 새 파일 생성
# (apt-get으로 설치한 python3-numpy가 사용되도록 유도)
RUN grep -v "numpy" /app/requirements.txt > /app/requirements_filtered.txt

# 필터링된 패키지 설치 (cffi 포함)
# --no-deps 옵션을 사용해서 다른 패키지들의 잠재적 의존성 충돌 방지
# 단, requirements.txt에 cffi==1.15.1 (혹은 호환되는 다른 버전)로 수정되어 있다고 가정합니다.
RUN pip install --no-cache-dir -r /app/requirements_filtered.txt --no-deps

# 애플리케이션 파일 복사
COPY ./www/ .

# 애플리케이션 실행
CMD ["python", "python/webserver.py"]
```
