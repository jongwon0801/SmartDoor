### -m 옵션 설명

```bash
python -m은 Python 명령어에서 특정 모듈을 스크립트처럼 실행할 때 사용하는 옵션입니다.
즉, Python 표준 라이브러리나 설치된 패키지의 모듈을 실행할 때 유용합니다.

python -m pip install cython

환경 간 구분: 특정 Python 인터프리터에서 모듈을 실행하고자 할 때.
예: 시스템에 Python 2와 Python 3가 공존하는 경우

python3 -m pip install package_name
PATH 설정 불필요: pip가 시스템 PATH에 등록되지 않았더라도 Python 경로에서 실행 가능.

예:
python -m venv myenv

```

### --user 옵션 설명

```bash
--user는 현재 사용자의 홈 디렉토리 안에 패키지를 설치하도록 지정하는 옵션입니다.
전역(시스템 전체) 설치 권한이 없거나, 특정 사용자 환경에서만 패키지를 설치하고자 할 때 사용됩니다.

python -m pip install cython --user

주의사항:
가상환경에서 --user는 비활성화됨:

가상환경에서는 이미 환경 자체가 독립적이기 때문에 사용자 디렉토리에 설치하지 못하도록 제한합니다.
따라서 가상환경에서는 --user 옵션을 사용할 필요가 없습니다.
가상환경에서는 그냥 pip install을 사용하세요.
패키지 경로:

일반적으로 --user로 설치한 패키지는 ~/.local/lib/pythonX.X/site-packages에 저장됩니다.



```
