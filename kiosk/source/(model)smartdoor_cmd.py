/home/pi/www/python/elcsoft/model/smartdoor_cmd.py

#!/usr/bin/python
import lib

import elcsoft.component

class SmartdoorCmd(elcsoft.component.Component):
    def __init__(self, **kwargs):
        self.__tableName__ = 'smartdoor_cmd'
        self.__pkName__ = 'smartdoor_cmd_id'
        self.__column__ = [
            {"field": "smartdoor_cmd_id", "type": "bigint", "option": "unsigned", "keytype": "primary", "key": "smartdoor_cmd_id", "extra": "auto_increment"},
            {"field": "user_id", "type": "bigint", "option": "unsigned", "key": "user_id", "defaul": 0},
            {"field": "type", "type": "int", "size": 2, "key": "type", "default": 0},
            {"field": "code", "type": "varchar", "size": 255, "key": "code", "default": ""},
            {"field": "name", "type": "varchar", "size": 255, "key": "name", "default": ""},
            {"field": "regDate", "type": "timestamp", "key": "regDate", "default": "CURRENT_TIMESTAMP"}
        ]
        elcsoft.component.Component.__init__(self, **kwargs)

    # isValidate
    def isValidate(self, obj):
        if lib.check_blank(obj.type) :
            self.__errorMsg__ = '문열기 방법을 입력해 주세요.'
            return False

        return True

    # save
    def save(self, isEcho=False):
        if not self.isValidate(self):
            return False
        
        if lib.check_blank(self.regDate) :
            self.regDate = lib.now()

        return super().save(isEcho)
