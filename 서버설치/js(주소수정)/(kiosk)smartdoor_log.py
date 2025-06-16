# ~/www/kiosk/python/elcsoft/controller/smartdoor_log.py

import lib

import elcsoft.model.code
import elcsoft.model.user
import elcsoft.model.smartdoor_log

import elcsoft.controller.smartdoor

#출입기록
def logProcess(**kwargs):
    if 'user_id' in kwargs and kwargs['user_id'] != None:
        user_id = int(kwargs['user_id'])
    else:
        user_id = 0

    if 'type' in kwargs and kwargs['type'] != None:
        type = int(kwargs['type'])
    else:
        raise Exception("Event 정보가 없습니다.")

    if 'code' in kwargs and kwargs['code'] != None:
        code = kwargs['code']
    else:
        code = "0000"

    if 'name' in kwargs and kwargs['name'] != None :
        name = kwargs['name']
    else :
        name = ""

        if user_id :
            userObj = elcsoft.model.user.User()
            userObj.getData(user_id)
            name = userObj.name  + " "

        codeObj = elcsoft.model.code.Code()
        codeObj.updateAllProcess(gcode='SMARTDOOR_LOG_TYPE')

        codeObj.getDataByCondition("gcode='SMARTDOOR_LOG_TYPE' AND code='%s'" % str(type).zfill(2))
        if codeObj.__pkValue__ <= 0 :
            codeObj.updateAllProcess(gcode='SMARTDOOR_LOG_TYPE')
            codeObj.getDataByCondition("gcode='SMARTDOOR_LOG_TYPE' AND code='%s'" % str(type).zfill(2))

        if codeObj.nickname != "" :
            name = name + codeObj.nickname + " 이벤트가 발생하였습니다."
        elif codeObj.name != "" :
            name = name + codeObj.name + " 이벤트가 발생하였습니다."
        else :
            name = name + " 이벤트가 발생하였습니다."

    if 'regDate' in kwargs and kwargs['regDate'] != None:
        regDate = kwargs['regDate']
    else:
        regDate = lib.now()

    url = "https://api2.hizib.wikibox.kr/SmartdoorLog"
    data = dict()
    data["user_id"] = user_id
    data["code"] = code
    data["name"] = name
    data["regDate"] = regDate
    #print(data)

    token = elcsoft.controller.smartdoor.getToken()

    result = lib.restapi(method="post", url=url, data=data, token=token, isDebug=True)
    #print(result)

    obj = elcsoft.model.smartdoor_log.SmartdoorLog()
    obj.fromDict(result)

    if not obj.save() :
        raise Exception(obj.__errorMsg__)

    return True
