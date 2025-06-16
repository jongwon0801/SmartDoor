# ~/www/python/elcsoft/controller/smartdoor_vod.py

import lib
import asyncio
import os
import datetime
import base64

import elcsoft.model.smartdoor
import elcsoft.model.smartdoor_vod
import elcsoft.controller.smartdoor

#등록
def joinProcess(**kwargs):
    smartdoor_id = kwargs.get('smartdoor_id', None)
    gcode = kwargs.get('gcode', None)
    code = kwargs.get('code', None)
    filepath = kwargs.get('filepath', None)
    fileurl = kwargs.get('fileurl', None)
    filename = kwargs.get('filename', None)

    #data['file'] = kwargs['file']
    obj = elcsoft.model.smartdoor_vod.SmartdoorVod()

    if smartdoor_id is None:
        obj.smartdoorObj.getDataRecent()
        smartdoor_id = obj.smartdoorObj.__pkValue__

    if gcode is None:
        raise Exception("녹화 일자 정보가 없습니다.")
    
    if code is None:
        raise Exception("녹화 시간 정보가 없습니다.")
    
    if filepath is None:
        raise Exception("파일 저장 위치 정보가 없습니다.")
    
    if fileurl is None:
        fileurl = filepath.replace("/home/pi/www", "")
    
    if filename is None:
        filename = "%s.mp4"
    
    if smartdoor_id <= 0:
        raise Exception("스마트도어 정보가 없습니다.")

    url = 'https://api2.hizib.wikibox.kr/SmartdoorVod'

    data = dict()
    data['smartdoor_id'] = obj.smartdoorObj.__pkValue__
    data['gcode'] = gcode
    data['code'] = code.replace('.mp4', '')
    data['filepath'] = filepath
    data['fileurl'] = fileurl
    data['filename'] = filename

    token = elcsoft.controller.smartdoor.getToken()

    result = lib.restapi(method="post", url=url, data=lib.jsonencode(data), token=token, isDebug=True)

    obj = elcsoft.model.smartdoor_vod.SmartdoorVod()
    obj.setData(result)

    if not obj.save() :
        raise Exception("녹화영상 정보 저장 실패. 원인 - %s" % obj.__errorMsg__)

    return obj


#서버에 데이터 동기화
def syncProcess(**kwargs):
    smartdoor_id = kwargs.get('smartdoor_id', None)
    gcode = kwargs.get('gcode', None)
    code = kwargs.get('code', None)
    filepath = kwargs.get('filepath', None)
    fileurl = kwargs.get('fileurl', None)
    filename = kwargs.get('filename', None)

    #data['file'] = kwargs['file']
    obj = elcsoft.model.smartdoor_vod.SmartdoorVod()

    if smartdoor_id is None:
        obj.smartdoorObj.getDataRecent()
        smartdoor_id = obj.smartdoorObj.__pkValue__

    if gcode is None:
        raise Exception("녹화 일자 정보가 없습니다.")
    
    if code is None:
        raise Exception("녹화 시간 정보가 없습니다.")
    
    if filepath is None:
        raise Exception("파일 저장 위치 정보가 없습니다.")
    
    if fileurl is None:
        fileurl = filepath.replace("/home/pi/www", "")
    
    if filename is None:
        filename = "%s.mp4" % code
    
    if smartdoor_id <= 0:
        raise Exception("스마트도어 정보가 없습니다.")
    
    code = code.replace('.mp4', '')

    obj.getDataByCondition("smartdoor_id='%s' AND gcode='%s' AND code='%s'" % (smartdoor_id, gcode, code))

    if obj.__pkValue__ <= 0 :
        obj = joinProcess(smartdoor_id=smartdoor_id, gcode=gcode, code=code, filepath=filepath, fileurl=fileurl, filename=filename)

    return obj


# vodUploadProcess
def vodUploadProcess(**kwargs):
    lib.log("/SmartdoorVod/vodUploadProcess %s" % kwargs)

    if not 'smartdoor_vod_id' in kwargs :
        raise Exception("녹화영상 정보가 없습니다.")

    obj = elcsoft.model.smartdoor_vod.SmartdoorVod()
    obj.getData(kwargs['smartdoor_vod_id'])

    if obj.__pkValue__ <= 0 :
        raise Exception("존재하지 않는 영상정보입니다.")

    filepath = "/home/pi/www/vod/%s/%s.mp4" % (obj.gcode, obj.code)
    lib.log("filepath : %s[존재 : %s]" % (filepath, os.path.isfile(filepath)))

    token = elcsoft.controller.smartdoor.getToken()

    if not os.path.isfile(filepath):
        url = 'https://api2.hizib.wikibox.kr/SmartdoorVod/%s' % obj.__pkValue__
        result = lib.restapi(method="delete", url=url, token=token)
        lib.log(result)
        raise Exception("삭제된 영상입니다.")

    url = 'https://api2.hizib.wikibox.kr/SmartdoorVod/vodUpload'
    lib.log("%s : %s" % (url, filepath))

    with open(filepath, 'rb') as file:
        files = {'file': file}
        result = lib.restapi(method="file", url=url, data={'smartdoor_vod_id':obj.__pkValue__}, files=files, token=token, isDebug=True)
    
    return True

# vodDeleteProcess
def vodDeleteProcess(**kwargs):
    lib.log("/SmartdoorVod/vodDeleteProcess %s" % kwargs)

    if not 'smartdoor_vod_id' in kwargs :
        raise Exception("녹화영상 정보가 없습니다.")

    obj = elcsoft.model.smartdoor_vod.SmartdoorVod()
    obj.getData(kwargs['smartdoor_vod_id'])

    if obj.__pkValue__ <= 0 :
        raise Exception("존재하지 않는 영상정보입니다.")

    url = 'https://api2.hizib.wikibox.kr/SmartdoorVod/vodDeleteProcess'

    token = elcsoft.controller.smartdoor.getToken()

    result = lib.restapi(method="post", url=url, data={'smartdoor_vod_id': obj.__pkValue__}, token=token)
    lib.log(result)

    return True

# 동영상 업로드
def saveVod(file) :
    return joinProcess(file=file)

# syncSmartdoorVods
def syncSmartdoorVods() :
    obj = elcsoft.model.smartdoor.Smartdoor()
    obj.getDataRecent()

    if obj.__pkValue__ <= 0:
        raise Exception("스마트도어 정보가 없습니다.")
    
    token = elcsoft.controller.smartdoor.getToken()
    
    path = "/home/pi/www/vod"
    files = []
    array = []
    # 디렉토리가 존재하는지 확인
    if os.path.exists(path):
        tops = sorted(os.listdir(path), key=lambda x: int(x))  # 숫자 오름차순 정렬
        for top in tops:
            print(f'folder : {top}')
            subs = sorted(os.listdir(os.path.join(path, top)), key=lambda x: int(x.replace('.mp4', '')))  # 숫자 오름차순 정렬
            for sub in subs:
                print(f'file : {sub}')
                file = os.path.join(path, top, sub)
                if os.path.isfile(file):
                    files.append(file)
                    gcode = top
                    code = sub.replace('.mp4', '')
                    print(f'gcode : {gcode} code : {code} filepath : {file}')
                    o = syncProcess(smartdoor_id=obj.__pkValue__, gcode=top, code=code, filepath=file)
                    array.append(o.__pkValue__)
    
    url = 'https://api2.hizib.wikibox.kr/SmartdoorVod/deleteNotUsed'
    
    data = dict()
    data['smartdoor_id'] = obj.__pkValue__
    data['smartdoor_vod_id'] = array

    result = lib.restapi(method="post", url=url, data=lib.jsonencode(data), token=token)

    condition = "smartdoor_id='%s'" % obj.__pkValue__
    for smartdoor_vod_id in array :
        condition = condition + " AND smartdoor_vod_id!='%s'" % smartdoor_vod_id

    lib.log(data)

    obj = elcsoft.model.smartdoor_vod.SmartdoorVod()
    if not obj.deleteByCondition(condition) :
        raise Exception("사용하지 않는 영상 정보를 삭제하는데 실패하였습니다.")
    
    return True

#비동기함수
async def asyncSyncSmartdoorVods():
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, syncSmartdoorVods)
