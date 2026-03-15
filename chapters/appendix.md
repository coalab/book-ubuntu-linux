# 부록: 빠른 참조 가이드

> 자주 쓰는 명령어와 설정을 한눈에 확인한다

---

## A. 필수 명령어 치트시트

### 파일과 디렉토리

```bash
ls -la              # 숨김 파일 포함 상세 목록
cd ~                # 홈 디렉토리
pwd                 # 현재 위치
mkdir -p a/b/c      # 중간 디렉토리 포함 생성
cp -r src/ dst/     # 디렉토리 복사
mv old new          # 이동/이름 변경
rm -rf dir/         # 디렉토리 강제 삭제
find / -name "*.log" -mtime +7   # 7일 이상된 .log 파일
ln -s /path/target link_name    # 심볼릭 링크
```

### 파일 내용

```bash
cat file.txt        # 전체 출력
less file.txt       # 페이지 단위 보기
head -20 file.txt   # 앞 20줄
tail -f /var/log/syslog  # 실시간 로그
grep -rn "pattern" /path/   # 재귀 검색 + 행번호
grep -v "exclude" file      # 제외 패턴
awk '{print $1,$3}' file    # 1,3번째 필드
sed 's/old/new/g' file      # 치환
wc -l file          # 줄 수
```

### 권한과 사용자

```bash
chmod 755 file      # rwxr-xr-x
chmod +x script.sh  # 실행 권한 추가
chown user:group file
sudo -i             # root 쉘
id                  # 현재 사용자 정보
whoami
useradd -m -s /bin/bash username
passwd username
usermod -aG sudo username
```

### 프로세스

```bash
ps aux              # 모든 프로세스
ps aux | grep nginx
top                 # 실시간 모니터링
htop                # 개선된 top
kill -9 PID         # 강제 종료
killall nginx
pgrep -l nginx      # 프로세스 검색
nohup cmd &         # 백그라운드 실행
jobs                # 백그라운드 작업 목록
```

### 네트워크

```bash
ip addr             # IP 주소
ip route            # 라우팅 테이블
ping -c 4 8.8.8.8
traceroute google.com
ss -tlnp            # 리스닝 포트
curl -I https://example.com   # HTTP 헤더
wget https://example.com/file
netstat -an | grep ESTABLISHED
```

---

## B. systemd 명령어

```bash
# 서비스 관리
systemctl start|stop|restart|reload nginx
systemctl enable|disable nginx     # 부팅 시 자동 시작
systemctl status nginx
systemctl is-active nginx
systemctl --failed                 # 실패한 서비스 목록

# 로그
journalctl -u nginx               # 서비스 로그
journalctl -f                     # 실시간
journalctl -b                     # 현재 부팅
journalctl -p err                 # 오류 이상
journalctl --since "1 hour ago"
journalctl --vacuum-size=500M     # 로그 정리

# 타이머
systemctl list-timers
```

---

## C. APT 패키지 관리

```bash
apt update                    # 패키지 목록 갱신
apt upgrade                   # 업그레이드
apt install nginx             # 설치
apt remove nginx              # 제거 (설정 유지)
apt purge nginx               # 완전 제거
apt autoremove                # 불필요 패키지 제거
apt search keyword            # 검색
apt show nginx                # 정보
dpkg -l | grep nginx          # 설치 확인
dpkg -L nginx                 # 설치된 파일 목록
```

---

## D. UFW 방화벽

```bash
ufw status verbose
ufw enable|disable
ufw allow 80/tcp
ufw allow ssh
ufw allow from 192.168.1.0/24 to any port 22
ufw deny 23
ufw delete allow 80/tcp
ufw limit ssh                 # brute-force 방어
ufw logging on
```

---

## E. SSH

```bash
# 접속
ssh user@host
ssh -p 2222 user@host
ssh -i ~/.ssh/key user@host

# 키 관리
ssh-keygen -t ed25519 -C "email"
ssh-copy-id user@host
cat ~/.ssh/id_ed25519.pub     # 공개키 확인

# 설정 (~/.ssh/config)
Host myserver
    HostName 192.168.1.100
    User ubuntu
    Port 22
    IdentityFile ~/.ssh/mykey

# 포트 포워딩
ssh -L 8080:localhost:80 user@host    # 로컬
ssh -R 9090:localhost:3000 user@host  # 원격
```

---

## F. Nginx 주요 설정

```nginx
# /etc/nginx/sites-available/mysite
server {
    listen 80;
    server_name example.com;
    root /var/www/mysite;
    index index.html;

    # 프록시
    location /api/ {
        proxy_pass http://localhost:3000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 정적 파일 캐시
    location ~* \.(jpg|css|js|png)$ {
        expires 30d;
    }

    # HTTPS 리디렉션
    return 301 https://$server_name$request_uri;
}
```

```bash
nginx -t            # 설정 검사
nginx -s reload     # 재로드
```

---

## G. MySQL

```bash
mysql -u root -p
mysql -u user -p dbname < dump.sql    # 복원

# MySQL 명령어
SHOW DATABASES;
USE dbname;
SHOW TABLES;
DESCRIBE tablename;

# 사용자 관리
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON dbname.* TO 'user'@'localhost';
FLUSH PRIVILEGES;

# 백업/복원
mysqldump -u root -p dbname > backup.sql
mysqldump -u root -p --all-databases > all.sql
```

---

## H. Docker

```bash
# 이미지
docker pull nginx
docker images
docker rmi nginx
docker build -t myapp:1.0 .

# 컨테이너
docker run -d -p 80:80 --name web nginx
docker ps
docker ps -a
docker stop|start|restart web
docker rm web
docker logs -f web
docker exec -it web bash

# Docker Compose
docker compose up -d
docker compose down
docker compose ps
docker compose logs -f
```

---

## I. 자주 쓰는 설정 파일

| 파일 | 용도 |
|------|------|
| `/etc/fstab` | 파일시스템 자동 마운트 |
| `/etc/hosts` | 로컬 DNS |
| `/etc/resolv.conf` | DNS 서버 |
| `/etc/network/interfaces` | 네트워크 설정 (구형) |
| `/etc/netplan/*.yaml` | 네트워크 설정 (신형) |
| `/etc/ssh/sshd_config` | SSH 서버 설정 |
| `/etc/sudoers` | sudo 권한 |
| `/etc/passwd` | 사용자 목록 |
| `/etc/group` | 그룹 목록 |
| `/etc/crontab` | 시스템 cron |
| `/var/log/syslog` | 시스템 로그 |
| `/var/log/auth.log` | 인증 로그 |

---

## J. 환경 변수와 .bashrc

```bash
# ~/.bashrc에 추가
export PATH="$HOME/bin:$PATH"
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export EDITOR=vim

# 유용한 alias
alias ll='ls -la'
alias ..='cd ..'
alias grep='grep --color=auto'
alias gs='git status'
alias gl='git log --oneline --graph'

# 함수
mkcd() { mkdir -p "$1" && cd "$1"; }

# 적용
source ~/.bashrc
```

---

## K. 트러블슈팅 빠른 참조

```bash
# 서비스 안 뜰 때
systemctl status SERVICE
journalctl -u SERVICE -n 50
SERVICE -t                    # 설정 검사 (nginx, apache2 등)

# 디스크 꽉 찼을 때
df -h                         # 파티션 확인
du -sh /* 2>/dev/null | sort -rh | head -10
journalctl --vacuum-size=200M
apt clean

# 포트 충돌
ss -tlnp | grep :80
fuser 80/tcp

# 네트워크 안 될 때
ip link show
ip addr show
ping -c 3 8.8.8.8
dig google.com @8.8.8.8

# 메모리 부족
free -h
ps aux --sort=-%mem | head -10
```

---

## L. 유용한 단축키

| 단축키 | 기능 |
|--------|------|
| `Ctrl+C` | 실행 중인 명령 취소 |
| `Ctrl+D` | 입력 종료 / 로그아웃 |
| `Ctrl+Z` | 프로세스 일시 정지 |
| `Ctrl+L` | 화면 지우기 |
| `Ctrl+A` | 줄 처음으로 |
| `Ctrl+E` | 줄 끝으로 |
| `Ctrl+R` | 명령어 이력 검색 |
| `Ctrl+W` | 앞 단어 삭제 |
| `!!` | 이전 명령 재실행 |
| `!$` | 이전 명령의 마지막 인자 |
| `Tab` | 자동완성 |
| `Tab Tab` | 자동완성 목록 |
