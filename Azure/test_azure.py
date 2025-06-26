# -*- coding: utf-8 -*-
# /home/pi/www/python/test_hione.py

import time
from azure.iot.device import IoTHubDeviceClient
from hione import Hione
import lib

# config.json에서 포트 정보 불러오기
global_config = lib.getConfigByJsonFile("/home/pi/www/python/config.json")
PORT = global_config["doorlock"]

# 도어락 클래스 초기화
hione = Hione(port=PORT)

# Azure IoT Hub 연결 문자열
CONNECTION_STRING = "HostName=smartdoor.azure-devices.net;DeviceId=smartdoor1;SharedAccessKey=L6nXuaejjwCA51bdBLIoCgPOE2RNxtz7PlzeXII6xdg="

def message_handler(message):
    try:
        msg = message.data.decode('utf-8').strip()
    except Exception as e:
        print("메시지 디코딩 오류:", e)
        msg = ""

    print("📩 Received message:", msg)
    print("Properties:", message.custom_properties)

    if msg.lower() == "open":
        try:
            result = hione.doorOpenProcess()
            print("✅ 문 열림 성공:", result)
        except Exception as e:
            print("🚨 doorOpenProcess() 실행 중 오류 발생:", e)

def main():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    try:
        client.connect()
        client.on_message_received = message_handler
        print("🔌 Azure IoT 메시지 대기 중...")

        # 무한 대기
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("🛑 종료됨")

    except Exception as e:
        print("💥 전체 예외 발생:", e)

    finally:
        client.shutdown()


if __name__ == "__main__":
    main()
