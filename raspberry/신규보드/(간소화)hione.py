#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import datetime
import argparse
import threading
import serial


class Hione:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            print("Hione __new__ is called\n")
            cls._instance = super().__new__(cls)
            cls.port = kwargs["port"]
            cls.IS_DOOR_OPEN = 0
            cls.client = None
            cls.exitThread = False
            cls.DOORCLOSER_OPEN_TIME = 10
            cls.lock = threading.Lock()
            cls.doorStatus = 0  # 0:닫힘 1:닫는중 2:여는중 3:열림
            cls.openTimes = 20
            cls.closeTimes = 30
        return cls._instance

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "_initialized"):
            print("Hione __init__ is called\n")
            self.port = kwargs.get("port")
            self._initialized = True

    def connect(self, timeout=5):
        self.client = serial.Serial()  # open serial port
        self.client.port = self.port
        self.client.baudrate = 19200
        self.client.stopbits = serial.STOPBITS_ONE
        self.client.bytesize = 8
        self.client.parity = serial.PARITY_NONE
        self.client.timeout = timeout
        self.client.open()
        # print(ser.name)         # check which port was really used
        # ser.write(b'hello')     # write a string
        # ser.close()             # close port

    def send(self, sdata):
        try:
            if self.client == None:
                self.connect()

            # print("Hione Send : %s [%s]" % (sdata.hex(), datetime.datetime.now()))
            # print('송신', sdata.hex())
            self.client.write(sdata)

            dummy = self.client.read(1)
            # print("Hione Recevied : %s [%s]" % (dummy, datetime.datetime.now()))

            if len(dummy) == 0:
                # print("Hione Recevied : no data")
                return None
            if dummy[0] != 0xFF:
                # print("Hione Recevied : dummy packet error %s" % dummy)
                return None

            # print(dummy)
            stx = self.client.read(1)
            # print(stx)
            length = self.client.read(1)  # command code +data
            # print(length)
            commdata = self.client.read(length[0])
            checksum = self.client.read(1)
            etx = self.client.read(1)

            # print("Hione Recevied : %s" % (dummy + stx + length + commdata + checksum + etx).hex())

            return dummy + stx + length + commdata + checksum + etx
        except Exception as e:
            # self.client = None
            print("Hione Recevied Fail : %s" % e)

    def ppacket(self, some_string):
        ret = [255, 255, 255, 255, 255, 255]
        x = 2
        res = [some_string[y - x : y] for y in range(x, len(some_string) + x, x)]

        for i in range(len(res)):
            istr = res[i]
            if len(istr) != 2:
                istr = istr + "F"
            ret[i] = int(istr, 16)

        return ret

    def close(self):
        if self.client:
            self.client.close()
            # print("serial close")
        self.client = None

    def showStatus(self, recv):
        # 00:잠금,01:해제
        if recv == None:
            raise NoDataException("시간이 초과되어 처리결과 메세지가 없습니다.")

        data = dict()

        # print('길이', len(recv))
        if recv and len(recv) == 14:
            # for i in range(len(recv)):
            #    print(i, recv[i])
            if recv[4] == 0x00:
                data["isDoorlock"] = False
                print("잠김상태:잠금상태")
            if recv[4] == 0x01:
                data["isDoorlock"] = True
                print("잠김상태:해제상태")
            if recv[5] == 0x00:
                data["isDooropen"] = False
                print("센서상태:닫힘상태")
            if recv[5] == 0x01:
                data["isDooropen"] = True
                print("센서상태:열림상태")
            if recv[6] == 0x00:
                data["battery"] = True
                print("베터리상태:정상")
            if recv[6] == 0x01:
                data["battery"] = False
                print("베터리상태:교환")

            if recv[3] == 0x03:  # 열기
                print("open time", recv[8])
                if recv[9] == 0x00:
                    print("오픈 실패")
                if recv[9] == 0x01:
                    print("오픈 성공")
            if recv[3] == 0x04:  # 닫기

                if recv[8] == 0x00:
                    print("닫기 실패")
                if recv[8] == 0x01:
                    print("닫기 성공")

            if recv[3] == 0x09:  # chage password
                if recv[8] == 0x00:
                    print("변경 실패")
                if recv[8] == 0x01:
                    print("변경 성공")
            return data

    def responseStatus(self, recv):
        # 00:잠금,01:해제
        if recv == None:
            raise NoDataException("시간이 초과되어 처리결과 메세지가 없습니다.")

        # print(recv)
        # print('길이', len(recv))
        if recv and len(recv) == 14:

            # for i in range(len(recv)):
            #    print(i, recv[i])
            """
            if recv[4] == 0x00:
                print('잠김상태:잠금상태')
            if recv[4] == 0x01:
                print('잠김상태:해제상태')
            if recv[5] == 0x00:
                print('센서상태:닫힘상태')
            if recv[5] == 0x01:
                print('센서상태:열림상태')
            if recv[6] == 0x00:
                print('베터리상태:정상')
            if recv[6] == 0x01:
                print('베터리상태:교환')
            """

            if recv[3] == 0x02:  # 상태
                if recv[4] == 0x00:
                    print("닫힘")
                    return False
                if recv[4] == 0x01:
                    print("열림")
                    return True

            if recv[3] == 0x03:  # 열기
                print("open door : %s" % recv[8])
                if recv[8] == 0x01:
                    print("오픈 성공")
                    return True
                elif recv[4] == 0x01:
                    print("오픈 성공")
                    return True
                elif recv[5] == 0x01:
                    print("오픈 성공")
                    return True
                elif recv[8] == 0x00:
                    print("오픈 실패")
                    raise Exception("문열기 명령에 실패하였습니다.")

            if recv[3] == 0x04:  # 닫기
                print("close door : %s" % recv[8])
                if recv[8] == 0x00:
                    print("닫기 실패")
                    raise Exception("문닫기 명령에 실패하였습니다.")
                if recv[8] == 0x01:
                    print("닫기 성공")
                    return True

            if recv[3] == 0x05:  # 일회용비밀번호 설정
                print("set one time passwd : %s" % recv[8:9])
                if recv[10] == 0x00:
                    print("일회용 비밀번호 설정 실패")
                    raise Exception("일회용 비밀번호 설정에 실패하였습니다.")
                if recv[10] == 0x01:
                    print("일회용 비밀번호 설정 성공")
                    return True

            if recv[3] == 0x06:  # 일회용비밀번호 초기화
                print("clear one time passwd : %s" % recv[8])
                if recv[8] == 0x00:
                    print("일회용 비밀번호 삭제 실패")
                    raise Exception("일회용 비밀번호 삭제에 실패하였습니다.")
                if recv[8] == 0x01:
                    print("일회용 비밀번호 삭제 성공")
                    return True

            if recv[3] == 0x07:  # 일회용비밀번호 조회
                print("get one time passwd : %s" % recv[11])

                if recv[8] == 0x00:
                    print("현재 저장된 일회용 비밀번호 없음")
                    raise False
                if recv[8] == 0x01:
                    print("사용하지 않은 일회용 비밀번호 존재")
                    return True

            if recv[3] == 0x09:  # chage password
                if recv[11] == 0x00:
                    print("변경 실패")
                    raise Exception("비밀번호 설정에 실패하였습니다.")
                if recv[11] == 0x01:
                    print("변경 성공")
                    return True
        else:
            raise NoDataException("도어락으로 부터 잘못된 응답이 왔습니다.")

    def setPassword(self, pwd):
        dummy = [0xFF]
        stx = [0x09]
        length = 0x00  # command + data length
        command = [0x04]  # 패스워드 변경
        data = self.ppacket(pwd) + [0, 0]  # password(6)+rfu(2)

        length = [0xFF & (len(data) + 1)]

        cs = length[0] + command[0]
        for d in data:
            cs = cs + d
        checksum = [0xFF & cs]

        # checksum=0x00 #length + command + data 16 digit +
        etx = [0x03]
        # print(dummy,stx,length,command ,data ,checksum ,etx)
        senddata = bytearray(dummy + stx + length + command + data + checksum + etx)
        return self.send(senddata)

    def closeGate(self):
        dummy = [0xFF]
        stx = [0x04]
        length = 0x00  # command + data length
        command = [0x04]  # 문닫기
        data = [00, 0x00, 0x00, 0x00]  # 10초간 문열기
        length = [0xFF & (len(data) + 1)]

        cs = length[0] + command[0]
        for d in data:
            cs = cs + d
        checksum = [0xFF & cs]

        # checksum=0x00 #length + command + data 16 digit +
        etx = [0x03]
        senddata = bytearray(dummy + stx + length + command + data + checksum + etx)
        return self.send(senddata)

    def status(self):
        dummy = [0xFF]
        stx = [0x04]
        length = 0x00  # command + data length
        command = [0x02]  # manuallock
        data = [0x00, 0x00, 0x00, 0x00]  # 10초간 문열기
        length = [0xFF & (len(data) + 1)]

        cs = length[0] + command[0]
        for d in data:
            cs = cs + d
        checksum = [0xFF & cs]

        # checksum=0x00 #length + command + data 16 digit +
        etx = [0x03]
        senddata = bytearray(dummy + stx + length + command + data + checksum + etx)
        return self.send(senddata)

    def setOneTimePassword(self, pstr):
        dummy = [0xFF]
        stx = [0x04]
        length = 0x00  # command + data length
        command = [0x05]  # 문열기
        data = [(int(pstr[0]) << 4) + int(pstr[1]), (int(pstr[2]) << 4) + int(pstr[3])]
        length = [0xFF & (len(data) + 1)]

        cs = length[0] + command[0]
        for d in data:
            cs = cs + d
        checksum = [0xFF & cs]

        # checksum=0x00 #length + command + data 16 digit +
        etx = [0x03]
        senddata = bytearray(dummy + stx + length + command + data + checksum + etx)
        return self.send(senddata)

    def clearOnetimePassword(self):
        dummy = [0xFF]
        stx = [0x04]
        length = 0x00  # command + data length
        command = [0x06]  # 문열기
        data = [00, 0x00, 0x00, 0x00]  # 0x00000000
        length = [0xFF & (len(data) + 1)]

        cs = length[0] + command[0]
        for d in data:
            cs = cs + d
        checksum = [0xFF & cs]

        # checksum=0x00 #length + command + data 16 digit +
        etx = [0x03]
        senddata = bytearray(dummy + stx + length + command + data + checksum + etx)
        return self.send(senddata)

    def getOnetimePassword(self):
        dummy = [0xFF]
        stx = [0x04]
        length = 0x00  # command + data length
        command = [0x07]  # 일회용 비밀번호 상태 조회
        data = [00, 0x00, 0x00, 0x00]  # 0x00000000
        length = [0xFF & (len(data) + 1)]

        cs = length[0] + command[0]
        for d in data:
            cs = cs + d
        checksum = [0xFF & cs]

        # checksum=0x00 #length + command + data 16 digit +
        etx = [0x03]
        senddata = bytearray(dummy + stx + length + command + data + checksum + etx)
        return self.send(senddata)

    def openGate(self, openTime=0):
        dummy = [0xFF]
        stx = [0x04]
        length = 0x00  # command + data length
        command = [0x03]  # 문열기
        data = [openTime, 0x00, 0x00, 0x00]  # 10초간 문열기
        length = [0xFF & (len(data) + 1)]

        cs = length[0] + command[0]
        for d in data:
            cs = cs + d
        checksum = [0xFF & cs]

        # checksum=0x00 #length + command + data 16 digit +
        etx = [0x03]
        senddata = bytearray(dummy + stx + length + command + data + checksum + etx)
        return self.send(senddata)

    def autoLock(self):
        dummy = [0xFF]
        stx = [0x04]
        length = 0x00  # command + data length
        command = [0x20]  # 문열기
        data = [0x00, 0x00, 0x00, 0x00]  # 10초간 문열기
        length = [0xFF & (len(data) + 1)]

        cs = length[0] + command[0]
        for d in data:
            cs = cs + d
        checksum = [0xFF & cs]

        # checksum=0x00 #length + command + data 16 digit +
        etx = [0x03]
        senddata = bytearray(dummy + stx + length + command + data + checksum + etx)
        return self.send(senddata)

    def manualLock(self):
        dummy = [0xFF]
        stx = [0x04]
        length = 0x00  # command + data length
        command = [0x21]  # manuallock
        data = [0x00, 0x00, 0x00, 0x00]  # 10초간 문열기
        length = [0xFF & (len(data) + 1)]

        cs = length[0] + command[0]
        for d in data:
            cs = cs + d
        checksum = [0xFF & cs]

        # checksum=0x00 #length + command + data 16 digit +
        etx = [0x03]
        senddata = bytearray(dummy + stx + length + command + data + checksum + etx)
        return self.send(senddata)

    def isSuccess(self, recv):
        if recv == None:
            return False

        if recv and len(recv) == 14:
            if recv[3] == 0x03:  # 열기
                # print('open time', recv[8])

                return recv[9] == 0x01

            if recv[3] == 0x04:  # 닫기

                return recv[8] == 0x01

            if recv[3] == 0x09:  # chage password
                return recv[8] == 0x01
        return False

    def doorOpenProcess(self):
        self.lock.acquire()
        self.connect()
        result = None

        try:
            recv = self.openGate(0)
            result = self.responseStatus(recv)
        except Exception as e:
            print(str(e))
        finally:
            self.close()
            self.lock.release()

        print(result)

        if result:
            print("WIKI Smartdoor is open start!!")
            return True
        else:
            return self.isDoorOpen()

    def doorCloseProcess(self):
        self.lock.acquire()
        self.connect()
        result = None

        try:
            recv = self.closeGate()
            result = self.responseStatus(recv)
        except Exception as e:
            print(str(e))
        finally:
            self.close()
            self.lock.release()

        print(result)

        if result:
            print("WIKI Smartdoor is close start!!")
            return True
        else:
            return self.isDoorOpen()

    def isDoorOpen(self):

        self.lock.acquire()
        result = None
        try:
            self.connect()
            recv = self.status()
            result = self.showStatus(recv)
        finally:
            self.close()
            self.lock.release()

        return result

    def guestkeyJoinProcess(self, passwd):
        self.lock.acquire()
        try:
            self.connect()
            recv = self.setOneTimePassword(passwd)
            result = self.responseStatus(recv)
        finally:
            self.close()
            self.lock.release()

        print("guestkeyJoinProcess [%s]" % result)

        return result

    def getGuestkey(self):
        self.lock.acquire()
        try:
            self.connect()
            recv = self.getOnetimePassword()
            result = self.responseStatus(recv)
            self.close()
        finally:
            self.lock.release()

        return result

    def clearGuestkey(self):
        self.lock.acquire()
        try:
            self.connect()
            recv = self.clearOnetimePassword()
            result = self.responseStatus(recv)
        finally:
            self.close()
            self.lock.release()
        return result


def main():
    cmds = ["isDoorOpen", "doorOpenProcess", "doorCloseProcess"]

    parser = argparse.ArgumentParser(prog="PROG")
    parser.add_argument("cmd", choices=cmds, help="bar help")
    parser.add_argument("-p", "--port", help="Hione doorlock serial port number")

    args = parser.parse_args()

    if not args.port:
        print("Error: Port number must be provided with -p or --port.")
        return

    obj = Hione(port=args.port)

    if args.cmd == "isDoorOpen":
        results = dict()
        results["result"] = obj.isDoorOpen()
        rs = lib.jsonencode(results)
        print(rs)
    elif args.cmd == "doorOpenProcess":
        results = dict()
        results["result"] = obj.doorOpenProcess()
        rs = lib.jsonencode(results)
        print(rs)
    elif args.cmd == "doorCloseProcess":
        results = dict()
        results["result"] = obj.doorOpenProcess()
        rs = lib.jsonencode(results)
        print(rs)


class NoDataException(Exception):
    def __init__(self, str="No Data"):
        super().__init__(str)


if __name__ == "__main__":
    main()
