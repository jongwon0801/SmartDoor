#### git 설치
```less
sudo apt update

sudo apt install git

git --version
```


#### 저장소용 사용자/폴더 준비
```less
# git 사용자 생성(비번 x)
sudo adduser git

pw : wiki6564

# 비번변경
sudo passwd git (root 권한 있는 계정으로)

# 저장소 폴더 생성
sudo mkdir -p /home/git/repos
sudo chown git:git /home/git/repos
```

#### git 계정으로 bare repository 생성
```less
# git 계정으로 전환
sudo -u git -i

# 저장소 폴더 생성
mkdir -p ~/repos
cd ~/repos

# 새 저장소 생성 
git init --bare smartdoor_origin.git

# 나가기
exit
```

#### rsync.sh 생성
```less
# 김대표 서버에서 www 소스 로컬 서버로 다운
rsync -e 'ssh -p 6001' -avzh --delete \
  --exclude="www/vod/*" --exclude="*.json" \
  hizib@101.101.162.43:/home/hizib/kiosk/* /home/hizib/www/
```

#### 1. hizib 계정으로 로그인 후 /home/hizib/www에서 Git 초기화
```less
sudo su hizib

cd /home/hizib/www
git init
git add ./*
git commit -m "initial commit"

# 브랜치 확인
git branch

# 모든 브랜치와 커밋 참조를 확인
git show-ref
```

#### 2. bare repository를 원격으로 추가
```less
git remote add origin git@localhost:/home/git/repos/smartdoor_origin.git
```

#### 3. push
```less
git push -u origin master
```

#### 다른 클라이언트에서 다운
```less
# 깃 클라이언트에 설치
sudo apt update
sudo apt install git -y
git --version   

# 내려받을 폴더로 이동 클론 (맨뒤에 폴더 지정가능)
git clone git@192.168.0.73:/home/git/repos/smartdoor_origin.git www
```




















