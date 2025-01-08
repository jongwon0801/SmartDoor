#### 압축

tar -czvf kiosk.tar.gz Bookshelf Downloads Public Videos css image json nohup.out reversessh.log.save screen.sh temp.txt 
www Music README.md Workspace font index.html log python reversesshservice.sh shell test Documents Pictures Templates click html
js logview.sh reversessh.log rsync.sh sound test.html


#### sftp 명령어로 압축파일 전송
```bash
sftp pi@192.168.0.161

get /home/pi/kiosk.tar.gz /home/pi

# 현재 경로에 압축해제
tar -xzvf kiosk.tar.gz -C /home/pi


```

#### 
