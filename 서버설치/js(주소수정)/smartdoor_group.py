# ~/www/python/elcsoft/model/smartdoor_group.py

#!/usr/bin/python
import lib
import elcsoft.component

class SmartdoorGroup(elcsoft.component.Component):
    def __init__(self, **kwargs):
        self.__tableName__ = 'smartdoor_group'
        self.__pkName__ = 'smartdoor_group_id'
        self.__column__ = [
            {"field": "smartdoor_group_id", "type": "bigint", "option": "unsigned", "keytype": "primary", "key": "smartdoor_group_id", "extra": "auto_increment"},
            {"field": "areacode", "type": "varchar", "size": 255, "key": "areacode", "default": ""},
            {"field": "name", "type": "varchar", "size": 255, "key": "name", "default": ""},
            {"field": "address", "type": "json", "default": "{}"}
        ]
        elcsoft.component.Component.__init__(self, **kwargs)

    # isValidate
    def isValidate(self, obj):
        if lib.check_blank(obj.name) :
            self.errorMsg = '단지명을 입력해 주세요.'
            return False

        return True
    
    # save
    def save(self, isEcho=False):
        if not self.isValidate(self):
            return False

        return super().save(isEcho)

    # downloadProcess
    def downloadProcess(self, **kwargs):
        if not 'token' in kwargs :
            raise Exception("토큰 정보가 없어 스마트도어 정보를 동기화 하는데 실패하였습니다.")

        if self.__pkName__ in kwargs :
            self.__pkValue__ = kwargs[self.__pkName__]

        url = 'https://api2.hizib.wikibox.kr/SmartdoorGroup/%s' % self.__pkValue__
        data = lib.restapi(method="get", url=url, token=kwargs['token'])
        #print(data)

        self.fromDict(data)

        if not self.save():
            raise Exception("단지 정보를 저장하는데 실패하였습니다. 원인 - %s" % self.__errorMsg__)

        return True
