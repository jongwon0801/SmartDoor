import RPi.GPIO as GPIO
import time
import datetime
import serial
import Adafruit_DHT
import threading

# GPIO 설정
PIR_PIN = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

# DHT 센서 설정
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 2

# 시리얼 포트 설정
PORT = "/dev/ttyACM0"
BAUD_RATE = 9600
TIMEOUT = 5

# 임계값 설정
GAS_THRESHOLD = 400
FLAME_THRESHOLD = 300

# 결과 저장용 전역 변수
pir_status = "초기화 중..."
pir_raw_value = "N/A"
temp_humidity = "초기화 중..."
temp_raw = "N/A"
humidity_raw = "N/A"
sensor_status = "초기화 중..."
gas_raw = "N/A"
flame_raw = "N/A"
vibration_raw = "N/A"


# PIR 센서 모니터링 함수
def monitor_pir():
    global pir_status, pir_raw_value
    print("PIR 센서 모니터링 시작...")

    while True:
        try:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sensor_value = GPIO.input(PIR_PIN)
            status = "움직임 감지됨!" if sensor_value else "움직임 없음"
            pir_status = f"PIR 센서: {status}"
            pir_raw_value = str(sensor_value)
            time.sleep(0.5)  # 0.5초 간격으로 확인
        except Exception as e:
            pir_status = f"PIR 오류: {str(e)}"
            pir_raw_value = "오류"
            time.sleep(1)


# 온습도 센서 모니터링 함수
def monitor_temp():
    global temp_humidity, temp_raw, humidity_raw
    print("온습도 센서 모니터링 시작...")

    while True:
        try:
            humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
            if humidity is not None and temperature is not None:
                temp_humidity = f"온도: {temperature:.1f}°C, 습도: {humidity:.1f}%"
                temp_raw = f"{temperature:.1f}"
                humidity_raw = f"{humidity:.1f}"
            else:
                temp_humidity = "온습도 센서 읽기 실패"
                temp_raw = "N/A"
                humidity_raw = "N/A"
            time.sleep(1)  # 1초 간격으로 확인
        except Exception as e:
            temp_humidity = f"온습도 오류: {str(e)}"
            temp_raw = "오류"
            humidity_raw = "오류"
            time.sleep(1)


# USB 센서 모니터링 함수
def monitor_sensors():
    global sensor_status, gas_raw, flame_raw, vibration_raw
    print("USB 센서 모니터링 시작...")

    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout=TIMEOUT)
        print(f"포트 {PORT} 열림")

        while True:
            try:
                line = ser.readline().decode("utf-8").strip()

                if line:
                    values = line.split(",")
                    if len(values) == 3:
                        gas_status_code = values[0]
                        flame_value = int(values[1])
                        vibration_value = values[2]

                        gas_status = (
                            "가스 위험"
                            if int(gas_status_code) > GAS_THRESHOLD
                            else "정상"
                        )
                        flame_detected = (
                            "불꽃 감지" if flame_value < FLAME_THRESHOLD else "정상"
                        )
                        vibration_detected = (
                            "진동 감지" if vibration_value != "0000" else "정상"
                        )

                        sensor_status = f"가스: {gas_status} | 불꽃: {flame_detected} | 진동: {vibration_detected}"

                        # 원시 데이터 저장
                        gas_raw = gas_status_code
                        flame_raw = str(flame_value)
                        vibration_raw = vibration_value
                time.sleep(0.1)  # 빠른 시리얼 데이터 확인
            except Exception as e:
                sensor_status = f"센서 데이터 처리 오류: {str(e)}"
                gas_raw = "오류"
                flame_raw = "오류"
                vibration_raw = "오류"
                time.sleep(1)
    except Exception as e:
        sensor_status = f"시리얼 포트 오류: {str(e)}"
        gas_raw = "오류"
        flame_raw = "오류"
        vibration_raw = "오류"
    finally:
        if "ser" in locals() and ser.is_open:
            ser.close()


# 메인 모니터링 함수
def main_monitor():
    print("통합 모니터링 시스템 시작...")
    print("-" * 80)

    try:
        while True:
            # 화면 지우기 (리눅스/맥)
            print("\033c", end="")
            # 윈도우의 경우 아래 주석 해제
            # import os
            # os.system('cls')

            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 화면 너비 계산
            width = 80
            half_width = width // 2 - 5  # 중앙 구분선 공간 확보

            print("=" * width)
            title = f"[{current_time}] 스마트 도어 통합 센서 모니터링"
            print(f"{title:^{width}}")
            print("=" * width)

            # 헤더 출력
            print(f"{'상태 정보':<{half_width}} | {'원시 데이터':^{half_width}}")
            print("-" * width)

            # PIR 센서 정보
            print(f"\n{'[PIR 모션 센서]':<{half_width}} | {'[데이터값]':^{half_width}}")
            print(
                f"{'-' * (half_width - 2):<{half_width}} | {'-' * (half_width - 2):^{half_width}}"
            )
            print(f"{pir_status:<{half_width}} | {pir_raw_value:^{half_width}}")

            # 온습도 센서 정보
            print(f"\n{'[온습도 센서]':<{half_width}} | {'[데이터값]':^{half_width}}")
            print(
                f"{'-' * (half_width - 2):<{half_width}} | {'-' * (half_width - 2):^{half_width}}"
            )
            print(
                f"{temp_humidity:<{half_width}} | {'온도: ' + temp_raw + '°C, 습도: ' + humidity_raw + '%':^{half_width}}"
            )

            # 가스/불꽃/진동 센서 정보
            print(
                f"\n{'[가스/불꽃/진동 센서]':<{half_width}} | {'[데이터값]':^{half_width}}"
            )
            print(
                f"{'-' * (half_width - 2):<{half_width}} | {'-' * (half_width - 2):^{half_width}}"
            )
            print(
                f"{sensor_status:<{half_width}} | {'가스: ' + gas_raw + ', 불꽃: ' + flame_raw + ', 진동: ' + vibration_raw:^{half_width}}"
            )

            print("\n" + "=" * width)
            print("종료하려면 Ctrl+C를 누르세요")

            time.sleep(0.5)  # 1초 간격으로 화면 갱신
    except KeyboardInterrupt:
        print("\n프로그램이 사용자에 의해 종료되었습니다.")
    except Exception as e:
        print(f"\n오류 발생: {e}")
    finally:
        GPIO.cleanup()
        print("GPIO 정리 완료")
        if "ser" in locals() and ser.is_open:
            ser.close()
            print("시리얼 포트 닫힘")


if __name__ == "__main__":
    # 각 센서 모니터링을 위한 스레드 생성
    pir_thread = threading.Thread(target=monitor_pir, daemon=True)
    temp_thread = threading.Thread(target=monitor_temp, daemon=True)
    sensor_thread = threading.Thread(target=monitor_sensors, daemon=True)

    # 스레드 시작
    pir_thread.start()
    temp_thread.start()
    sensor_thread.start()

    # 메인 모니터링 시작
    main_monitor()
