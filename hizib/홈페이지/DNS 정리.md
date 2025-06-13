#### 호스팅kr 보유 도메인
1. wikismartdoor.com
```less
# 기간
2023/12/04 ~ 2025/12/04

# 네임서버
ns1.cafe24.com
ns1.cafe24.co.kr
```

2. hizib.com
```less
# 기간
2022/12/12 ~ 2025/12/12

# 네임서버
ns1.hosting.co.kr
ns2.hosting.co.kr
ns3.hosting.co.kr
ns4.hosting.co.kr

# 포워딩 : 고정 포워딩 (주소창에 입력한 도메인으로 표기)
wisemonster.kr
```

3. wisemonster.kr
```less
# 기간
2020/09/25 ~ 2025/09/25

# 네임서버
ns1.cafe24.com
ns1.cafe24.co.kr
```

4. apple-box.kr
```less
# 기간
2016/07/04 ~ 2026/07/04

# 네임서버
ns1.hosting.co.kr
ns2.hosting.co.kr
ns3.hosting.co.kr
ns4.hosting.co.kr

# DNS 레코드
유형     호스트이름             값          TTL
A /       @        / 125.209.198.152 / 180
A / applebox-10000 / 125.209.200.159 / 180
A / applebox-10001 / 125.209.200.159 / 180
A / applebox-10002 / 125.209.200.159 / 180
A / applebox-11097 / 125.209.200.159 / 180
A / smart / 125.209.200.159 / 180
A / test / 125.209.200.159 / 180

# 호스트
호스트 이름  	        IP 주소
smart.apple-box.kr  125.209.200.159

www.apple-box.kr    125.209.198.152
```

5. wikibox.kr
```less
# 기간
2015/01/23 ~ 2026/01/23

# 네임서버
ns1.hosting.co.kr
ns2.hosting.co.kr
ns3.hosting.co.kr
ns4.hosting.co.kr

# DNS 레코드
유형     호스트이름             값          TTL

# 인증서 https 때문에 네이버 클라우드 nginx 경유함
# 125.209.200.159 (smart.apple-box.kr)
A /         @      /    125.209.200.159 / 180     

A / api.hizib     /     13.124.155.19 / 180
A / api1.hizib   /      175.211.153.28 / 300
A / api2.hizib   /      175.211.153.28 / 180
A / dev         /       1.255.56.176 / 180
A / hizib       /       13.124.155.19 / 180
A / www         /       125.209.200.159 / 180
TXT / _acme-challenge.hizib / 0GAXIkNMvYLa-HbSGR8QnVKw_F7tQuQuZJ5yw9_Hwe8 / 180
TXT / _acme-challenge.hizib / rsxzT-84HmFolHjHpFFP4JpS9dMSKs4-oKwonEaDzMk / 180
MX /       @     / 10 aspmx.daum.net / 3600
MX /       @     / 20 alt.aspmx.daum.net / 3600
TXT /      @     / v=spf1 include:_spf.daum.net ~all / 3600
```

#### 카페24 호스팅 도메인
1. wisemonster.kr
```less
# 호스트IP(A 레코드) 관리
210.114.6.139

nslookup wisemonster.kr
Name:	wisemonster.kr
Address: 210.114.6.139

# 메일서버(MX) 관리
wisemonster.kr	mw-002.cafe24.com	10

# 별칭(CNAME) 관리
*.wisemonster.kr		wisemonster.kr

# SPF 관리
wisemonster.kr	"v=spf1 ip4:210.114.6.139 ~all"
```

2. wikismartdoor.com
```less
# 호스트IP(A 레코드) 관리
210.114.6.139

nslookup wikismartdoor.com
Name:	wikismartdoor.com
Address: 210.114.6.139

# 메일서버(MX) 관리
wisemonster.kr	mw-002.cafe24.com	10

# 별칭(CNAME) 관리
*.wisemonster.kr		wisemonster.kr

# SPF 관리
wisemonster.kr	"v=spf1 ip4:210.114.6.139 ~all"
```








