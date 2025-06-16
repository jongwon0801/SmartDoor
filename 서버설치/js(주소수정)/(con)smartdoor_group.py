# ~/www/python/elcsoft/controller/smartdoor_group.py

import lib
import elcsoft.model.smartdoor_group
import elcsoft.controller.smartdoor

# downloadProcess
def downloadProcess(**kwargs):
    obj = elcsoft.model.smartdoor_group.SmartdoorGroup()

    if not obj.__pkName__ in kwargs :
        raise Exception("단지 정보가 없습니다.")
    
    obj.getData(kwargs[obj.__pkName__])

    
    token = elcsoft.controller.smartdoor.getToken()

    url = 'https://api2.hizib.wikibox.kr/SmartdoorGroup/%s' % kwargs[obj.__pkName__]
    #data = lib.restapi(method="get", url=url, token=token, isDebug=True)
    data = lib.restapi(method="get", url=url, token=token)
    print(data)

    obj.fromDict(data)

    if not obj.save():
        raise Exception("단지 정보를 저장하는데 실패하였습니다. 원인 - %s" % obj.__errorMsg__)

    return obj
