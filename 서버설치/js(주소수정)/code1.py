# ~/www/python/elcsoft/model/code.py

#!/usr/bin/python
import lib
import elcsoft.component
import requests

class Code(elcsoft.component.Component):
    def __init__(self, **kwargs):
        self.__tableName__ = 'code'
        self.__pkName__ = 'code_id'
        self.__column__ = [
            {"field":"code_id","type":"bigint","option":"unsigned auto_increment","keytype":"primary","key":"code_id"},
            {"field":"gcode","type":"varchar","size":255,"key":"gcode","default":""},
            {"field":"code","type":"varchar","size":255,"key":"code","default":""},
            {"field":"name","type":"varchar","size":255,"key":"name","default":""},
            {"field":"nickname","type":"varchar","size":255,"key":"nickname","default":""},
            {"field":"sortNum","type":"int","size":10,"option":"unsigned","key":"sortNum","default":0},
            {"field":"isUse","type":"int","size":1,"option":"unsigned","key":"isUse","default":0}
        ]
        elcsoft.component.Component.__init__(self, **kwargs)
    # isValidate
    def isValidate(self, obj):
        if lib.check_blank(obj.gcode) :
            self.errorMsg = '코드그룹을 입력해 주십시오.'
            return False

        if lib.check_blank(obj.code) :
            self.errorMsg = '코드를 입력해 주십시오.'
            return False
        
        return True
    
    # save
    def save(self, isEcho=False):
        if self.sortNum <= 0 :
            results = self.__lib__['conn'].select("code", "MAX(sortNum) as sortNum", "WHERE gcode='%s'" % self.gcode);
            sortNum = results[0]['sortNum']
            
            if sortNum != None :
                self.sortNum = int(sortNum) + 1
            else :
                self.sortNum = 1
            
        if not self.isValidate(self):
            return False

        return super().save(isEcho)
    
    # updateAllProcess
    def updateAllProcess(self, gcode):
        url = 'https://api2.hizib.wikibox.kr/Code/getListByGcode?gcode=%s' % gcode
        #print(url)
        
        try :
            lists = lib.restapi(url=url,method="get")
            print(lists)

            if self.getTotal("gcode='SMARTDOOR_LOG_TYPE'") != len(lists) :
                for data in lists :
                    #print(data)
                    obj = Code()
                    obj.fromDict(data)

                    if not obj.save() :
                        self.__errorMsg__ = obj.__errorMsg__
                        return False

        except Exception as e:
            raise e
