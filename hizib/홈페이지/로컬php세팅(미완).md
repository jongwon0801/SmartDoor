#### map 파일 경로

```less
grep -r "map" /Users/jongwon/test/home

/Users/jongwon/test/home/plugin/editor/cheditor5/popup/js/google_map.js
```

#### 로컬에서 php 파일 확인

```less
# vscode에서 php 서버 로컬로 실행

# 버젼확인
php -v

# php brew로 설치 (7.3 이하로 해야함)
brew tap shivammathur/php

brew install shivammathur/php/php@7.3

# PATH 설정
echo 'export PATH="/opt/homebrew/opt/php@7.3/bin:$PATH"' >> ~/.zshrc
echo 'export PATH="/opt/homebrew/opt/php@7.3/sbin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# mysql 설치
brew uninstall mysql
brew install mysql@8.0
brew services start mysql@8.0

# 경로 설정
echo 'export PATH="/opt/homebrew/opt/mysql@8.0/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# mysql 중지
brew services stop mysql

# 비밀번호 없이 MySQL 서버 시작 (안전모드)
sudo mysqld_safe --skip-grant-tables &

# 로컬 php 서버 실행
php -S localhost:8000
```
