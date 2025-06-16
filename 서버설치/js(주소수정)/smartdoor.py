# ~/www/python/elcsoft/controller/smartdoor.py

import lib
import time
import json
import os
import fcm
import shutil
import subprocess
import qrimg
import msgbox
import weather

import elcsoft.model.smartdoor_cmd
import elcsoft.model.user
import elcsoft.model.smartdoor
import elcsoft.model.smartdoor_user
import elcsoft.model.smartdoor_notice
import elcsoft.model.smartdoor_schedule
import elcsoft.model.smartdoor_message
import elcsoft.model.smartdoor_item
import elcsoft.model.smartdoor_guestkey
import elcsoft.model.smartdoor_vod

smartdoorObj = elcsoft.model.smartdoor.Smartdoor()

#스마트도어 정보 가져오기
def getSmartdoorObj() :
    global smartdoorObj
    if smartdoorObj.__pkValue__ <= 0 :
        smartdoorObj.getDataRecent()
    return smartdoorObj

#스마트도어 정보 가져오기
def getSmartdoorInfo() :
    global smartdoorObj
    if smartdoorObj.__pkValue__ <= 0 :
        smartdoorObj.getDataRecent()
    return smartdoorObj.toDict()

#기기 등록 여부
def isJoin() :
    global smartdoorObj

    if smartdoorObj.__pkValue__ <= 0 :
        smartdoorObj.getDataRecent()

    if smartdoorObj.__pkValue__ :
        return True
    else :
        return False
    
#도어락 등록여부
def isDoorlock() :
    #hione locker의 경우 true처리
    return True

    
    obj.getDataRecent()

    if lib.check_blank(obj.ble) :
        return False

#오너 등록여부
def isOwner() :
    #로컬DB에서 확인 하는 것으로 변경
    url = 'https://api2.hizib.wikibox.kr/Smartdoor/owner'

    token = getToken()

    result = lib.restapi(method="get", url=url, token=token, isDebug=True)
    return int(result['smartdoor_user_id']) > 0 and int(result['isUse']) == 1

#smartdoor token가져오기
def getToken(**kwargs) :
    global smartdoorObj

    if smartdoorObj.__pkValue__ <= 0 :
        smartdoorObj.getDataRecent()

    if smartdoorObj.__pkValue__ <= 0 :
        raise Exception("스마트도어 정보가 없습니다.")
    
    path = '/home/pi/www/python/token.json'

    #print(path)
    # 파일이 존재하는지 확인
    if os.path.exists(path):
        config = lib.getConfigByJsonFile(path)
    else:
        config = {}

    #print(config['token'])
    isReresh = False

    global_config = lib.getConfigByJsonFile('/home/pi/www/python/config.json')

    if 'token' in config and config['token'] != '':
        token = config['token'].strip()

        import jwt

        try :
            payload = jwt.decode(token, global_config['accessKey'], algorithms=["HS512"])
            if smartdoorObj.__pkValue__ != int(payload['smartdoor_id']) :
                isReresh = True
            elif  int(time.time()) >= int(payload['exp']) :
                isReresh = True
        except :
            token = ""
            isReresh = True
            #재발급
    else :
        isReresh = True

    if isReresh :
        if not 'smartdoor_id' in kwargs :
            kwargs['smartdoor_id'] = smartdoorObj.__pkValue__

        if kwargs['smartdoor_id'] <= 0 :
            raise Exception("스마트도어 정보가 없어 토큰 발행을 할 수 없습니다.")

        url = 'https://api2.hizib.wikibox.kr/Smartdoor/token?smartdoor_id=%s' % kwargs['smartdoor_id']

        try :
            result = lib.restapi(method="get", url=url)
            #print(result)
            token = result['token']
            #print(token)

            config['token'] = token
            with open(path, "w") as fp:
                json.dump(config, fp)
        except :
            token = ""
    return token

#owner topic
def getOwnerTopic() :
    global smartdoorObj

    if smartdoorObj.__pkValue__ <= 0 :
        smartdoorObj.getDataRecent()

    if smartdoorObj.__pkValue__ <= 0 :
        raise Exception("스마트도어 정보가 없습니다.")

    smartdoorUserObj = elcsoft.model.smartdoor_user.SmartdoorUser()
    smartdoorUserObj.getDataByCondition("smartdoor_id='%s' AND isOwner=1" % smartdoorObj.__pkValue__)

    if smartdoorUserObj.__pkValue__ <= 0 :
        raise Exception("스마트오너 정보가 없습니다.")

    return 'hizib01/%s/user/%s' % (smartdoorObj.code, smartdoorUserObj.user_id)

def getUserTopic(user_id) :
    global smartdoorObj

    if smartdoorObj.__pkValue__ <= 0 :
        smartdoorObj.getDataRecent()

    if smartdoorObj.__pkValue__ <= 0 :
        raise Exception("스마트도어 정보가 없습니다.")

    return 'hizib01/%s/user/%s' % (smartdoorObj.code, user_id)

# door topic
def getDoorTopic():
    global smartdoorObj

    if smartdoorObj.__pkValue__ <= 0 :
        smartdoorObj.getDataRecent()

    if smartdoorObj.__pkValue__ <= 0:
        raise Exception("스마트도어 정보가 없습니다.")

    return 'hizib01/%s/door' % smartdoorObj.code

# get ble
def getBle() :
    global smartdoorObj

    if smartdoorObj.__pkValue__ <= 0 :
        smartdoorObj.getDataRecent()

    if smartdoorObj.__pkValue__ <= 0:
        raise Exception("스마트도어 정보가 없습니다.")

    return smartdoorObj.ble

#ble App 등록
def bleAppJoinProcess() :
    global smartdoorObj

    if smartdoorObj.__pkValue__ <= 0 :
        smartdoorObj.getDataRecent()

    if smartdoorObj.__pkValue__ <= 0 :
        raise Exception("스마트도어 정보가 없어 BLE설정에 실패하였습니다.")

    out = subprocess.run(['python', '/home/pi/www/python/solity_cmd.py', 'auth'], capture_output=True)
    result = lib.jsondecode(out.stdout.decode('utf-8'))
    #print(result)

    if not result['result'] :
        raise Exception(result['message'])

    return True

# ble정보 설정
def setBle(address) :
    global smartdoorObj

    if smartdoorObj.__pkValue__ <= 0 :
        smartdoorObj.getDataRecent()

    if smartdoorObj.__pkValue__ <= 0 :
        raise Exception("스마트도어 정보가 없어 BLE설정에 실패하였습니다.")

    if address == None :
        raise Exception("BLE Address 정보가 없습니다.")

    if smartdoorObj.__pkValue__ <= 0 :
        raise Exception("스마트도어 등록 후 이용해 주세요.")

    if smartdoorObj.ble != address :
        smartdoorObj.ble = address

        url = "https://api2.hizib.wikibox.kr/Smartdoor"
        data = {"ble": address}
        token = getToken()
        results = lib.restapi(method="put", url=url, data=lib.jsonencode(data), token=token)

        if not smartdoorObj.save() :
            raise Exception(smartdoorObj.__errorMsg__)

    return True

#기기 등록
def joinProcess(code) :
    if code == None or code == "":
        raise Exception("제품 Serial Number를 입력해 주세요.")

    url = 'https://api2.hizib.wikibox.kr/Smartdoor/findByCode?code=%s' % code

    results = lib.restapi(method="get", url=url)

    if not 'result' in  results :
        obj = elcsoft.model.smartdoor.Smartdoor()
        obj.fromDict(results)

        obj.smartdoorGroupObj.fromDict(results['smartdoorGroupObj'])
        if not obj.smartdoorGroupObj.save() :
            raise Exception("단지 정보를 저장하는데 실패하였습니다.")

        if not obj.save() :
            raise Exception("도어락 정보를 저장하는데 실패하였습니다.")
        
        return qrimg.saveImage()
    else :
        raise Exception(results['message'])
    
# 서버 데이터베이스 동기화
def syncProcess() :
    global smartdoorObj

    if smartdoorObj.__pkValue__ <= 0 :
        smartdoorObj.getDataRecent()

    if smartdoorObj.__pkValue__ <= 0 :
        raise Exception("스마트도어 정보가 없어 데이터 동기화에 실패하였습니다.")

    token = getToken()
    if token != "" :
        downloadProcess(token=token)

        import elcsoft.controller.smartdoor_user
        import elcsoft.controller.smartdoor_notice
        import elcsoft.controller.smartdoor_schedule
        import elcsoft.controller.smartdoor_item
        import elcsoft.controller.smartdoor_message
        import elcsoft.controller.smartdoor_vod

        elcsoft.controller.smartdoor_user.downloadProcess()
        elcsoft.controller.smartdoor_notice.downloadProcess()
        elcsoft.controller.smartdoor_schedule.downloadProcess()
        elcsoft.controller.smartdoor_item.downloadProcess()
        elcsoft.controller.smartdoor_message.downloadProcess()
        elcsoft.controller.smartdoor_vod.syncSmartdoorVods()
        elcsoft.controller.smartdoor_user.trainProcess()
    return True

#외부모션 감지
def motionDetectProcess() :
    sendFcm("WIKI Smartdoor 알림", "외부인이 감지되었습니다. 지금 확인하시겠습니까?", "motionDetect", "isMotionDetect")

#도어벨 눌림
def doorbellPushProcess() :
    sendFcm("WIKI Smartdoor 알림", "도어벨이 울렸습니다. 지금 확인하시겠습니까?", "doorbellPush", "isDoorbell")

#send fcm
def sendFcm(title, body, click_action, option="") :
    global smartdoorObj

    if smartdoorObj.__pkValue__ <= 0 :
        smartdoorObj.getDataRecent()

    if smartdoorObj.__pkValue__ <= 0 :
        raise Exception("스마트도어 정보가 없어 FCM메세지 발송에 실패하였습니다.")

    data = dict()
    data['title'] = title
    data['body'] = body
    if click_action != "":
        data['click_action'] = click_action

    import elcsoft.components

    listObj = elcsoft.components.Components()
    listObj.setJoin("SmartdoorUser", "a", "a.smartdoor_id='%s'" % smartdoorObj.__pkValue__)
    listObj.setJoin("User", "b", "b.user_id=a.user_id")

    if option != "" :
        listObj.setAndCondition("a.%s=1" % option)

    listObj.setSort("a.isOwner", "desc")
    results = listObj.getOnlyResult()

    tokens = list()
    for result in results :
        #print(result)
        #fcm.send(token=result['b_fcm_token'], title=title, body=body, data=data)
        if result['b_fcm_token'] != "":
            tokens.append(result['b_fcm_token'])
    #print(tokens)
    #token = ','.join(tokens)
    #print("token : %s" % token)
    if len(tokens) :
        response = fcm.sends(tokens=tokens, title=title, body=body, data=data)
        #print(response)
        results = dict()
        results['total'] = len(tokens)
        results['success'] = response
        results['failure'] = len(tokens) - response
        return results
    else :
        raise Exception("PUSH메세지를 발송할 대상이 없습니다.")

# 모든 사용자에게 mqtt보내기
def sendMqtt(mqtt=None, message=""):
    import elcsoft.controller.user
    users = elcsoft.controller.user.getUsers()
    for user in users['lists'] :
        #print(user)
        topic = getUserTopic(user['user_id'])
        #print(topic)
        if mqtt :
            mqtt.publish(getUserTopic(user['user_id']), message)
        else :
            msgbox.sendMsg(cmd="mqtt", topic=getUserTopic(user['user_id']), msg=message)

    return True

# 초기화하는 메소드
def initProcess() :
    global smartdoorObj

    if smartdoorObj.__pkValue__ <= 0 :
        smartdoorObj.getDataRecent()

    if smartdoorObj.__pkValue__ <= 0 :
        raise Exception("스마트도어 정보가 없어 초기화하는데 실패하였습니다.")
    
    global_config = lib.getConfigByJsonFile('/home/pi/www/python/config.json')

    try :
        smartdoorObj.__lib__['conn'].query("drop database hizib")
        print("데이터베이스 삭제 완료")
    except Exception as e:
        print(e)

    try :
        smartdoorObj.__lib__['conn'].query("create database hizib")
        print("데이터베이스 생성 완료")
    except Exception as e:
        print(e)

    try :
        o = qrimg.deleteQr()
    except Exception as e:
        print(e)

    try :
        #파일이 있는지 검사
        if os.path.exists(global_config['face']['dataset']) :
            os.remove(global_config['face']['dataset'])
    except Exception as e:
        print(e)

    try :
        # 삭제할 경로
        directory = '/home/pi/www/vod'

        # 디렉토리가 존재하는지 확인
        if os.path.exists(directory):
            # 디렉토리의 모든 내용 삭제
            shutil.rmtree(directory)
            # 빈 디렉토리 생성 (원하는 경우)
            os.makedirs(directory)
    except Exception as e:
        print(e)

    try :
        # 삭제할 경로
        directory = '/home/pi/www/image/user'

        # 디렉토리가 존재하는지 확인
        if os.path.exists(directory):
            # 디렉토리의 모든 내용 삭제
            shutil.rmtree(directory)
            # 빈 디렉토리 생성 (원하는 경우)
            os.makedirs(directory)
    except Exception as e:
        print(e)

    try :
        msgbox.refresh()
    except Exception as e:
        print(e)

    return True

# downloadProcess
def downloadProcess(**kwargs):
    global smartdoorObj

    if smartdoorObj.__pkValue__ <= 0 :
        smartdoorObj.getDataRecent()

    if smartdoorObj.__pkValue__ <= 0 :
        raise Exception("등록된 스마트도어 정보가 없습니다.")

    pkValue = kwargs.get('smartdoor_id', smartdoorObj.__pkValue__)
 
    if pkValue <= 0:
        raise Exception("스마트도어 제품 정보가 없습니다.")

    url = 'https://api2.hizib.wikibox.kr/Smartdoor/%s' % pkValue
    data = lib.restapi(method="get", url=url, token=getToken())
    #print(data)

    smartdoorObj.fromDict(data)

    if 'smartdoorGroupObj' in data :
        smartdoorObj.smartdoorGroupObj.fromDict(data['smartdoorGroupObj'])

        if not smartdoorObj.smartdoorGroupObj.save():
            raise Exception("스마트도어 단지 정보를 저장하는데 실패하였습니다. 원인 - %s" % smartdoorObj.smartdoorGroupObj.__errorMsg__)
    else :
        import elcsoft.controller.smartdoor_group
        smartdoorObj.smartdoorGroupObj = elcsoft.controller.smartdoor_group.downloadProcess(smartdoor_group_id=data['smartdoor_group_id'], token=kwargs['token'])
        smartdoorObj.smartdoor_group_id = smartdoorObj.smartdoorGroupObj.__pkValue__

    if not smartdoorObj.save():
        raise Exception("스마트도어 정보를 저장하는데 실패하였습니다. 원인 - %s" % smartdoorObj.__errorMsg__)

    return smartdoorObj

# refresh
def refresh(**kwargs):
    try :
        msgbox.refresh()
        return True
    except Exception as e :
        return False
    
# vodUploadProcess
def vodUploadProcess(**kwargs):
    global smartdoorObj

    if smartdoorObj.__pkValue__ <= 0 :
        smartdoorObj.getDataRecent()

    if smartdoorObj.__pkValue__ <= 0 :
        raise Exception("스마트도어 정보가 없어 녹화영상 정보 가져오는데 실패하였습니다.")

    if not 'token' in kwargs :
        kwargs['token'] = smartdoorObj.getToken()

    if not 'file' in kwargs :
        raise Exception("업로드할 파일이 없습니다.")
    
    gcode = lib.date('%Y%m%d')
    code = lib.date('%H%M')

    obj = elcsoft.model.smartdoor_vod.SmartdoorVod()
    
    kwargs['smartdoor_id'] = self.__pkValue__
    kwargs['gcode'] = gcode
    kwargs['code'] = code

    if not obj.vodUploadProcess(**kwargs) :
        raise Exception(obj.__errorMsg__)

    return True

def weatherUpdate() :
    global smartdoorObj

    if smartdoorObj.__pkValue__ <= 0 :
        smartdoorObj.getDataRecent()

    if smartdoorObj.__pkValue__ <= 0 :
        raise Exception("스마트도어 정보가 없어 날씨 정보 가져오는데 실패하였습니다.")
    
    if smartdoorObj.smartdoorGroupObj.__pkValue__ <= 0 :
        smartdoorObj.smartdoorGroupObj.getData(smartdoorObj.smartdoor_group_id)
    
    lib.log(f'areacode : {smartdoorObj.smartdoorGroupObj.areacode}')
    return weather.search(smartdoorObj.smartdoorGroupObj.areacode)
