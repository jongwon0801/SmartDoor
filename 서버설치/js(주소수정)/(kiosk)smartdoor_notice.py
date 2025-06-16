# ~/www/kiosk/python/elcsoft/controller/smartdoor_notice.py

import tts
import lib
import threading
import elcsoft.components
import elcsoft.model.smartdoor
import elcsoft.model.smartdoor_notice
import elcsoft.controller.smartdoor

global_config = lib.getConfigByJsonFile('/home/pi/www/python/config.json')

# 공지사항 가져오기
def getNotices() :
    global global_config
    
    downloadProcess()

    obj = elcsoft.model.smartdoor.Smartdoor()
    obj.getDataRecent()

    noticeObj = elcsoft.model.smartdoor_notice.SmartdoorNotice()
    query = dict()
    query['table'] = "smartdoor_notice"
    query['where'] = "smartdoor_id='%s'" % obj.__pkValue__
    query['orderby'] = "smartdoor_notice_id desc"
    query['rows'] = 5
    #query['isEcho'] = True
    
    results = noticeObj.getResults(**query)

    array = list()
    for result in results:
        noticeObj = elcsoft.model.smartdoor_notice.SmartdoorNotice()
        noticeObj.setData(result)
        array.append(noticeObj.toDict())
    
    th = threading.Thread(target=createTTS, args=(array,))
    th.demon = True
    th.start()

    return array

#음성 녹음
def createTTS(array) :
    global global_config

    lib.log("createTTS start")

    if not lib.isSetupTTS(global_config) :
        lib.log("Notice TTS is not setup") 
        return False

    starts_with = "notice"

    text = ""
    file = global_config['tts']['path'] + starts_with
    for o in array :
        if text != "" :
            text = text + "\n\n"
        text = text + o['title']

        file = file + "_%s" % o['smartdoor_notice_id']
    text = text + "\n\n\n\n\n이상 공지사항이었습니다."

    file = file + ".wav"

    lib.log(text)
    lib.log(file)

    if text == "" :
        return True

    return tts.saveFile(file, text)
    
def joinProcess(**kwargs):
    global global_config
    
    url = 'https://api2.hizib.wikibox.kr/SmartdoorNotice'

    data = dict()

    if not 'user_id' in kwargs:
        raise Exception("회원정보를 입력해 주세요.")
    else :
        data['user_id'] = kwargs['user_id']
    
    if not 'title' in kwargs:
        raise Exception("공지글을 입력해 주세요.")
    else :
        data['title'] = kwargs['title']

    token = elcsoft.controller.smartdoor.getToken()

    #data['file'] = kwargs['file']
    obj = elcsoft.model.smartdoor_notice.SmartdoorNotice()
    obj.smartdoorObj.getDataRecent()

    if obj.smartdoorObj.__pkValue__ <= 0:
        raise Exception("스마트도어 정보가 없습니다.")
    else :
        obj.smartdoor_id = obj.smartdoorObj.__pkValue__

    result = lib.restapi(method="post", url=url, data=lib.jsonencode(data), token=token, isDebug=True)
    obj.fromDict(result)

    if not obj.save():
        raise Exception("공지사항 저장 실패! 원인 - %s" % obj.__errorMsg__)
    
    #tts 파일삭제
    lib.delete_files(global_config['tts']['path'], "notice", ".wav")

    return obj

def updateProcess(**kwargs):
    global global_config
    data = dict()

    if not 'smartdoor_notice_id' in kwargs:
        raise Exception("공지글 정보를 입력해 주세요.")
    else :
        data['smartdoor_notice_id'] = kwargs['smartdoor_notice_id']

    if 'user_id' in kwargs:
        data['user_id'] = kwargs['user_id']
    else :
        data['user_id'] = None
    
    if not 'title' in kwargs:
        raise Exception("공지글을 입력해 주세요.")
    else :
        data['title'] = kwargs['title']

    if data['user_id'] is None :
        del(data['user_id'])

    url = 'https://api2.hizib.wikibox.kr/SmartdoorNotice/%s' % data['smartdoor_notice_id']
    lib.log("/SmartdoorNotice/modifyProcess %s" % data)

    #data['file'] = kwargs['file']
    obj = elcsoft.model.smartdoor_notice.SmartdoorNotice()
    obj.getData(data['smartdoor_notice_id'])

    if obj.__pkValue__ <= 0:
        raise Exception("존재하지 않는 공지 정보입니다.")

    token = elcsoft.controller.smartdoor.getToken()

    result = lib.restapi(method="put", url=url, data=lib.jsonencode(data), token=token, isDebug=True)
    lib.log(result)
    obj.fromDict(result)

    if not obj.save():
        raise Exception("공지사항 저장 실패! 원인 - %s" % obj.__errorMsg__)
    
    #tts 파일삭제
    lib.delete_files(global_config['tts']['path'], "notice", ".wav")

    return obj

def deleteProcess(**kwargs):
    global global_config
    data = dict()

    if not 'smartdoor_notice_id' in kwargs:
        raise Exception("공지글 정보를 입력해 주세요.")
    else :
        data['smartdoor_notice_id'] = kwargs['smartdoor_notice_id']

    url = 'https://api2.hizib.wikibox.kr/SmartdoorNotice/%s' % data['smartdoor_notice_id']

    lib.log("/SmartdoorNotice/deleteProcess %s" % data)

    #data['file'] = kwargs['file']
    obj = elcsoft.model.smartdoor_notice.SmartdoorNotice()
    obj.getData(data['smartdoor_notice_id'])

    if obj.__pkValue__ <= 0:
        raise Exception("존재하지 않는 공지 정보입니다.")

    token = elcsoft.controller.smartdoor.getToken()

    result = lib.restapi(method="delete", url=url, token=token, isDebug=True)
    lib.log(result)

    if not obj.delete():
        raise Exception("공지사항 삭제 실패! 원인 - %s" % obj.__errorMsg__)
    
    #tts 파일삭제
    lib.delete_files(global_config['tts']['path'], "notice", ".wav")
    
    return True

# downloadProcess
def downloadProcess():
    token = elcsoft.controller.smartdoor.getToken()

    url = 'https://api2.hizib.wikibox.kr/SmartdoorNotice/lists'
    #result = lib.restapi(method="get", url=url, token=token, isDebug=True)
    result = lib.restapi(method="get", url=url, token=token)

    for data in result['lists'] :
        obj = elcsoft.model.smartdoor_notice.SmartdoorNotice()
        obj.fromDict(data)
        if not obj.save() :
            raise Exception("공지사항 정보를 저장하는데 실패하였습니다. 원인 - %s" % obj.__errorMsg__)

    return True
