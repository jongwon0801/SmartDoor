# ~/www/kiosk/python/elcsoft/controller/smartdoor_cmd.py

import lib
import elcsoft.model.user
import elcsoft.model.smartdoor
import elcsoft.model.smartdoor_cmd
import elcsoft.model.smartdoor_guestkey

import elcsoft.controller.smartdoor
import elcsoft.controller.smartdoor_log
import elcsoft.controller.smartdoor_guestkey

# 문상태조회
def isDoorOpen(self) :
    return self.isDoorlock()

# 문열기
def doorOpenProcess(self) :
    return self.doorOpenProcess()

# 문닫기
def doorCloseProcess(self):
    return self.doorCloseProcess()

# QR코드로 문열기
def doorOpenByQrProcess(self, pkValue) :
    self.doorOpenByQrProcess(pkValue)

# KIOSK에서 문열기
def doorOpenAtKioskProcess(self) :
    self.doorOpenAtKioskProcess()

# KIOSK에서 문닫기
def doorCloseAtKioskProcess(self) :
    self.doorCloseAtKioskProcess()

# APP에서 문열기
def doorOpenAtAppProcess(self, user_id) :
    self.doorOpenAtAppProcess(user_id)

# App에서 문닫기
def doorCloseAtAppProcess(self, user_id) :
    self.doorCloseAtAppProcess(user_id)

# APP에서 문열기
def doorOpenAtWebProcess(self, user_id) :
    self.doorOpenAtWebProcess(user_id)

# App에서 문닫기
def doorCloseAtWebProcess(self, user_id) :
    self.doorCloseAtWebProcess(user_id)

#mqtt로 관리자가 문열기
def doorOpenByAdminProcess(self) :
    self.doorOpenByAdminProcess()

#mqtt로 관리자가 문열기
def doorCloseByAdminProcess(self) :
    self.doorCloseByAdminProcess()

# FACE로 문열기
def doorOpenByFaceProcess(self, user_id) :
    self.doorOpenByFaceProcess(user_id)

#문열기 상태 처리
def doorOpenStatusProcess(self, smartdoor_cmd_id=None) :
    self.doorOpenStatusProcess(smartdoor_cmd_id)

#문닫기 상태 처리
def doorCloseStatusProcess(self, smartdoor_cmd_id=None) :
    self.doorCloseStatusProcess(smartdoor_cmd_id)
        
# 스마트도어 명령 기록
def smartdoorCmdProcess(type, user_id=0) :
    obj = elcsoft.model.smartdoor_cmd.SmartdoorCmd()
    obj.user_id = int(user_id)
    obj.type = int(type)
    obj.code = ''
    obj.name = ''
    obj.regDate = lib.now()
    if not obj.save() :
        raise Exception(f"스마트도어 명령 기록 실패! 원인 - {obj.__errorMsg__}")

    return obj

# Guestkey 등록
def guestkeyJoinProcess(**kwargs):
    print(kwargs)
    startDate = kwargs.get('startDate', '2199-12-31 23:59:59')
    stopDate = kwargs.get('stopDate', '1900-01-01 00:00:00')
    user_id = kwargs.get('user_id', 0)
    handphone = kwargs.get('handphone', '')
    passwd = kwargs.get('passwd', '')

    if lib.getDatetime(startDate) > lib.getDatetime(stopDate) :
        raise Exception("게스트키 시작일자가 만료일자 보다 이전입니다.")

    if lib.isCurrentTimeBefore(stopDate) :
        raise Exception("게스트키 만료일자가 현재 시간 이전입니다.")
    
    token = elcsoft.controller.smartdoor.getToken()

    result = lib.restapi(method="POST", url="https://api2.hizib.wikibox.kr/Smartdoor/guestkeyJoinProcess", data={"user_id": int(user_id), "handphone": handphone, "passwd": passwd, "startDate": startDate, "stopDate": stopDate}, token=token)
    #logger.Logger._LOGGER.info(result)

    #게스트키 등록
    #ho = hione.Hione()
    #ho.guestkeyJoinProcess(passwd)

    o = elcsoft.model.smartdoor_guestkey.SmartdoorGuestkey()
    o.setData(result)

    if not o.save() :
        raise Exception("게스트키 발행 정보를 가져오는데 실패하였습니다.")

    #상태 업데이트
    o.updateProcess()

    return o.toDict()

# 문열기 성공처리
def doorOpenedProcess(smartdoor_cmd_id=None):
    obj = elcsoft.model.smartdoor_cmd.SmartdoorCmd()
    if smartdoor_cmd_id is not None:
        obj.getData(smartdoor_cmd_id)
    else :
        obj.getDataRecent()

    if obj.__pkValue__ <= 0 :
        return True
    
    obj.code = "0000"
    if not obj.save() :
        raise Exception("문열림 상태 저장 실패!")

    try :
        elcsoft.controller.smartdoor_log.logProcess(user_id=obj.user_id, type=obj.type, code=obj.code, regDate=lib.now())
        obj.delete()
    except Exception as e :
        lib.log(str(e))

    return True

# 문열기 실패처리
def doorOpenFailProcess(smartdoor_cmd_id=None):
    obj = elcsoft.model.smartdoor_cmd.SmartdoorCmd()
    if smartdoor_cmd_id is not None:
        obj.getData(smartdoor_cmd_id)
    else :
        obj.getDataRecent()

    if obj.__pkValue__ <= 0 :
        return True
    
    obj.code = "9999"

    if not obj.save() :
        raise Exception("문열림 상태 저장 실패!")

    try :
        elcsoft.controller.smartdoor_log.logProcess(user_id=obj.user_id, type=obj.type, code=obj.code, regDate=lib.now())
        obj.delete()
    except Exception as e :
        lib.log(str(e))

    return True


# 문닫기 성공처리
def doorClosedProcess(smartdoor_cmd_id=None):
    obj = elcsoft.model.smartdoor_cmd.SmartdoorCmd()
    if smartdoor_cmd_id is not None:
        obj.getData(smartdoor_cmd_id)
    else :
        obj.getDataRecent()

    if obj.__pkValue__ <= 0 :
        return True
    
    obj.code = "0000"
    if not obj.save() :
        raise Exception("문닫힘 상태 저장 실패!")

    try :
        elcsoft.controller.smartdoor_log.logProcess(user_id=obj.user_id, type=obj.type, code=obj.code, regDate=lib.now())
        obj.delete()
    except Exception as e :
        lib.log(str(e))

    return True

# 문열기 실패처리
def doorCloseFailProcess(smartdoor_cmd_id=None):
    obj = elcsoft.model.smartdoor_cmd.SmartdoorCmd()
    if smartdoor_cmd_id is not None:
        obj.getData(smartdoor_cmd_id)
    else :
        obj.getDataRecent()

    if obj.__pkValue__ <= 0 :
        return True
    
    obj.code = "9999"

    if not obj.save() :
        raise Exception("문닫힘 상태 저장 실패!")

    try :
        elcsoft.controller.smartdoor_log.logProcess(user_id=obj.user_id, type=obj.type, code=obj.code, regDate=lib.now())
        obj.delete()
    except Exception as e :
        lib.log(str(e))

    return True

# 문열림 닫힘 상태를 저장
'''
def setIsDoorOpenProcess(isOpen):
    #print("setIsDoorOpenProcess")
    obj = elcsoft.model.smartdoor.Smartdoor()

    if obj.__pkValue__ <= 0 :
        obj.getDataRecent()

    if obj.__pkValue__ <= 0 :
        raise Exception("스마트도어 정보가 없습니다.")

    url = 'https://api2.hizib.wikibox.kr/Smartdoor/setIsDoorOpen'
    data = dict()
    if isOpen:
        data['isDoorOpen'] = 1
    else:
        data['isDoorOpen'] = 0

    result = lib.restapi(method="post", url=url, data=lib.jsonencode(data), token=getToken(), isDebug=False)
    #print(result)
    obj.isDoorOpen = data['isDoorOpen']

    if not obj.save():
        raise Exception("문 상태를 저장하는데 실패하였습니다.")

    return True

'''
