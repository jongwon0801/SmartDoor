#### AWS IoT Core에 MQTT로 연결

```less
# AWSIoTPythonSDK 설치

pip install AWSIoTPythonSDK


# AWS IoT 연결 위한 사용자 지정 엔드포인트 도메인
a3w0bwid9rv2t1-ats.iot.ap-northeast-2.amazonaws.com
```

#### 기본 Python 예제 코드
```less
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time

# 기본 설정
client_id = "wikibox_pi_01"  # Thing 이름
endpoint = "a3w0bwid9rv2t1-ats.iot.ap-northeast-2.amazonaws.com"  # 실제 엔드포인트로 변경
root_ca_path = "/home/pi/www/aws/AmazonRootCA1.pem"
certificate_path = "/home/pi/www/aws/7876a33691b43bf8d75bb97523c5880b1eca939fff26badf2ab1924069a3cbdb-certificate.pem.crt"
private_key_path = "/home/pi/www/aws/7876a33691b43bf8d75bb97523c5880b1eca939fff26badf2ab1924069a3cbdb-private.pem.key"

# MQTT 클라이언트 초기화
mqtt_client = AWSIoTMQTTClient(client_id)
mqtt_client.configureEndpoint(endpoint, 8883)
mqtt_client.configureCredentials(root_ca_path, private_key_path, certificate_path)

# 연결 시도
print("Connecting to AWS IoT Core...")
mqtt_client.connect()
print("Connected!")

# 테스트 메시지 전송
topic = "wikibox/door/control"
message = '{"status": "open"}'
mqtt_client.publish(topic, message, 1)
print(f"Message '{message}' published to topic '{topic}'")

# 계속 유지 (필요에 따라)
time.sleep(2)
mqtt_client.disconnect()

```












































