import Adafruit_DHT
import time

# 센서 종류 설정 (DHT11 또는 DHT22)
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 2  # GPIO 번호

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            print(f"온도: {temperature:.1f}°C, 습도: {humidity:.1f}%")
        else:
            print("센서 읽기 실패")
        time.sleep(2)  # 2초 간격으로 읽기

except KeyboardInterrupt:
    print("종료")
