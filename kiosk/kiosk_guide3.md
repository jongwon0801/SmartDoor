### 설치 에러 모음

```bash
1. error
ERROR: Could not find a version that satisfies the requirement virtualenv==20.4.0+ds
ERROR: No matching distribution found for virtualenv==20.4.0+ds

# 가상환경 업그래이드
pip install --upgrade virtualenv

2. error
ERROR: THESE PACKAGES DO NOT MATCH THE HASHES FROM THE REQUIREMENTS FILE. If you have updated the package versions, please update the hashes. Otherwise, examine the package contents carefully; someone may have tampered with them.
    virtualenv from https://www.piwheels.org/simple/virtualenv/virtualenv-20.26.6-py3-none-any.whl#sha256=7345cc5b25405607a624d8418154577459c3e0277f5466dd79c49d5e492995f2 (from virtualenvwrapper==4.8.4->-r requirements1.txt (line 119)):
        Expected sha256 7345cc5b25405607a624d8418154577459c3e0277f5466dd79c49d5e492995f2
             Got        1003d35a2867d310d211be03e198533a5ae4012fcb2f0f80836619fab08fc9c9

# 캐시삭제
sudo python3 -m pip cache purge

pip install virtualenvwrapper


3. error: metadata-generation-failed

sudo apt-get install python-dev

sudo apt-get install build-essential

# 필요한 종속성을 설치
sudo apt-get update
sudo apt-get install build-essential python3-dev qt5-qmake qtbase5-dev libqt5gui5 libqt5widgets5

# SIP 및 PyQt5-sip 설치
pip install sip pyqt5-sip

# libsmbclient 개발 패키지 설치
sudo apt-get install libsmbclient-dev
python3 -m pip install pysmbc==1.0.23






```
