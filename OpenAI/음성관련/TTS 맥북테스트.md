





#### 1. Coqui TTS (Mozilla TTS)

```less
1. 환경 준비
python3 -m venv tts-env
source tts-env/bin/activate
pip install --upgrade pip
pip install TTS
```
```less
2. 여자 목소리 미리 학습된 모델 다운로드 및 테스트
from TTS.api import TTS

# 모델 리스트 중에서 여성 목소리 고르기 (예: "tts_models/en/ljspeech/tacotron2-DDC")
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

# 텍스트를 wav 파일로 저장
tts.tts_to_file(text="Hello, this is a female voice test.", file_path="output.wav")
```
```less
3. wav 파일이 만들어짐

생성된 output.wav를 맥에서 바로 재생하거나, 스마트도어 프로젝트에 넣어 사용 가능
```



#### 2. macOS 기본 TTS (say 명령어) (기계음 보통, 여자음성)

```less
설치 필요 없음, macOS에 기본 내장되어 있음.

텍스트를 음성으로 바로 출력하거나 음성 파일로 저장 가능.
```

```less
음성 출력
say "Hello, this is a test"
```

```less
AIFF 음성 파일로 저장
say "Hello, this is a test" -o output.aiff
```

```less
AIFF를 WAV로 변환 (macOS 내장 afconvert 사용)
afconvert output.aiff output.wav
```

#### 3. espeak-ng (오픈소스 TTS 엔진) (기계음 심함, 남자음성)

```less
Homebrew로 설치 가능

brew install espeak
```
```less
텍스트 음성 출력

espeak "Hello world"
```

```less
WAV 파일로 저장
espeak "Hello world" --stdout > output.wav
```

#### 4. Python 라이브러리: pyttsx3 (크로스 플랫폼) (기계음 보통, 여자음성, 한글 잘 안됨)

Python에서 로컬 TTS를 쉽게 사용 가능

```less
설치

pip install pyttsx3
```

간단 사용 예제 (음성 출력)

```less
import pyttsx3

engine = pyttsx3.init()
engine.say("Hello")
engine.runAndWait()
```

pyttsx3는 wav 파일 저장 직접 지원은 없고, 음성 출력에 더 적합함.

문제 요약

```less
내가 쓴 파일 이름 pytts_test.py가

import pytts_test에서 자기 자신을 불러오고 있어서

init() 함수 같은 게 없는 자기 모듈을 참조해서 에러 발생
```

```less
해결법
pytts_test.py 파일 안에서 절대 import pytts_test 하지 말기!
```

#### 5. Google Text-to-Speech (gTTS) (기계음 낮음, 남자음성, 성별 결제해야함)
```less
pip install gTTS
```

```less
# 간단 예제 코드
from gtts import gTTS
import os

text = "안녕하세요 apple 입니다."

# 한글 텍스트, lang='ko' 꼭 넣어야 함
tts = gTTS(text=text, lang='ko')

# 음성 파일로 저장
tts.save("welcome_ko.mp3")

# 저장한 음성파일 재생 (Mac 예시)
os.system("afplay welcome_ko.mp3")  # Mac에서 mp3 재생 명령어
# Linux는: os.system("mpg123 welcome_ko.mp3") 또는 vlc, cvlc로 재생 가능
```



