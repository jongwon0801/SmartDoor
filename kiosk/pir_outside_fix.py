# rm pir_outside.py 삭제
# nano ~/www/python/pir_outside.py 관련 로직삭제 후 아래 로직으로 변경
# pir 관련 로직 무시하고 진행하기 위해서

# -*- coding: utf-8 -*-
import lib
import serial
import threading


def pushed_callback() :
    print('pushed')

def moved_callback(self) :
    print('moved')

    if self.wikismartdoor is not None :
        self.wikismartdoor.sendKiosk('outCameraOn')

def finished_callback() :
    print('finished')

class PirOutside() :
    STX = b'\x02'  # message start byte
    ETX = b'\x03'  # message end byte
    timer = 0
    prev_time = None
    serial = None
    isBell = False
    process_task = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            lib.log("PIR Outside __new__ is called\n")
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        lib.log("PIR Outside __init__ is called\n")
        #serial 포트 연결 제거
        #self.serial = serial.Serial(kwargs['device'], 9600, timeout=0.5, writeTimeout=0.5)

    def run(self):
        while True:
            # 메시지 처리 로직을 주석 처리 또는 수정
            pass

    def receive_msg(self):
        return None  # 메시지 수신하지 않도록 수정

    def process(self, msg):
        pass  # 메시지 처리 코드 제거
