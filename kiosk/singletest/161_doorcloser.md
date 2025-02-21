#### 오토락 X, 문 open, 잠금 X 응답

#### 도어락 조회
```bash
workon elcsoft

cd ~/www/python

python doorcloser.py doorcloserOpen -p "21"

python doorcloser.py doorSafeModeProcess -p "15"
```

#### 결과

```bash
doorcloserOpen는 도어락오픈 후 문열기 명령

doorSafeModeProcess는 문 닫히는 과정에 안전모드로 문열림 명령
```
