#### 도어락 doorOpenProcess, doorCloseProcess 결과

```bash
닫혔을때 unlock 명령
{"request": "/Smartdoor/doorOpenAtWebProcess", "data": {"result": true}, "response": "doorOpened"}

열렸을때 unlock 명령
{"request": "/Smartdoor/doorOpenAtWebProcess", "data": {"result": true, "isDoorOpen": true}, "response":
"doorAlreadyOpened"}
```

```bash
닫혔을때 lock 명령 (auto lock x 인 경우)
{"request": "/Smartdoor/doorCloseAtWebProcess", "data": {"result": true}, "response": "doorClosed"}

이미 lock 일떄 lock 명령
{"request": "/Smartdoor/doorCloseAtWebProcess", "data": {"result": true, "isDoorOpen": false}, "response":
"doorAlreadyClosed"}
```

```bash
열렸을때 lock 명령 
{"request": "/Smartdoor/doorCloseAtWebProcess", "data": {"result": true}, "response": "doorClosed"}
```
