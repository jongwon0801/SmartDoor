# /home/pi/www/python/elcsoft/controller/ws/smartdoor_cmd.py

import os
import lib
import logger
import face
import qrread
import elcsoft.model.user
import elcsoft.controller.smartdoor
import elcsoft.controller.smartdoor_cmd
import elcsoft.controller.msg.exception
import elcsoft.controller.msg.smartdoor_cmd

'''
def doorOpenByQrProcess(self, **kwargs):
    logger.Logger._LOGGER.info(f"------------------------- doorOpenByQrProcess Start -------------------------")

    if not 'data' in kwargs or not 'smartdoor_guestkey_id' in kwargs['data'] :
        self.sendKioskAlert("QR코드로부터 게스트키 정보를 제대로 받지 못했습니다. 다시 시도해 주세요.")
        return False
    
    try :
        elcsoft.controller.smartdoor_cmd.doorOpenByQrProcess(int(kwargs['data']['smartdoor_guestkey_id']))
        self.sendKiosk('')
        elcsoft.controller.msg.smartdoor_cmd.qrScanStop(self)
    except Exception as e :
        logger.Logger._LOGGER.exception("QR 문열기 실패 : %s" % e)

    logger.Logger._LOGGER.info(f"------------------------- doorOpenByQrProcess Stop -------------------------")
    return True
'''
def doorOpenByKioskProcess(self, **kwargs):
    logger.Logger._LOGGER.info(f"------------------------- doorOpenByKioskProcess Start -------------------------")

    try :
        elcsoft.controller.smartdoor_cmd.doorOpenAtKioskProcess()
        self.sendKiosk('doorOpenedAtKiosk')
    except Exception as e :
        self.sendKioskAlert(str(e))

    logger.Logger._LOGGER.info(f"------------------------- doorOpenByKioskProcess Stop -------------------------")
    return True

def faceLoginProcess(self, **kwargs) :
    logger.Logger._LOGGER.info(f"------------------------- faceLoginProcess Start -------------------------")

    if self.doorStatus != 0 :
      return False
    
    logger.Logger._LOGGER.info(f"------------------------- faceLoginProcess kwargs -------------------------")
    print(kwargs)
    logger.Logger._LOGGER.info(f"------------------------- faceLoginProcess kwargs -------------------------")
    
    try:
        lib.delete_files(self.config['face']['picture'], "picture")        
        file_path = lib.saveFile(kwargs['data']['file'], self.config['face']['picture'], 'picture')
        logger.Logger._LOGGER.info("picture image : %s" % file_path)
    except Exception as e:
        elcsoft.controller.msg.exception.websocket(self, str(e))
        return False
    
    if os.path.exists(file_path):
        file_url = file_path.replace('/home/pi/www', '')

        try:
            obj = face.Face()
            result = obj.searchByFile(file_path)
            logger.Logger._LOGGER.info("face login process result : %s" % result)

            obj = elcsoft.model.user.User()
            if len(result) :
                obj.getDataByCondition("user_id='%s'" % result[0])

            data = dict()
            lib.delete_files(self.config['face']['picture'], "picture")

            if obj.__pkValue__ :
                elcsoft.controller.msg.smartdoor_cmd.faceLogined(self, obj.__pkValue__, file_url)
            else :
                elcsoft.controller.msg.smartdoor_cmd.faceLoginFail(self, file_url)
        except Exception as e:
            elcsoft.controller.msg.smartdoor_cmd.faceLoginFail(self, file_url)
    else :
        elcsoft.controller.msg.smartdoor_cmd.loginFacePictureNotFound(self)

    logger.Logger._LOGGER.info(f"------------------------- faceLoginProcess Stop -------------------------")
    return True

def faceLoginByDataProcess(self, **kwargs) :
    logger.Logger._LOGGER.info(f"------------------------- faceLoginByDataProcess Start -------------------------")

    if not 'isDoorOpen' in self.config['faceLogin'] :
        self.config['faceLogin']['isDoorOpen'] = False

    if not 'isLogPicture' in self.config['faceLogin'] :
        self.config['faceLogin']['isLogPicture'] = False

    if not self.config['faceLogin']['isDoorOpen'] and self.doorlo.doorStatus != 0 :
        lib.log('문이 열려있어 얼굴로그인 사용 못함')
        return False

    try :
        if self.config['faceLogin']['isLogPicture'] :
            timestamp = lib.date('%Y%m%d%H%M%S')
            filename = f'picture{timestamp}'
            lib.log(f'faceLogin picture filename : {filename}')
            lib.saveFile(kwargs['data']['file'], self.config['face']['picture'], filename)
        
        obj = face.Face()
        result = obj.searchByBase64(kwargs['data']['file'].split(';base64,')[1])
        logger.Logger._LOGGER.info("-------------------------------- faceLoginByDataProcess searchByBase64 --------------------------------")
        lib.log(type(result))
        lib.log(result)
        logger.Logger._LOGGER.info("face login process result : %s" % result)
        logger.Logger._LOGGER.info("-------------------------------- faceLoginByDataProcess searchByBase64 --------------------------------")

        obj = elcsoft.model.user.User()
        if len(result) :
            obj.getDataByCondition("user_id='%s'" % result[0])

        if obj.__pkValue__ :
            print(f'user_id : %s' % obj.__pkValue__)
            elcsoft.controller.msg.smartdoor_cmd.faceLogined(self, obj.__pkValue__, kwargs['data']['file'])
        else :
            elcsoft.controller.msg.smartdoor_cmd.faceLoginFail(self, kwargs['data']['file'])
    except Exception as e:
        lib.log(e)
        elcsoft.controller.msg.smartdoor_cmd.loginFacePictureNotFound(self)

    logger.Logger._LOGGER.info(f"------------------------- faceLoginByDataProcess Stop -------------------------")
    return True
'''
def faceDoorOpenProcess(self, **kwargs):
    logger.Logger._LOGGER.info(f"------------------------- faceDoorOpenProcess Start -------------------------")

    #logger.Logger._LOGGER.info(kwargs)
    if self.doorStatus != 0 :
        return False
    
    try:
        lib.delete_files(self.config['face']['picture'], "login")

        file_path = lib.saveFile(kwargs['data']['file'], self.config['face']['picture'], 'login')
        logger.Logger._LOGGER.info("login image : %s" % file_path)
    except Exception as e:
        elcsoft.controller.msg.exception.websocket(self, str(e))
        return False

    if os.path.exists(file_path):
        file_url = file_path.replace('/home/pi/www', '')

        try:
            #qrcode = qrimg.readQr(file_path)
            #logger.Logger._LOGGER.info("login qrcode : %s" % qrcode)
            #logger.Logger._LOGGER.info("페이스 시작")

            obj = face.Face()
            result = obj.searchByFile(file_path)
            logger.Logger._LOGGER.info("face door open process result : %s" % result)

            obj = elcsoft.model.user.User()
            if len(result) :
                obj.getDataByCondition("user_id='%s'" % result[0])

            if obj.__pkValue__ :
                elcsoft.controller.smartdoor_cmd.doorOpenByFaceProcess(user_id=obj.__pkValue__)
                elcsoft.controller.msg.smartdoor_cmd.faceDoorOpened(self, obj.__pkValue__, file_url)
            else :
                elcsoft.controller.msg.smartdoor_cmd.faceDoorOpenFail(self, file_url)

            data = dict()
            lib.delete_files(self.config['face']['picture'], "login")
        except Exception as e:
            elcsoft.controller.msg.smartdoor_cmd.faceDoorOpenFail(self, file_url)
    else :
        elcsoft.controller.msg.smartdoor_cmd.dooropenFacePictureNotFound(self)

    logger.Logger._LOGGER.info(f"------------------------- faceDoorOpenProcess Stop -------------------------")
    return True

def faceDoorOpenByDataProcess(self, **kwargs):
    logger.Logger._LOGGER.info(f"------------------------- faceDoorOpenByDataProcess Start -------------------------")

    if self.doorStatus != 0 :
        return None
    
    try:
        #qrcode = qrimg.readQr(file_path)
        #logger.Logger._LOGGER.info("login qrcode : %s" % qrcode)
        #logger.Logger._LOGGER.info("페이스 시작")

        obj = face.Face()
        result = obj.searchByBase64(kwargs['data']['file'].split(';base64,')[1])
        logger.Logger._LOGGER.info("face login process result : %s" % result)

        obj = elcsoft.model.user.User()
        if len(result) :
            obj.getDataByCondition("user_id='%s'" % result[0])

        if obj.__pkValue__ :
            elcsoft.controller.smartdoor_cmd.doorOpenByFaceProcess(user_id=obj.__pkValue__)
            elcsoft.controller.msg.smartdoor_cmd.faceDoorOpened(self, obj.__pkValue__, kwargs['data']['file'])
        else :
            elcsoft.controller.msg.smartdoor_cmd.faceDoorOpenFail(self, kwargs['data']['file'])
    except Exception as e:
        logger.Logger._LOGGER.exception(e)
        elcsoft.controller.msg.smartdoor_cmd.doorOpenFacePictureNotFound(self)

    logger.Logger._LOGGER.info(f"------------------------- faceDoorOpenByDataProcess Stop -------------------------")
    return True
'''

def doorOpenByPicture(self, **kwargs):
    logger.Logger._LOGGER.info(f"------------------------- doorOpenByPicture Start -------------------------")
    #lib.log(kwargs)
    #lib.log(kwargs['data'])
    #lib.log(kwargs['data']['file'])
    if self.doorStatus != 0 :
        logger.Logger._LOGGER.info(f"문이 열린 상태에서는 작동하지 않음")
        return False
    
    try:
        result = lib.jsondecode(qrread.readQrcodeByBase64(kwargs['data']['file'].split(';base64,')[1]))
        lib.log("-------------------------------- readQrcodeByBase64 --------------------------------")
        lib.log(type(result))
        lib.log(result)
        lib.log("-------------------------------- readQrcodeByBase64 --------------------------------")
        elcsoft.controller.smartdoor_cmd.doorOpenByQrProcess(self, result['data']['smartdoor_guestkey_id'])
        elcsoft.controller.msg.smartdoor_cmd.qrDoorOpened(self, kwargs['data']['file'])
        return True
    except Exception as e:
        lib.log(f'QRCode read failed : {e}')

    try :
        #timestamp = lib.now().strftime('%Y%m%d%H%M%S')
        #filename = f'picture{timestamp}'
        #lib.saveFile(kwargs['data']['file'], self.config['face']['picture'], filename)

        obj = face.Face()
        result = obj.searchByBase64(kwargs['data']['file'].split(';base64,')[1])
        lib.log("-------------------------------- doorOpenByPicture searchByBase64 --------------------------------")
        lib.log(type(result))
        lib.log(result)
        logger.Logger._LOGGER.info("face login process result : %s" % result)
        lib.log("-------------------------------- doorOpenByPicture searchByBase64 --------------------------------")

        obj = elcsoft.model.user.User()
        if len(result) :
            obj.getDataByCondition("user_id='%s'" % result[0])

        if obj.__pkValue__ :
            elcsoft.controller.smartdoor_cmd.doorOpenByFaceProcess(self, user_id=obj.__pkValue__)
            elcsoft.controller.msg.smartdoor_cmd.faceDoorOpened(self, obj.__pkValue__, kwargs['data']['file'])
        else :
            elcsoft.controller.msg.smartdoor_cmd.faceDoorOpenFail(self, kwargs['data']['file'])
    except Exception as e:
        elcsoft.controller.msg.smartdoor_cmd.faceDoorOpenFail(self, kwargs['data']['file'])
    
    logger.Logger._LOGGER.info(f"------------------------- doorOpenByPicture Stop -------------------------")
