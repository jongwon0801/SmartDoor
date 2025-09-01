import RPi.GPIO as GPIO
import time
import datetime

# GPIO 설정
PIR_PIN = 22  # BCM 모드의 GPIO 22번 핀
GPIO.setmode(GPIO.BCM)  # BCM 모드 설정
GPIO.setup(PIR_PIN, GPIO.IN)  # PIR 센서 입력으로 설정

def test_pir_sensor():
    try:
        print("PIR 센서 모니터링 시작... (종료하려면 Ctrl+C를 누르세요)")
        print("시간\t\t\t상태\t\t데이터값")
        print("-" * 50)
        
        while True:
            # 현재 시간 가져오기
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 현재 센서 상태 읽기
            sensor_value = GPIO.input(PIR_PIN)
            
            # 상태 메시지 결정
            status = "움직임 감지됨!" if sensor_value else "움직임 없음"
            
            # 출력
            print(f"{current_time}\t{status}\t\t{sensor_value}")
            
            time.sleep(0.5)  # 딜레이 약간 늘림 (출력 빈도 조절)
            
    except KeyboardInterrupt:
        print("\n프로그램 종료")
    finally:
        GPIO.cleanup()  # GPIO 설정 초기화
        print("GPIO 정리 완료")

if __name__ == "__main__":
    print("PIR 센서 테스트 (GPIO 22번 핀)")
    test_pir_sensor()
