<img width="506" alt="image" src="https://github.com/user-attachments/assets/018b28a1-6433-44dd-a9a8-388974db7613" /><br>
<img width="413" alt="image" src="https://github.com/user-attachments/assets/a649e837-2528-4a83-90c3-d3090b1f7a79" />



### `source /usr/share/virtualenvwrapper/virtualenvwrapper.sh`를 
### `~/.profile` 파일의 마지막에 추가하는 이유

```bash
`virtualenvwrapper`는 Python의 가상 환경을 관리하는 도구입니다. 
`source /usr/share/virtualenvwrapper/virtualenvwrapper.sh` 명령어를 `~/.profile` 파일의 마지막에 추가하는 이유는, 
이 명령어를 통해 가상 환경 관련 명령어들을 사용할 수 있도록 설정해주기 때문입니다.
```
### 이유

#### 1. 전역 설정 적용
`virtualenvwrapper.sh` 스크립트는 `virtualenv`와 관련된 명령어들을 정의합니다. 이 파일을 `~/.profile`에 추가하면 사용자가 로그인할 때마다 `virtualenvwrapper` 명령어를 사용할 수 있게 됩니다. 예를 들어, `mkvirtualenv`, `workon`, `deactivate` 등의 명령어가 이를 통해 활성화됩니다.

#### 2. 로그인 시 자동 실행
`~/.profile`은 사용자가 로그인할 때 자동으로 실행되는 파일입니다. 따라서 이 파일에 `source /usr/share/virtualenvwrapper/virtualenvwrapper.sh`를 넣으면, 사용자가 터미널을 열 때마다 가상 환경 관리 명령어들을 사용할 수 있게 됩니다.

#### 3. PATH 설정
`virtualenvwrapper.sh`는 가상 환경을 쉽게 만들고 관리할 수 있는 여러 가지 기능을 제공합니다. 이를 통해 `WORKON_HOME` 디렉토리나 `VIRTUALENVWRAPPER_PYTHON` 등의 환경 변수를 설정합니다. 이러한 설정들은 사용자가 가상 환경을 잘 관리할 수 있도록 도와줍니다.

#### 마지막에 추가하는 이유

`~/.profile` 파일에서 다른 환경 변수 설정 후 마지막에 이 명령을 추가하는 이유는, 가상 환경을 관리하는 데 필요한 설정들이 다른 설정들이 완료된 후에 적용되는 것이 바람직하기 때문입니다. 또한, 마지막에 추가하면 가독성도 좋고, 파일의 나머지 설정들과 충돌 없이 작동할 수 있습니다.
