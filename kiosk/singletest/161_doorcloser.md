#### 오토락 X, 문 open, 잠금 X 응답

#### 도어락 조회
```bash
workon elcsoft

cd ~/www/python

python doorcloser.py doorcloserOpen -p "21"
```
#### 결과

```bash
잠김상태:해제상태
센서상태:열림상태
베터리상태:정상
{"result": {"isDoorlock": true, "isDooropen": true, "battery": true}}
```
