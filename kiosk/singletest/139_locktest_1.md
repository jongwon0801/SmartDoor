#### 오토락 X, 문 open, 잠금 X 응답

#### 도어락 조회
```bash
workon elcsoft

cd ~/www/python

python hione.py isDoorOpen -p "/dev/hione"
```
#### 결과

```bash
잠김상태:해제상태
센서상태:열림상태
베터리상태:정상
{"result": {"isDoorlock": true, "isDooropen": true, "battery": true}}
```

#### 도어락 열기
```bash
workon elcsoft

cd ~/www/python

python hione.py doorOpenProcess -p "/dev/hione"
```
#### 결과

```bash
open door : 0
오픈 성공
True
[ 2025-02-21 15:08:41 ]  WIKI Smartdoor is open start!!
{"result": true}

```

#### 도어락 닫기
```bash
workon elcsoft

cd ~/www/python

python hione.py doorCloseProcess -p "/dev/hione"
```
#### 결과

```bash
open door : 0
오픈 성공
True
[ 2025-02-21 15:09:09 ]  WIKI Smartdoor is open start!!
{"result": true}

```






