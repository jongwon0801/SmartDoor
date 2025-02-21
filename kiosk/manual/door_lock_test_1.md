#### 오토락 해제, 문 닫혀있음, 잠금 해제 상태일 때 응답

#### 도어락 조회
```bash
python hione.py isDoorOpen -p "/dev/ttyUSB0"
```
#### 결과

```bash
잠김상태:해제상태
센서상태:닫힘상태
베터리상태:정상
{"result": {"isDoorlock": true, "isDooropen": false, "battery": true}}
```

#### 도어락 열기
```bash
python hione.py doorOpenProcess -p "/dev/ttyUSB0"
```
#### 결과

```bash
open door : 0
오픈 성공
True
[ 2025-02-21 14:55:20 ]  WIKI Smartdoor is open start!!
{"result": true}
```

#### 도어락 닫기
```bash
python hione.py doorCloseProcess -p "/dev/ttyUSB0"
```
#### 결과

```bash
open door : 0
오픈 성공
True
[ 2025-02-21 14:57:31 ]  WIKI Smartdoor is open start!!
{"result": true}
```






