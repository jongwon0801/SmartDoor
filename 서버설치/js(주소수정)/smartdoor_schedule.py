# ~/www/python/elcsoft/controller/smartdoor_schedule.py

import tts
import lib
import threading
import elcsoft.model.smartdoor_schedule
import elcsoft.controller.smartdoor

global_config = lib.getConfigByJsonFile('/home/pi/www/python/config.json')

# 일정가져오기
def getSchedules(startDate=None, stopDate=None) :
    global global_config

    lib.log("getSchedules startDate=%s stopDate=%s" % (startDate, stopDate))

    if startDate == None :
        startDate = lib.date('%Y-%m-%d', lib.get_first_day_of_current_month())

    if stopDate == None :
        stopDate = lib.date('%Y-%m-%d', lib.get_last_day_of_current_month())

    scheduelObj = elcsoft.model.smartdoor_schedule.SmartdoorSchedule()
    query = dict()
    query['table'] = "smartdoor_schedule"
    query['where'] = "'%s' <= dday and dday <= '%s'" % (startDate, stopDate)
    query['orderby'] = "dday"
    #query['isEcho'] = True

    results = scheduelObj.getResults(**query)

    array = list()
    for result in results:
        scheduelObj = elcsoft.model.smartdoor_schedule.SmartdoorSchedule()
        scheduelObj.setData(result)
        array.append(scheduelObj.toDict())
    
    th = threading.Thread(target=createTTS, args=(array,))
    th.demon = True
    th.start()

    return array

#음성 녹음
def createTTS(array=None) :
    global global_config

    lib.log("createTTS start")

    if not lib.isSetupTTS(global_config) :
        lib.log("Schedule TTS is not setup") 
        return False

    starts_with = "schedule"

    text = ""
    file = global_config['tts']['path'] + starts_with
    for o in array :
        if o['dday'] == lib.get_current_date('%Y-%m-%d 00:00:00') :
            if text != "" :
                text = text + ","

            text = text + o['name']
            file = file + "_%s" % o['smartdoor_schedule_id']

    if text == "" :
        return True
    
    text = "오늘은 \n\n\n\n\n" + text
    text = text + "\n\n\n\n\n일정이 있습니다."
    file = file + ".wav"

    lib.log(text)
    lib.log(file)

    return tts.saveFile(file, text)

def joinProcess(**kwargs):
    lib.log(kwargs)
    url = 'https://api2.hizib.wikibox.kr/SmartdoorSchedule'

    data = dict()
    
    if not 'name' in kwargs:
        raise Exception("일정명을 입력해 주세요!")
    else :
        data['name'] = kwargs['name']

    if not 'dday' in kwargs:
        raise Exception("날짜를 입력해 주세요.")
    else :
        data['dday'] = kwargs['dday']

    lib.log("/SmartdoorSchedule/joinProcess %s" % data)

    #data['file'] = kwargs['file']
    obj = elcsoft.model.smartdoor_schedule.SmartdoorSchedule()
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
        raise Exception("일정 등록 실패! 원인 - %s" % obj.__errorMsg__)
    
    #tts 파일삭제
    lib.delete_files(global_config['tts']['path'], "schedule", ".wav")

    return obj

def updateProcess(**kwargs):
    data = dict()

    if not 'smartdoor_schedule_id' in kwargs:
        raise Exception("일정 정보를 입력해 주세요.")
    else :
        data['smartdoor_schedule_id'] = kwargs['smartdoor_schedule_id']

    if not 'name' in kwargs:
        raise Exception("일정명을 입력해 주세요.")
    else :
        data['name'] = kwargs['name']

    if not 'dday' in kwargs:
        raise Exception("날짜를 입력해 주세요.")
    else :
        data['dday'] = kwargs['dday']

    url = 'https://api2.hizib.wikibox.kr/SmartdoorSchedule/%s' % data['smartdoor_schedule_id']
    lib.log("/SmartdoorSchedule/modifyProcess %s" % data)

    #data['file'] = kwargs['file']
    obj = elcsoft.model.smartdoor_schedule.SmartdoorSchedule()
    obj.getData(data['smartdoor_schedule_id'])

    if obj.__pkValue__ <= 0:
        raise Exception("존재하지 않는 일정 정보입니다.")

    token = elcsoft.controller.smartdoor.getToken()

    result = lib.restapi(method="put", url=url, data=lib.jsonencode(data), token=token, isDebug=True)
    lib.log(result)
    obj.fromDict(result)

    if not obj.save():
        raise Exception("일정 수정 실패! 원인 - %s" % obj.__errorMsg__)
    
    #tts 파일삭제
    lib.delete_files(global_config['tts']['path'], "schedule", ".wav")

    return obj

def deleteProcess(**kwargs):
    data = dict()

    if not 'smartdoor_schedule_id' in kwargs:
        raise Exception("일정 정보를 입력해 주세요.")
    else :
        data['smartdoor_schedule_id'] = kwargs['smartdoor_schedule_id']

    url = 'https://api2.hizib.wikibox.kr/SmartdoorSchedule/%s' % data['smartdoor_schedule_id']

    lib.log("/SmartdoorSchedule/deleteProcess %s" % data)

    #data['file'] = kwargs['file']
    obj = elcsoft.model.smartdoor_schedule.SmartdoorSchedule()
    obj.getData(data['smartdoor_schedule_id'])

    if obj.__pkValue__ <= 0:
        raise Exception("존재하지 않는 일정 정보입니다.")
        
    token = elcsoft.controller.smartdoor.getToken()

    result = lib.restapi(method="delete", url=url, data=lib.jsonencode(data), token=token, isDebug=True)
    lib.log(result)

    if not obj.delete():
        raise Exception("일정 삭제 실패! 원인 - %s" % obj.__errorMsg__)
    
    #tts 파일삭제
    lib.delete_files(global_config['tts']['path'], "schedule", ".wav")

    return True
    
# downloadProcess
def downloadProcess():
    token = elcsoft.controller.smartdoor.getToken()

    url = 'https://api2.hizib.wikibox.kr/SmartdoorSchedule/lists'
    #result = lib.restapi(method="get", url=url, token=token, isDebug=True)
    result = lib.restapi(method="get", url=url, token=token)

    for data in result['lists'] :
        obj = elcsoft.model.smartdoor_schedule.SmartdoorSchedule()
        obj.fromDict(data)
        
        if not obj.save() :
            raise Exception("일정 정보를 저장하는데 실패하였습니다. 원인 - %s" % obj.__errorMsg__)

    return True
