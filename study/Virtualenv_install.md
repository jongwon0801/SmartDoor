
## 1. Virtualenv 및 Virtualenvwrapper 설치

```bash
sudo apt update
sudo apt install python3-pip
pip3 install virtualenv virtualenvwrapper
```

## 2. 환경 변수 및 스크립트 설정
```bash
WORKON_HOME 환경 변수 설정:
가상 환경이 저장될 디렉토리 설정입니다. 기본적으로 ~/.virtualenvs로 지정됩니다.
다음 명령어를 ~/.profile, ~/.bashrc 또는 ~/.zshrc에 추가합니다:

export WORKON_HOME=$HOME/.virtualenvs
mkdir -p $WORKON_HOME  # 디렉토리가 없으면 생성

Virtualenvwrapper 스크립트 로드:
아래 명령어를 동일한 파일에 추가합니다:

source /usr/local/bin/virtualenvwrapper.sh
```

## 3. 설정 파일 적용
```bash
변경 내용을 즉시 적용:
source ~/.profile  # 또는 source ~/.bashrc / source ~/.zshrc

재부팅
변경 사항을 영구적으로 적용하려면:

sudo reboot

가상 환경들이 저장될 디렉터리를 정의, 환경 변수가 설정된 경로를 출력하는 명령

echo $WORKON_HOME  WORKON_HOME 

```
## 4. 가상 환경 생성 및 활성화
```bash
가상 환경 생성:
mkvirtualenv elcsoft

가상 환경 활성화:
workon elcsoft
```
