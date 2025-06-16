# /www/kiosk/python/elcsoft/controller/user.py

import lib
import os
import face

import elcsoft.model.smartdoor
import elcsoft.model.smartdoor_user
import elcsoft.model.user

import elcsoft.controller.smartdoor

# 사용자를 가져오기
def getUsers() :
    obj = elcsoft.model.smartdoor.Smartdoor()
    obj.getDataRecent()

    smartdoorUserObj = elcsoft.model.smartdoor_user.SmartdoorUser()
    #smartdoorUserObj.downloadProcess(token=obj.getToken())

    return smartdoorUserObj.lists()

# 사용자를 가져오기
def getUser(user_id) :
    obj = elcsoft.model.user.User()
    obj.getData(user_id)

    return obj

# user의 페이스 이미지만 업데이트
def faceUpdateProcess(pkValue) :
    if not downloadProcess(user_id=pkValue) :
        raise Exception("회원 정보를 가져오는데 실패하였습니다.")
    
    userObj = elcsoft.model.user.User()
    userObj.getData(pkValue)

    lib.log(userObj.faces['1'])
    #lib.rotate_image_based_on_exif(userObj.faces[0].path)

    obj = face.Face()
    obj.train()

    return True

# user의 페이스 이미지 삭제
def faceDeleteProcess(pkValue) :
    if not faceImageDelete(user_id=pkValue) :
        raise Exception("얼굴 이미지를 삭제하는데 실패하였습니다.")

    obj = face.Face()
    obj.train()

    return True

# downloadProcess
def downloadProcess(**kwargs):
    token = elcsoft.controller.smartdoor.getToken()

    if not 'user_id' in kwargs :
        raise Exception("회원 정보가 없습니다.")

    url = 'https://api2.hizib.wikibox.kr/User/%s' % kwargs['user_id']
    result = lib.restapi(method="get", url=url, token=token)

    #print(result)
    obj = elcsoft.model.user.User()
    obj.fromDict(result)

    if not obj.save():
        return False

    pictureDownloadProcess(user_id=kwargs['user_id'])
    facesDownloadProcess(user_id=kwargs['user_id'])

    return True

#pictureDownloadProcess
def pictureDownloadProcess(**kwargs) :
    if not 'user_id' in kwargs :
        raise Exception("회원 정보가 없습니다.")
    
    obj = elcsoft.model.user.User()
    obj.getData(kwargs['user_id'])

    if obj.__pkValue__ <= 0 :
         raise Exception("존재하지 않는 회원 정보입니다.")

    if not 'url' in obj.picture :
        return True

    url = "%s" % obj.picture['url']
    path = "/home/pi/www/image/user/%s" % obj.__pkValue__
    file = "%s/%s" % (path, obj.picture['name'])
    cmd = "curl -s https://api2.hizib.wikibox.kr%s > %s" % (url, file)
    #print(url)
    #print(path)
    #print(file)
    #print(cmd)

    if not os.path.exists("/home/pi/www/image") :
        os.system("mkdir /home/pi/www/image")
        os.system("chmod 755 /home/pi/www/image")

    if not os.path.exists("/home/pi/www/image/user") :
        os.system("mkdir /home/pi/www/image/user")
        os.system("chmod 755 /home/pi/www/image/user")

    if not os.path.exists(path) :
        os.system("mkdir %s" % path)
        os.system("chmod 755 %s" % path)

    os.system(cmd)

    if not os.path.exists(file) :
        raise Exception("파일을 다운로드하는데 실패하였습니다.")

    obj.picture['url'] = url
    obj.picture['path'] = path

    if not obj.save() :
        raise Exception("사진 정보를 저장하는데 실패하였습니다.")
    
    return obj

#facesDownloadProcess
def facesDownloadProcess(**kwargs) :
    if not 'user_id' in kwargs :
        raise Exception("회원 정보가 없습니다.")
    
    obj = elcsoft.model.user.User()
    obj.getData(kwargs['user_id'])

    if obj.__pkValue__ <= 0 :
        raise Exception("존재하지 않는 회원 정보입니다.")

    if len(obj.faces) <= 0:
        return True
    
    path = "/home/pi/www/image/user/%s" % obj.__pkValue__
    #print(path)
    
    if not os.path.exists("/home/pi/www/image") :
        os.system("mkdir /home/pi/www/image")
        os.system("chmod 755 /home/pi/www/image")

    if not os.path.exists("/home/pi/www/image/user") :
        os.system("mkdir /home/pi/www/image/user")
        os.system("chmod 755 /home/pi/www/image/user")

    if not os.path.exists(path) :
        os.system("mkdir %s" % path)
        os.system("chmod 755 %s" % path)

    path = "%s/face" % path

    os.system("rm -rf %s" % path)
    os.system("mkdir %s" % path)
    os.system("chmod 755 %s" % path)

    faces = dict()

    for i in obj.faces :
        face = obj.faces[i]
        #print(face)
        if 'url' in face :
            url = "%s" % face['url']
            file = "%s/%s" % (path, face['name'])
            cmd = "curl -s https://api2.hizib.wikibox.kr%s > %s" % (url, file)

            print("%s : %s" % (i, url))
            print("%s : %s" % (i, file))
            print("%s : %s" % (i, cmd))

            os.system(cmd)

            if not os.path.exists(file) :
                raise Exception("파일을 다운로드하는데 실패하였습니다.")

            lib.rotate_image_based_on_exif(file)

            url = file.replace('/home/pi/www', '')
            temp = file.split("/")

            faces[i] = dict()
            faces[i]['path'] = file
            faces[i]['url'] = url
            faces[i]['name'] = temp[-1]
            faces[i]['size'] = face['size']

    obj.faces = faces

    if not obj.save() :
        raise Exception("안면인식용 사진 정보를 저장하는데 실패하였습니다.")

    return obj

#face image delete
def faceImageDelete(**kwargs) :
    if not 'user_id' in kwargs :
        raise Exception("회원 정보가 없습니다.")
    
    obj = elcsoft.model.user.User()
    obj.getData(kwargs['user_id'])

    if obj.__pkValue__ <= 0 :
        raise Exception("존재하지 않는 회원 정보입니다.")
    
    token = elcsoft.controller.smartdoor.getToken()

    # self.faces가 딕셔너리라고 가정할 때
    if len(obj.faces) :
        for key, o in obj.faces.items():
            #lib.log("%s : %s" % (key, o))
            url = 'https://api2.hizib.wikibox.kr/User/faceUpload?user_id=%s&idx=%s&isDel=1' % (obj.__pkValue__, key)
            result = lib.restapi(method="get", url=url, token=token, isDebug=True)
            if result['result'] :
                lib.log(o)
                # 파일이 존재하는지 확인
                if os.path.exists(o['path']):
                    os.remove(o['path'])  # 파일 삭제
                    lib.log(f"파일 '{o['path']}'가 삭제되었습니다.")

    obj.faces = dict()
    
    if not obj.save() :    
        raise Exception("삭제한 정보를 저장하는데 실패하였습니다.")
    
    deleteAllFaceImages(user_id=obj.__pkValue__)
    
    return obj

def deleteAllFaceImages(**kwargs):
    if not 'user_id' in kwargs :
        raise Exception("회원 정보가 없습니다.")
    
    obj = elcsoft.model.user.User()
    obj.getData(kwargs['user_id'])

    if obj.__pkValue__ <= 0 :
        raise Exception("존재하지 않는 회원 정보입니다.")
    
    path = "/home/pi/www/image/user/%s/face/" % obj.__pkValue__

    if not '1' in obj.faces :
        lib.delete_all_in_path(path)

    return obj
