#### 모드버스 스크립트
```less
import logging
import time
import threading
from pymodbus.client.sync import ModbusSerialClient

_log = logging.getLogger("ModbusControl")

# -------------------
# Modbus 시리얼 설정
# -------------------
MODBUS_CONFIG = {
    "method": "rtu",
    "port": "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AK3XEFC4-if00-port0",
    "baudrate": 9600,
    "bytesize": 8,
    "parity": "N",
    "stopbits": 1,
    "timeout": 1,
}

# -------------------
# 스위치 & 센서 정의
# -------------------
MODBUS_SWITCHES = {
    "OUT 1": {"slave": 1, "address": 0, "command_on": 0x0100, "command_off": 0x0200},
    "OUT 2": {"slave": 1, "address": 1, "command_on": 0x0100, "command_off": 0x0200},
    "OUT 8": {"slave": 1, "address": 7, "command_on": 0x0100, "command_off": 0x0200},
}

MODBUS_SENSORS = {
    "IN 1": {"slave": 1, "address": 192, "scan_interval": 1},
}

# -------------------
# 상태 저장
# -------------------
switch_states = {sw: False for sw in MODBUS_SWITCHES}
sensor_states = {sn: None for sn in MODBUS_SENSORS}
manual_override = {sw: False for sw in MODBUS_SWITCHES}

# -------------------
# 클라이언트
# -------------------
client = ModbusSerialClient(**MODBUS_CONFIG)


def setup():
    """모드버스 연결 초기화"""
    if not client.connect():
        _log.error("❌ Modbus 연결 실패")
        return False
    _log.info("✅ Modbus 연결 성공")
    return True


def cleanup():
    """모드버스 종료"""
    client.close()
    _log.info("🧹 Modbus 연결 종료")


def read_sensors():
    for name, cfg in MODBUS_SENSORS.items():
        try:
            response = client.read_holding_registers(cfg["address"], 1, unit=cfg["slave"])
            if not response.isError():
                value = response.registers[0]
                if value != sensor_states[name]:
                    _log.info(f"📖 센서 {name} 값: {value}")
                sensor_states[name] = value
            else:
                _log.error(f"{name} 읽기 오류: {response}")
        except Exception as e:
            _log.error(f"{name} 읽기 예외: {e}")


def write_switch(name, on: bool):
    cfg = MODBUS_SWITCHES[name]
    try:
        value = cfg["command_on"] if on else cfg["command_off"]
        response = client.write_register(cfg["address"], value, unit=cfg["slave"])
        if response.isError():
            _log.error(f"{name} 쓰기 오류: {response}")
            return False
        else:
            switch_states[name] = on
            manual_override[name] = True
            _log.info(f"✍️ {name} {'ON' if on else 'OFF'} 완료 (수동)")
            return True
    except Exception as e:
        _log.error(f"{name} 쓰기 예외: {e}")
        return False


def set_auto(name):
    if name in manual_override:
        manual_override[name] = False
        _log.info(f"🔄 {name} 자동 제어 모드 전환")


def automation_logic():
    in1 = sensor_states.get("IN 1")
    if in1 is None:
        return

    if manual_override["OUT 8"]:
        return  # 수동 모드면 자동 제어 안 함

    if in1 > 0 and not switch_states["OUT 8"]:
        _log.info("IN 1 > 0 → OUT 8 ON (자동)")
        write_switch("OUT 8", True)
        manual_override["OUT 8"] = False
    elif in1 <= 0 and switch_states["OUT 8"]:
        _log.info("IN 1 < 1 → OUT 8 OFF (자동)")
        write_switch("OUT 8", False)
        manual_override["OUT 8"] = False


def start_background_loop():
    """센서 읽기 + 자동화를 백그라운드에서 실행"""
    def loop():
        while True:
            read_sensors()
            automation_logic()
            time.sleep(0.5)

    t = threading.Thread(target=loop, daemon=True)
    t.start()
    _log.info("▶️ 모드버스 백그라운드 루프 시작됨")

```
