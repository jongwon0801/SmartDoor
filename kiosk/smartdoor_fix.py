# nano /home/pi/www/python/elcsoft/controller/smartdoor.py 수정

# 기기 관련 코드 제거
# setBle() 함수, joinProcess(), syncProcess() 등의 기기와 연동되는 부분을 제거 또는 주석 처리

# BLE 설정 (기기 없이 주석 처리)
# def setBle(device_id):
#     pass

# 기기 등록 (기기 없이 주석 처리)
# def joinProcess(serial_number):
#     print(f"Joining device with serial number {serial_number}")

# 서버 동기화 (기기 없이 주석 처리)
# def syncProcess():
#     print("Syncing data with server")

# Motion 감지 (기기 없이 주석 처리)
# def motionDetectProcess():
#     print("Motion detected, sending notification")

# 서버만 돌리기 위한 기능 (필요한 코드만 남기기)

def getSmartdoorObj():
    # 스마트도어 객체 가져오기
    print("Getting smart door object")

def getSmartdoorInfo():
    # 스마트도어 정보 가져오기
    print("Getting smart door info")

def getToken():
    # 토큰 관리
    print("Fetching token")

def doorbellPushProcess():
    # 도어벨 푸시 알림
    print("Sending doorbell push notification")

def sendFcm(message):
    # FCM 푸시 알림 전송
    print(f"Sending FCM push notification: {message}")

# 기타 서버에서 필요한 함수들만 남기고 기기 관련 부분 삭제

if __name__ == "__main__":
    # 서버 실행
    print("Server is running without physical devices")
    getSmartdoorObj()  # 스마트도어 객체 가져오기
    getSmartdoorInfo()  # 스마트도어 정보 가져오기
    getToken()  # 토큰 처리
    doorbellPushProcess()  # 도어벨 푸시 알림
