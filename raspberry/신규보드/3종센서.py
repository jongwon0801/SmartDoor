import serial
import time

# 시리얼 포트 설정
PORT = '/dev/ttyACM0'
BAUD_RATE = 9600
TIMEOUT = 5

# 가스 센서 임계값 설정
GAS_THRESHOLD = 400  # 이 값 이상이면 위험 상태로 간주
# 불꽃 센서 임계값 - 값이 이것보다 낮으면 불꽃 감지로 판단
FLAME_THRESHOLD = 300

try:
    # 시리얼 포트 연결
    ser = serial.Serial(PORT, BAUD_RATE, timeout=TIMEOUT)
    print(f'포트 {PORT} 열림 - {time.strftime("%H:%M:%S")}')
    print("Press CTRL+C to exit")
    
    last_print_time = time.time()
    
    while True:
        # 데이터 읽기
        line = ser.readline().decode('utf-8').strip()
        
        current_time = time.time()
        
        # 2초마다 출력
        if current_time - last_print_time >= 2.0 and line:
            try:
                # 데이터 형식: "0101,1023,0000"
                values = line.split(',')
                if len(values) == 3:
                    gas_status_code = values[0]
                    flame_value = int(values[1])
                    vibration_value = values[2]
                    
                    # 가스 센서 상태 해석
                    gas_status = "가스 위험" if int(gas_status_code) > GAS_THRESHOLD else "정상"
                    
                    # 불꽃 센서 값 해석 - 값이 낮을 때 불꽃 감지로 변경
                    flame_detected = "불꽃 감지" if flame_value < FLAME_THRESHOLD else "정상"
                    
                    # 진동 센서 값 해석
                    vibration_detected = "진동 감지" if vibration_value != "0000" else "정상"
                    
                    # 결과 출력 (원시 데이터 포함)
                    status_msg = f"가스: {gas_status} | 불꽃: {flame_detected} | 진동: {vibration_detected} | 원시값: {line}"
                    print(status_msg)
                    
                    last_print_time = current_time
                else:
                    print(f"알 수 없는 데이터 형식: {line}")
            except Exception as e:
                print(f"데이터 처리 오류: {e} - 원시 데이터: {line}")
        
        # 짧은 대기 시간
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print("\n사용자에 의해 종료됨")
    
except Exception as e:
    print(f"오류 발생: {e}")
    
finally:
    # 프로그램 종료 시 포트 닫기
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("포트 닫힘")
