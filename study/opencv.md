## OpenCV가 설치되었는지 확인

```python

# 터미널에서 Python 인터프리터 실행
python

# Python 인터프리터에서 아래 코드 입력
import cv2
print(cv2.__version__)

- OpenCV가 설치되어 있다면 설치된 OpenCV 버전이 출력됩니다. 
4.10.0

- OpenCV가 설치되지 않았거나 문제가 있으면 오류 메시지가 출력됩니다. 

ModuleNotFoundError: No module named 'cv2'

```

#### pip list로 확인
```bash
pip list | grep opencv

ex)
opencv-contrib-python 4.10.0.84
opencv-python         4.10.0.84
```

#### pip show로 특정 패키지 확인
```bash
pip show opencv-python

ex)
Name: opencv-python
Version: 4.9.0
```
#### 파일 시스템에서 확인 (설치된 경로에서 직접 확인)

```bash
find / -name "cv2*.so"
```
#### opencv 설치 명령어
```bash
pip install opencv-python==4.9.0

```

#### cash 삭제
```bash
pip cache purge
```

#### pi@192.168.0.161 / elcsoft (kiosk) 버젼 확인 후 설치
```bash
pip install opencv-python==4.9.0.80

Raspberry Pi 환경에서는 최신 버전 대신 안정적인 이전 버전을 사용하는 것이 좋습니다.
```

