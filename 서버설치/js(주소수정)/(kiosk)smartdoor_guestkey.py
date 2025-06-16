# ~/www/kiosk/python/elcsoft/controller/smartdoor_guestkey.py

import lib
import elcsoft.model.smartdoor_guestkey
import elcsoft.controller.smartdoor
import elcsoft.controller.user

# 기한 만료 처리
def canceledProcess(**kwargs):
    if not 'smartdoor_guestkey_id' in kwargs :
        raise Exception('게스트키 정보가 없습니다.')
    
    obj = elcsoft.model.smartdoor_guestkey.SmartdoorGuestkey()
    obj.getData(kwargs['smartdoor_guestkey_id'])

    if obj.__pkValue__ <= 0:
        raise Exception( "기한 만료 처리할 게스트키 정보가 없습니다.")

    url = "https://api2.hizib.wikibox.kr/SmartdoorGuestkey/%s" % obj.__pkValue__
    data = {'status': 9}

    token = elcsoft.controller.smartdoor.getToken()

    result = lib.restapi(method="PUT", url=url, data=data, token=token)
    obj.setData(result)

    if not obj.save() :
        raise Exception("기한 만료 처리하는데 실패하였습니다.")

    return obj

# downloadProcess
def downloadProcess(**kwargs):
    token = elcsoft.controller.smartdoor.getToken()

    url = 'https://api2.hizib.wikibox.kr/SmartdoorGuestkey/lists'
    #result = lib.restapi(method="get", url=url, token=token, isDebug=True)
    result = lib.restapi(method="get", url=url, token=token)
    #print(result)

    for data in result['lists'] :
        obj = elcsoft.model.smartdoor_guestkey.SmartdoorGuestkey()
        obj.fromDict(data)
        obj.smartdoorObj.fromDict(data['smartdoorObj'])
        obj.userObj.fromDict(data['userObj'])

        if not obj.smartdoorObj.save():
            elcsoft.controller.smartdoor.downloadProcess(token=token)

        if not obj.userObj.save():
            elcsoft.controller.user.downloadProcess(user_id=data['user_id'], token=token)

        if not obj.save():
            raise Exception("게스트키 정보 다운 실패! 원인 - %s" % obj.smartdoorObj.__errorMsg__)

    return obj

#updateProcess
def updateProcess():
    obj = elcsoft.model.smartdoor_guestkey.SmartdoorGuestkey()

    if obj.__pkValue__ <= 0 :
        raise Exception("존재하지 않는 게스트키 정보입니다.")

    obj.updateByCondition("status='1'", "'%s' < startDate" % lib.now())
    obj.updateByCondition("status='2'", "startDate<='%s' AND '%s' <= stopDate" % (lib.now(), lib.now()))
    obj.updateByCondition("status='3'", "stopDate<'%s'" % lib.now())

    return True
