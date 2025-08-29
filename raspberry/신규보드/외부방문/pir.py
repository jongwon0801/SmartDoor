import serial
import time

# USB 시리얼 포트 설정 (포트 이름은 시스템에 따라 다를 수 있습니다)
# Linux에서는 일반적으로 /dev/ttyUSB0 또는 /dev/ttyACM0 형태입니다
PORT = "/dev/ttyUSB0"  # 실제 포트 이름으로 변경하세요
BAUD_RATE = 9600       # 센서의 통신 속도에 맞게 설정하세요

def test_pir_sensor():
    try:
        # 시리얼 포트 열기
        ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
        print(f"연결 성공: {PORT}")
        
        print("PIR 센서 모니터링 시작... (종료하려면 Ctrl+C를 누르세요)")
        while True:
            # 데이터 읽기
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
                print(f"수신 데이터: {data}")
                
                # 움직임 감지 여부 확인 (센서 출력 형식에 따라 조정 필요)
                if "1" in data or "HIGH" in data or "MOTION" in data:
                    print("움직임 감지됨!")
                elif "0" in data or "LOW" in data or "NO_MOTION" in data:
                    print("움직임 없음")
            
            time.sleep(0.1)  # 약간의 딜레이
            
    except serial.SerialException as e:
        print(f"시리얼 포트 오류: {e}")
    except KeyboardInterrupt:
        print("\n프로그램 종료")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("시리얼 포트 닫힘")

if __name__ == "__main__":
    # 사용 가능한 시리얼 포트 확인 (선택 사항)
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
    print("사용 가능한 포트:")
    for port in ports:
        print(f" - {port.device}: {port.description}")
    
    # PIR 센서 테스트 시작
    test_pir_sensor()
