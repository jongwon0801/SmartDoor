# # pir 센서에 기기가 등록 안되어있어서 에러
# nano ~/www/python/pir_outside.py


# # 경로 검색
# find /home/pi/www/python -name "pir_outside.py"

# --> /home/pi/www/python/pir_outside.py

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
        #lib.log(kwargs)

        self.wikismartdoor = kwargs.get('wikismartdoor', None)
        self.times = kwargs.get('times', 30) * 2
        self.pushed_callback = kwargs.get('pushed_callback', pushed_callback)
        self.moved_callback = kwargs.get('moved_callback', moved_callback)
        self.finished_callback = kwargs.get('finished_callback', finished_callback)
        
        if self.serial is not None:
            lib.log("PIR Outside : Serial port is already connected.")
        elif self.serial == None and 'device' in kwargs and kwargs['device'] != '':
            lib.log("PIR Outside : %s is connected" % (kwargs['device']))
            self.serial = serial.Serial(kwargs['device'], 9600, timeout=0.5, writeTimeout=0.5)
        else:
            lib.log("PIR Outside : Serial port is not connected.")

    def run(self):
        while True :
            msg = self.receive_msg()

            if msg != None:
                self.nomsg = 0
                self.process(msg)

    def receive_msg(self) :
        char = self.serial.read(1)
        #lib.log("timer : %s" % self.timer)
        #lib.log("timer : %s recordStatus : %s isAction : %s" % (self.timer, self.recordStatus, self.isAction))
        #lib.log(char)
        if self.timer > 0 :
            self.timer = self.timer + 1

        if self.timer >= self.times :
            #threading.Thread(target=self.finished_callback, daemon=True).start()
            self.finished_callback()
            self.timer = 0

        if char and char == self.STX:
            msg = bytearray()
            msg.append(int.from_bytes(char, "big"))
            while True:
                char = self.serial.read(1)
                msg.append(int.from_bytes(char, "big"))
                if char == self.ETX:  # 메시지 종료 바이트 수신되면 루프 탈출
                    break

            # 실제 테스트를 하면서 올바른 메시지 검증 코드 추가
            #lib.log(f'외부카메라로부터 받은 메시지: {msg}')
            #lib.log('PIR Outside Receive Message : %s' % msg)
            return msg
        else:
            #lib.log('0.5초 기다린 후 다음으로 진행합니다.[%s]' % self.timer)
            pass
        return None

    def process(self, msg):
        #lib.log('%s msg[4],[6] : %s,%s [%s](%s)[%s]' % (msg, msg[4], msg[6], datetime.datetime.now(), self.timer, self.isAction))

        #도어벨을 누른경우
        if msg[6] == 49:
            lib.log("PIR OUT doorbell push...")

            if not self.isBell and hasattr(self, 'pushed_callback') and self.pushed_callback :
                self.isBell = True
                #lib.log("PIR OUT doorbell thread call...")
                #threading.Thread(target=self.pushed_callback, daemon=True).start()
                self.pushed_callback()
                #lib.log("PIR OUT doorbell thread end...")
                self.isBell = False

        # 모션이 감지되는 경우
        elif msg[4] == 48 :
            lib.log("PIR OUT camera on...%s " % self.timer)

            if self.timer > 0 :
                self.timer = 1
            
            if hasattr(self, 'moved_callback') and self.moved_callback :
                #threading.Thread(target=self.moved_callback, daemon=True).start()
                self.moved_callback()

        # 모션이 감지가 종료되는 경우
        elif msg[4] == 49 :
            self.timer = 1
            lib.log("PIR OUT 모션 감지 종료... %s " % self.timer)
