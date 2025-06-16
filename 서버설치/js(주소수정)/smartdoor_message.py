# ~/www/kiosk/python/elcsoft/controller/smartdoor_message.py

import tts
import lib
import threading
import datetime
import elcsoft.components
import elcsoft.model.smartdoor
import elcsoft.model.smartdoor_message
import elcsoft.controller.smartdoor

global_config = lib.getConfigByJsonFile('/home/pi/www/python/config.json')

# 메세지 가져오기
def getMessages(to_user_id) :
    global global_config

    downloadProcess()

    obj = elcsoft.model.smartdoor_message.SmartdoorMessage()

    listObj = elcsoft.components.Components()
    listObj.setJoin("SmartdoorMessage", "a", "a.to_user_id=%s" % to_user_id)
    listObj.setJoin("User", "b", "b.user_id=a.from_user_id")
    listObj.setSort("smartdoor_message_id", "desc")

    # 현재 시간에서 24시간 전의 시간 계산
    twenty_four_hours_ago = datetime.datetime.now() - datetime.timedelta(days=1)
    
    # regDate 조건을 24시간 전으로 수정
    listObj.setAndCondition("a.regDate >= '%s'" % twenty_four_hours_ago.strftime("%Y-%m-%d %H:%M:%S"))
    
    results = listObj.getOnlyResult()

    array = list()
    for result in results :
        #print(result)
        obj = elcsoft.model.smartdoor_message.SmartdoorMessage()
        obj.setData(result, 'a')
        obj.fromUserObj.setData(result, 'b')
        array.append(obj.toDict())

    array.reverse()
    
    th = threading.Thread(target=createTTS, args=(array,))
    th.demon = True
    th.start()

    return array 

#음성 녹음
def createTTS(array) :
    global global_config

    if not lib.isSetupTTS(global_config) : 
        return False
    
    starts_with = "message"

    text = ""
    file = global_config['tts']['path'] + starts_with
    for o in array :
        #print(o.fromUserObj)
        if text != "" :
            text = text + "\n"

        if o['fromUserObj']['nickname'] != "" :
            text = text + o['fromUserObj']['nickname']
        else :
            text = text + o['fromUserObj']['name']

        text = text + "으로부터 메세지가 있습니다.   " + o['msg']

        file = file + "_%s" % o['smartdoor_message_id']
    if text == '':
        return True
    
    file = file + ".wav"

    return tts.saveFile(file, text)
    
def joinProcess(**kwargs):
    url = 'https://api2.hizib.wikibox.kr/SmartdoorMessage'

    data = dict()

    if not 'from_user_id' in kwargs:
        raise Exception("보내는 사람 정보를 입력해 주세요.")
    else :
        data['from_user_id'] = kwargs['from_user_id']

    if not 'to_user_id' in kwargs:
        raise Exception("받는 사람 정보를 입력해 주세요.")
    else :
        data['to_user_id'] = kwargs['to_user_id']
    
    if not 'msg' in kwargs:
        raise Exception("메세지 내용을 입력해 주세요.")
    else :
        data['msg'] = kwargs['msg']

    lib.log("/SmartdoorMessage/joinProcess %s" % data)

    #data['file'] = kwargs['file']
    obj = elcsoft.model.smartdoor_message.SmartdoorMessage()
    obj.smartdoorObj.getDataRecent()

    if obj.smartdoorObj.__pkValue__ <= 0:
        raise Exception("스마트도어 정보가 없습니다.")
    else :
        obj.smartdoor_id = obj.smartdoorObj.__pkValue__

    token = elcsoft.controller.smartdoor.getToken()

    result = lib.restapi(method="post", url=url, data=lib.jsonencode(data), token=token, isDebug=True)
    lib.log(result)
    obj.fromDict(result)

    if not obj.save():
        raise Exception("메세지 등록 실패! 원인 - %s" % obj.__errorMsg__)
    
    #tts 파일삭제
    lib.delete_files(global_config['tts']['path'], "message", ".wav")

    return obj

def updateProcess(**kwargs):
    data = dict()

    if not 'smartdoor_message_id' in kwargs:
        raise Exception("메세지 정보를 입력해 주세요.")
    else :
        data['smartdoor_message_id'] = kwargs['smartdoor_message_id']

    if not 'from_user_id' in kwargs:
        raise Exception("보내는 사람 정보를 입력해 주세요.")
    else :
        data['from_user_id'] = kwargs['from_user_id']

    if not 'to_user_id' in kwargs:
        raise Exception("받는 사람 정보를 입력해 주세요.")
    else :
        data['to_user_id'] = kwargs['to_user_id']
    
    if not 'msg' in kwargs:
        raise Exception("메세지 내용을 입력해 주세요.")
    else :
        data['msg'] = kwargs['msg']

    url = 'https://api2.hizib.wikibox.kr/SmartdoorMessage/%s' % data['smartdoor_message_id']

    lib.log("/SmartdoorMessage/modifyProcess %s" % data)

    #data['file'] = kwargs['file']
    obj = elcsoft.model.smartdoor_message.SmartdoorMessage()
    obj.getData(data['smartdoor_message_id'])

    if obj.__pkValue__ <= 0:
        raise Exception("존재하지 않는 메세지 정보입니다.")

    token = elcsoft.controller.smartdoor.getToken()

    result = lib.restapi(method="put", url=url, data=lib.jsonencode(data), token=token, isDebug=True)
    lib.log(result)
    obj.fromDict(result)

    if not obj.save():
        return False
    
    #tts 파일삭제
    lib.delete_files(global_config['tts']['path'], "message", ".wav")

    return obj

def deleteProcess(**kwargs):
    data = dict()

    if not 'smartdoor_message_id' in kwargs:
        raise Exception("메세지 정보를 입력해 주세요.")
    else :
        data['smartdoor_message_id'] = kwargs['smartdoor_message_id']

    url = 'https://api2.hizib.wikibox.kr/SmartdoorMessage/%s' % data['smartdoor_message_id']

    lib.log("/SmartdoorMessage/deleteProcess %s" % data)

    #data['file'] = kwargs['file']
    obj = elcsoft.model.smartdoor_message.SmartdoorMessage()
    obj.getData(data['smartdoor_notice_id'])

    if obj.__pkValue__ <= 0:
        raise Exception("존재하지 않는 메세지 정보입니다.")
    
    token = elcsoft.controller.smartdoor.getToken()

    result = lib.restapi(method="delete", url=url, data=lib.jsonencode(data), token=token, isDebug=True)
    lib.log(result)

    if not obj.delete():
        raise Exception("메세지 삭제 실패! 원인 - %s" % obj.__errorMsg__)
    
    #tts 파일삭제
    lib.delete_files(global_config['tts']['path'], "message", ".wav")

    return True

# downloadProcess
def downloadProcess(**kwargs):
    token = elcsoft.controller.smartdoor.getToken()

    url = 'https://api2.hizib.wikibox.kr/SmartdoorMessage/lists'
    #result = lib.restapi(method="get", url=url, token=token, isDebug=True)
    result = lib.restapi(method="get", url=url, token=token)

    for data in result['lists'] :
        #print(data)
        obj = elcsoft.model.smartdoor_message.SmartdoorMessage()
        obj.fromDict(data)

        obj.toUserObj.fromDict(data['toUserObj'])
        if not obj.toUserObj.save():
            raise Exception("받는 회원 정보 저장하는데 실패하였습니다. 원인 - %s" % obj.smartdoorObj.__errorMsg__)

        obj.fromUserObj.fromDict(data['fromUserObj'])
        if not obj.fromUserObj.save():
            raise Exception("보내는 회원 정보 저장하는데 실패하였습니다. 원인 - %s" % obj.smartdoorObj.__errorMsg__)

        if not obj.save() :
            raise Exception("메세지 정보를 저장하는데 실패하였습니다. 원인 - %s" % obj.__errorMsg__)
    return True
