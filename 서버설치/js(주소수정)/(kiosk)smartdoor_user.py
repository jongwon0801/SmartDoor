# ~/www/kiosk/python/elcsoft/controller/smartdoor_user.py

import lib
import asyncio
import face
import threading

import elcsoft.components
import elcsoft.controller.user
import elcsoft.model.smartdoor
import elcsoft.model.smartdoor_user
import elcsoft.controller.smartdoor
import elcsoft.controller.smartdoor_user

# syncSmartdoorUsers
def syncSmartdoorUsers() :
    obj = elcsoft.model.smartdoor.Smartdoor()
    obj.getDataRecent()

    if obj.__pkValue__ <= 0:
        raise Exception("스마트도어 정보가 없습니다.")

    downloadProcess()
    return True

#비동기함수
async def asyncSyncSmartdoorUsers():
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, syncSmartdoorUsers)

# joinProcess
def joinProcess(**kwargs):
    smartdoor_id = int(kwargs.get('smartdoor_id', 0))
    user_id = int(kwargs.get('user_id', 0))

    if smartdoor_id <= 0 :
        raise Exception("스마트도어 정보가 없습니다.")

    if user_id <= 0 :
        raise Exception("회원정보가 없습니다.")

    smartdoorObj = elcsoft.model.smartdoor.Smartdoor()
    smartdoorObj.getData(smartdoor_id)

    #내부 데이터 베이스 등록여부
    obj = elcsoft.model.smartdoor_user.SmartdoorUser()
    obj.getDataByCondition("smartdoor_id='%s' AND user_id='%s'" % (smartdoorObj.__pkValue__, user_id))
                           
    if obj.__pkValue__ > 0:
        raise Exception("이미 등록된 스마트도어 사용자입니다.")

    obj.smartdoor_id = smartdoorObj.__pkValue__
    obj.user_id = user_id

    #서버 등록 요청
    url = 'https://api2.hizib.wikibox.kr/SmartdoorUser/joinProcess'
    data = obj.toJson()
    lib.log("/SmartdoorUser/joinProcess %s" % data)
    
    try :
        result = lib.restapi(method="post", url=url, data=data, token=elcsoft.controller.smartdoor.getToken())
        lib.log(result)
        obj.fromDict(result)
        if not obj.save():
            raise Exception("스마트도어 사용자 정보를 저장하는데 실패하였습니다.")
    except Exception as e:
        downloadProcess()
        obj.getDataByCondition("smartdoor_id='%s' AND user_id='%s'" % (smartdoorObj.__pkValue__, user_id))

    th = threading.Thread(target=trainProcess)
    th.demon = True
    th.start()

    return obj

# updateProcess
def updateProcess(**kwargs):
    user_id = int(kwargs.get('user_id', 0))

    if user_id <= 0 :
        raise Exception("회원정보가 없습니다.")

    smartdoorObj = elcsoft.model.smartdoor.Smartdoor()
    smartdoorObj.getDataRecent()

    #내부 데이터 베이스 등록여부
    obj = elcsoft.model.smartdoor_user.SmartdoorUser()
    obj.getDataByCondition("smartdoor_id='%s' AND user_id='%s'" % (smartdoorObj.__pkValue__, user_id), 1)
                           
    if obj.__pkValue__ <= 0:
        raise Exception("등록되지 않은 스마트도어 사용자입니다.")

    #서버 등록 요청
    url = 'https://api2.hizib.wikibox.kr/SmartdoorUser/%s' % obj.__pkValue__
    lib.log(url)
    lib.log("/SmartdoorUser/updateProcess %s" % obj.__pkValue__)

    data = dict()
    data['isDoorbell'] = kwargs.get('isDoorbell')
    data['isAccessRecord'] = kwargs.get('isAccessRecord')
    data['isMotionDetect'] = kwargs.get('isMotionDetect')
    
    try :
        result = lib.restapi(method="put", url=url, data=data, token=elcsoft.controller.smartdoor.getToken())
        lib.log(result)
        obj.fromDict(result)

        if not obj.save():
            raise Exception("스마트도어 사용자 정보를 수정하는데 실패하였습니다.")
    except Exception as e:
        lib.log(e)
        downloadProcess()

    return True
# deleteProcess
def deleteProcess(**kwargs):
    user_id = int(kwargs.get('user_id', 0))

    if user_id <= 0 :
        raise Exception("회원정보가 없습니다.")

    smartdoorObj = elcsoft.model.smartdoor.Smartdoor()
    smartdoorObj.getDataRecent()

    #내부 데이터 베이스 등록여부
    obj = elcsoft.model.smartdoor_user.SmartdoorUser()
    obj.getDataByCondition("smartdoor_id='%s' AND user_id='%s'" % (smartdoorObj.__pkValue__, user_id), 1)
                           
    if obj.__pkValue__ <= 0:
        raise Exception("등록되지 않은 스마트도어 사용자입니다.")

    #서버 등록 요청
    url = 'https://api2.hizib.wikibox.kr/SmartdoorUser/%s' % obj.__pkValue__
    lib.log(url)
    lib.log("/SmartdoorUser/deleteProcess %s" % obj.__pkValue__)
    
    try :
        result = lib.restapi(method="delete", url=url, token=elcsoft.controller.smartdoor.getToken())
        lib.log(result)

        if not obj.delete():
            raise Exception("스마트도어 사용자 정보를 삭제하는데 실패하였습니다.")
    except Exception as e:
        lib.log(e)
        downloadProcess()

    th = threading.Thread(target=trainProcess)
    th.demon = True
    th.start()

    return True

# me
def me(**kwargs):
    user_id = int(kwargs.get('user_id', 0))

    if user_id <= 0 :
        raise Exception("회원정보가 없습니다.")

    smartdoorObj = elcsoft.model.smartdoor.Smartdoor()
    smartdoorObj.getDataRecent()

    #내부 데이터 베이스 등록여부
    obj = elcsoft.model.smartdoor_user.SmartdoorUser()
    obj.getDataByCondition("smartdoor_id='%s' AND user_id='%s'" % (smartdoorObj.__pkValue__, user_id))
                           
    if obj.__pkValue__ <= 0:
        downloadProcess()
        obj.getDataByCondition("smartdoor_id='%s' AND user_id='%s'" % (smartdoorObj.__pkValue__, user_id))

    if obj.__pkValue__ <= 0:
        raise Exception("등록되지 않은 스마트도어 사용자 정보입니다.")

    return obj

# downloadProcess
def downloadProcess(**kwargs):
    token = elcsoft.controller.smartdoor.getToken()

    url = 'https://api2.hizib.wikibox.kr/SmartdoorUser/lists'
    #result = lib.restapi(method="get", url=url, token=token, isDebug=True)
    result = lib.restapi(method="get", url=url, token=token)

    smartdoor_users = list()
    users = list()

    path = '/home/pi/www/image/user'
    pathes = lib.get_directories(path)

    for data in result['lists'] :
        obj = elcsoft.model.smartdoor_user.SmartdoorUser()
        obj.fromDict(data)

        obj.userObj.fromDict(data['userObj'])
        if not obj.userObj.save() :
            raise Exception("회원정보를 저장하는데 실패하였습니다. 원인 - %s" % obj.userObj.__errorMsg__)
        else :
            if not obj.save() :
                raise Exception("스마트도어 사용자 정보를 저장하는데 실패하였습니다. 원인 - %s" % obj.__errorMsg__)
            else :
                obj.user_id = obj.userObj.__pkValue__
                users.append(obj.user_id)

        obj.smartdoorObj.fromDict(data['smartdoorObj'])
        if not obj.smartdoorObj.save() :
            raise Exception("스마트도어 저장하는데 실패하였습니다. 원인 - %s" % obj.smartdoorObj.__errorMsg__)

        obj.fromDict(data)
        if not obj.save() :
            raise Exception("스마트도어 사용자 정보를 저장하는데 실패하였습니다. 원인 - %s" % obj.__errorMsg__)
        else :
            smartdoor_users.append(obj.__pkValue__)

    if len(smartdoor_users) :
        condition = ""
        for i in smartdoor_users :
            if condition != "" :
                condition = condition + " AND "
            condition = condition + "smartdoor_user_id!=%s" % i

        if not obj.deleteByCondition(condition) :
            raise Exception("사용하지 않는 스마트도어사용자를 삭제하는데 실패하였습니다.")
        
    if len(users) :
        condition = ""
        for i in users :
            if condition != "" :
                condition = condition + " AND "
            condition = condition + "user_id!=%s" % i
        
        if not obj.userObj.deleteByCondition(condition) :
            raise Exception("사용하지 않는 회원정보를 삭제하는데 실패하였습니다.")

    return True

# downloadProcess
def trainProcess():
    smartdoorObj = elcsoft.model.smartdoor.Smartdoor()
    smartdoorObj.getDataRecent()

    if smartdoorObj.__pkValue__ <= 0:
        return True

    listObj = elcsoft.components.Components()
    listObj.setJoin("SmartdoorUser", "a", "a.smartdoor_id='%s'" % smartdoorObj.__pkValue__)
    listObj.setJoin("User", "b", "b.user_id=a.user_id")
    
    results = listObj.getResults()

    users = list()

    path = '/home/pi/www/image/user'
    pathes = lib.get_directories(path)

    for data in results :
        obj = elcsoft.model.smartdoor_user.SmartdoorUser()
        obj.setData(data, 'a')

        obj.userObj.setData(data, 'b')
        
        #사진 이미지 다운로드
        elcsoft.controller.user.pictureDownloadProcess(user_id=obj.user_id)
        
        #안면 인식용 사진 다운로드
        elcsoft.controller.user.facesDownloadProcess(user_id=obj.user_id)
            
        users.append(obj.user_id)        

    lib.delete_directories_except_users('/home/pi/www/image/user/', users)

    if not lib.compare_lists(pathes, users) :
        o = face.Face()
        o.train()

    return True
