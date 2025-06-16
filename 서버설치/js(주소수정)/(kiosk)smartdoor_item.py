# ~/www/kiosk/python/elcsoft/controller/smartdoor_item.py

import tts
import lib
import threading
import elcsoft.components
import elcsoft.model.smartdoor
import elcsoft.model.smartdoor_item
import elcsoft.controller.smartdoor

global_config = lib.getConfigByJsonFile('/home/pi/www/python/config.json')

# 소지품 가져오기
def getItems(user_id) :
    global global_config
    
    downloadProcess()

    obj = elcsoft.model.smartdoor.Smartdoor()
    obj.getDataRecent()

    smartdoorItemObj = elcsoft.model.smartdoor_item.SmartdoorItem()

    query = dict()
    query['table'] = "smartdoor_item"
    query['where'] = "smartdoor_id='%s' AND user_id='%s'" % (obj.__pkValue__, user_id)
    query['orderby'] = "smartdoor_item_id"
    #query['isEcho'] = True

    results = smartdoorItemObj.getResults(**query)
    array = list()
    for result in results:
        smartdoorItemObj = elcsoft.model.smartdoor_item.SmartdoorItem()
        smartdoorItemObj.setData(result)
        array.append(smartdoorItemObj.toDict())
    
    th = threading.Thread(target=createTTS, args=(array,))
    th.demon = True
    th.start()

    return array

#음성 녹음
def createTTS(array=None) :
    global global_config

    if not lib.isSetupTTS(global_config) : 
        return False

    starts_with = "item"

    text = ""
    file = global_config['tts']['path'] + starts_with
    
    for o in array :
        if text != "" :
            text = text + ", "

        text = text + o['name']

        file = file + "_%s" % o['smartdoor_item_id']

    if text == '':
        return True
    
    text = "외출시에는 " + text + "를 꼭 챙겨 나가세요."
    file = file + ".wav"

    return tts.saveFile(file, text)
    
def joinProcess(**kwargs):
    url = 'https://api2.hizib.wikibox.kr/SmartdoorItem'

    data = dict()

    if not 'user_id' in kwargs:
        raise Exception("회원정보를 입력해 주세요.")
    else :
        data['user_id'] = kwargs['user_id']
    
    if not 'name' in kwargs:
        raise Exception("소지품명을 입력해 주세요.")
    else :
        data['name'] = kwargs['name']

    lib.log("/SmartdoorItem/joinProcess %s" % data)

    #data['file'] = kwargs['file']
    obj = elcsoft.model.smartdoor_item.SmartdoorItem()
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
        raise Exception("소지품 등록 실패! 원인 - %s" % obj.__errorMsg__)
    
    #tts 파일삭제
    lib.delete_files(global_config['tts']['path'], "item", ".wav")

    return obj

def updateProcess(**kwargs):
    data = dict()

    if not 'smartdoor_item_id' in kwargs:
        raise Exception("소지품 정보를 입력해 주세요.")
    else :
        data['smartdoor_item_id'] = kwargs['smartdoor_item_id']

    if not 'user_id' in kwargs:
        raise Exception("회원정보를 입력해 주세요.")
    else :
        data['user_id'] = kwargs['user_id']
    
    if not 'name' in kwargs:
        raise Exception("소지품명을 입력해 주세요.")
    else :
        data['name'] = kwargs['name']

    url = 'https://api2.hizib.wikibox.kr/SmartdoorItem/%s' % data['smartdoor_item_id']

    lib.log("/SmartdoorItem/modifyProcess %s" % data)

    #data['file'] = kwargs['file']
    obj = elcsoft.model.smartdoor_item.SmartdoorItem()
    obj.getData(data['smartdoor_item_id'])

    if obj.__pkValue__ <= 0:
        raise Exception("존재하지 않는 소지품 정보입니다.")

    token = elcsoft.controller.smartdoor.getToken()

    result = lib.restapi(method="put", url=url, data=lib.jsonencode(data), token=token, isDebug=True)
    lib.log(result)
    obj.fromDict(result)

    if not obj.save():
        raise Exception("소지품 수정 실패! 원인 - %s" % obj.__errorMsg__)
    
    #tts 파일삭제
    lib.delete_files(global_config['tts']['path'], "item", ".wav")

    return obj

def deleteProcess(**kwargs):
    data = dict()

    if not 'smartdoor_item_id' in kwargs:
        raise Exception("소지품 정보를 입력해 주세요.")
    else :
        data['smartdoor_item_id'] = kwargs['smartdoor_item_id']

    url = 'https://api2.hizib.wikibox.kr/SmartdoorItem/%s' % data['smartdoor_item_id']

    lib.log("/SmartdoorItem/deleteProcess %s" % data)

    #data['file'] = kwargs['file']
    obj = elcsoft.model.smartdoor_item.SmartdoorItem()
    obj.getData(data['smartdoor_item_id'])

    if obj.__pkValue__ <= 0:
        raise Exception("존재하지 않는 소지품 정보입니다.")

    token = elcsoft.controller.smartdoor.getToken()

    result = lib.restapi(method="delete", url=url, data=lib.jsonencode(data), token=token, isDebug=True)
    lib.log(result)

    if not obj.delete():
        raise Exception("소지품 삭제 실패! 원인 - %s" % obj.__errorMsg__)
    
    #tts 파일삭제
    lib.delete_files(global_config['tts']['path'], "item", ".wav")

    return True

# downloadProcess
def downloadProcess(**kwargs):
    token = elcsoft.controller.smartdoor.getToken()

    url = 'https://api2.hizib.wikibox.kr/SmartdoorItem/lists'
    #result = lib.restapi(method="get", url=url, token=token, isDebug=True)
    result = lib.restapi(method="get", url=url, token=token)
    #print(result)

    for data in result['lists'] :
        obj = elcsoft.model.smartdoor_item.SmartdoorItem()
        obj.fromDict(data)

        if 'smartdoorObj' in data :
            obj.smartdoorObj.fromDict(data['smartdoorObj'])
            if not obj.smartdoorObj.save() :
                raise Exception("스마트도어 정보를 저장하는데 실패하였습니다. 원인 - %s" % obj.smartdoorObj.__errorMsg__)

        if 'userObj' in data :
            obj.userObj.fromDict(data['userObj'])
            if not obj.userObj.save() :
                raise Exception("사용자 정보를 저장하는데 실패하였습니다. 원인 - %s" % obj.userObj.__errorMsg__)

        if not obj.save() :
            raise Exception("소지품 정보를 저장하는데 실패하였습니다. 원인 - %s" % obj.__errorMsg__)

    return True
