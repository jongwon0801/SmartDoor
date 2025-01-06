
### 1. include /etc/nginx/modules-enabled/*.conf;
이 설정은 Nginx가 활성화된 모듈 설정 파일을 포함하도록 지정합니다. 모듈은 Nginx의 기능을 확장하는 데 사용됩니다. 이 구문은 Nginx가 시작될 때 modules-enabled 디렉터리 내에 있는 모든 .conf 파일을 로드하여 활성화합니다.
위치: Nginx의 초기 설정 부분에서 로드되므로, 전체 Nginx 설정에 영향을 미칩니다.


### 2. user www-data;
이 설정은 Nginx가 실행될 때 사용하는 사용자와 그룹을 지정합니다. www-data는 Nginx 웹 서버 프로세스가 사용하는 기본 사용자입니다.
위치: 주로 Nginx 설정의 상단에 위치하여, 서버가 시작될 때 먼저 적용됩니다.


### 3. worker_processes auto;
이 설정은 Nginx가 사용할 워커 프로세스의 수를 지정합니다. auto로 설정하면, Nginx는 CPU 코어 수에 맞게 자동으로 워커 프로세스 수를 설정합니다.
위치: Nginx가 시작될 때 설정되며, 기본적인 서버 설정입니다.

### 4. pid /run/nginx.pid;
이 설정은 Nginx의 PID(프로세스 ID) 파일 위치를 지정합니다. 이 파일은 Nginx 프로세스가 실행 중일 때 해당 프로세스의 ID를 기록하는 데 사용됩니다.
위치: Nginx의 초기 설정에 포함되어 서버 시작 시에 설정됩니다.

### 5. include /etc/nginx/conf.d/*.conf;
이 구문은 Nginx가 conf.d/ 디렉터리 내에 있는 모든 .conf 파일을 포함하도록 설정합니다. 보통 이 디렉터리에는 서버 블록, 리버스 프록시 설정, 기타 다양한 서버 관련 설정 파일들이 포함됩니다.
위치: http 블록 안에 포함되며, 서버 동작에 필요한 다양한 설정들을 정의할 수 있습니다.

### 6. include /etc/nginx/sites-enabled/*;
이 구문은 sites-enabled 디렉터리 내의 모든 설정 파일을 포함하도록 지정합니다. 이 디렉터리에는 각 도메인에 대한 서버 블록 설정이 위치합니다.
위치: http 블록 안에 포함되어 도메인별 서버 설정을 로드합니다.

### 우선순위

nginx.conf 파일은 기본 설정 파일로 가장 먼저 로드됩니다. 이 파일 내에서 다른 파일을 include하여 로드하게 됩니다.
http 블록 안에 있는 include /etc/nginx/conf.d/*.conf;와 include /etc/nginx/sites-enabled/*;는 nginx.conf에서 http 블록이 로드된 후에 읽힙니다.
이들은 서버 동작과 관련된 세부적인 설정들을 다루기 위한 것입니다.
user와 worker_processes, pid 설정은 서버의 기본 실행 환경을 설정하는 데 사용되며, Nginx가 시작할 때 가장 먼저 적용됩니다.
이러한 설정들은 nginx.conf의 상단에 위치하며, 서버의 기본 환경을 정의합니다.

### 결론
모든 include 지시문은 Nginx의 설정을 분리하고 유연하게 관리하는 데 도움을 줍니다. 이렇게 하면 각 설정 파일을 독립적으로 관리하고, 여러 서버 블록 또는 모듈 설정을 쉽게 수정할 수 있습니다.
우선순위: 기본적인 서버 설정(user, worker_processes, pid)은 Nginx가 시작할 때 가장 먼저 읽고 적용되며, 그 후에 include 구문을 통해 다양한 추가 설정이 적용됩니다.
conf.d나 sites-enabled와 같은 설정 파일은 Nginx가 동작하는 데 필요한 세부적인 설정을 정의합니다.






### 1. 목적
Nginx는 다양한 모듈을 통해 기능을 확장할 수 있습니다.
이 include 구문은 /etc/nginx/modules-enabled/ 디렉터리에 있는 모든 .conf 파일을 로드하여, 해당 모듈들을 활성화하는 역할을 합니다.
이 방법을 사용하면 Nginx가 필요로 하는 특정 모듈들을 동적으로 관리할 수 있게 되며, 각 모듈은 .conf 파일을 통해 활성화됩니다.
예를 들어, 특정 인증 모듈이나 압축 모듈을 로드하고자 할 때 이 방식이 사용됩니다.

### 2. 모듈 활성화
modules-enabled 디렉터리는 보통 Nginx가 지원하는 모듈들이 링크나 파일 형태로 배치된 디렉터리입니다. 이 디렉터리에 있는 .conf 파일을 포함하여, Nginx가 시작될 때 이 모듈들이 자동으로 활성화됩니다.
/etc/nginx/modules-enabled/ 디렉터리에 있는 파일들은 modules-available 디렉터리에 있는 모듈들을 활성화할 수 있도록 심볼릭 링크로 연결된 경우가 많습니다.

### 3. 동적 모듈
Nginx에서는 모듈을 정적으로 컴파일하거나, 동적으로 로드할 수 있습니다.
include /etc/nginx/modules-enabled/*.conf;는 동적 모듈을 로드하는 방식입니다.
이 구문을 사용하면 Nginx를 재컴파일하지 않고도 필요한 모듈을 추가하거나 제거할 수 있습니다.
필요한 모듈의 설정 파일을 modules-enabled 디렉터리에 추가하거나 제거함으로써, Nginx 설정을 유연하게 관리할 수 있습니다.

### 4. 실제 사용 예
예를 들어, ngx_http_rewrite_module, ngx_http_ssl_module 등의 모듈이 필요하다면, 이들 모듈을 modules-enabled 디렉터리 내의 .conf 파일로 활성화하고, 해당 모듈의 설정을 포함할 수 있습니다.
설정 파일에 예를 들면, /etc/nginx/modules-enabled/에 mod_rewrite.conf 파일이 있을 경우, Nginx는 이 파일을 읽고 관련된 모듈을 로드하여 사용합니다.

### 요약

include /etc/nginx/modules-enabled/*.conf;는 Nginx가 시작될 때 modules-enabled 디렉터리 내의 .conf 파일을 읽어, 해당 모듈들을 활성화하는 역할을 합니다.
이 구문은 Nginx에서 동적 모듈을 사용하고 있으며, 필요한 모듈을 손쉽게 관리하고 추가하거나 제거할 수 있는 유연성을 제공합니다.
모듈을 동적으로 로드함으로써, Nginx의 기능을 쉽게 확장할 수 있습니다.
