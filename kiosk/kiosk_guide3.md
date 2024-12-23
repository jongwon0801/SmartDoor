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

4. ERROR: Ignored the following yanked versions: 0.0.0, 0.7.8
ERROR: Ignored the following versions that require a different python version: 1.9.5 Requires-Python >=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <3.7; 2.1.0 Requires-Python >=3.10; 2.1.0rc1 Requires-Python >=3.10; 2.1.1 Requires-Python >=3.10; 2.1.2 Requires-Python >=3.10; 2.1.3 Requires-Python >=3.10; 2.2.0 Requires-Python >=3.10; 2.2.0rc1 Requires-Python >=3.10; 2.2.1 Requires-Python >=3.10
ERROR: Could not find a version that satisfies the requirement python-apt==2.2.1 (from versions: none)
ERROR: No matching distribution found for python-apt==2.2.1


sudo apt-get install python3-apt


5. 이 오류는 python-prctl 패키지를 설치하려고 할 때, libcap 개발 헤더가 부족하다는 문제
Preparing metadata (setup.py) ... error
  error: subprocess-exited-with-error
  
  × python setup.py egg_info did not run successfully.
  │ exit code: 1
  ╰─> [1 lines of output]
      You need to install libcap development headers to build this module
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
error: metadata-generation-failed


sudo apt-get install libcap-dev

6. Collecting pygame<2.0,>=1.9.2 (from pgzero==1.2->-r requirements1.txt (line 56))
  Using cached pygame-1.9.6.tar.gz (3.2 MB)
  Preparing metadata (setup.py) ... error
  error: subprocess-exited-with-error
  
  × python setup.py egg_info did not run successfully.
  │ exit code: 1
  ╰─> [18 lines of output]
      
      
      WARNING, No "Setup" File Exists, Running "buildconfig/config.py"
      Using UNIX configuration...
      
      Missing dependencies
      
      Hunting dependencies...
      SDL     : found 1.2.15
      FONT    : not found
      IMAGE   : not found
      MIXER   : not found
      PNG     : found
      JPEG    : found
      SCRAP   : found
      PORTMIDI: not found
      PORTTIME: not found
      FREETYPE: found 23.4.17

sudo apt-get install libsdl1.2-dev
sudo apt-get install libsdl-mixer1.2-dev
sudo apt-get install libsdl-image1.2-dev
sudo apt-get install libsdl-ttf2.0-dev
sudo apt-get install libportmidi-dev
sudo apt-get install libfreetype6-dev

6. INFO: pip is looking at multiple versions of thonny to determine which version is compatible with other requirements. This could take a while.
ERROR: Cannot install -r requirements1.txt (line 106) and jedi==0.18.0 because these package versions have conflicting dependencies.

The conflict is caused by:
    The user requested jedi==0.18.0
    thonny 4.0.1 depends on jedi>=0.18.1

To fix this you could try to:
1. loosen the range of package versions you've specified
2. remove package versions to allow pip to attempt to solve the dependency conflict

ERROR: ResolutionImpossible: for help visit https://pip.pypa.io/en/latest/topics/dependency-resolution/#dealing-with-dependency-conflicts


pip install jedi==0.18.0
pip install thonny==4.0.1


7.

pip install pygame==1.9.6

sudo apt install -y build-essential python3-dev libffi-dev libjpeg-dev libfreetype6-dev libsdl1.2-dev libportmidi-dev libasound2-dev

sudo apt install python3-rpi.gpio
pip install pycups
pip install RTIMULib

sudo apt install libcups2-dev

pip install pycups

sudo apt install libboost-all-dev

sudo apt install cmake

pip install RPi.GPIO

sudo apt install python3-rpi.gpio

python3 -m pip install --upgrade pip setuptools wheel





```
