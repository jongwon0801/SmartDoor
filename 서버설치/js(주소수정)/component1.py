# ~/www/python/elcsoft/component.py

#!/usr/bin/python
import os
import lib
import sys
import re
import json
import elcsoft.db
import datetime
import requests
import urllib3
import lib

from decimal import *

class Component(object):
	__lib__ = {}
	__tableName__ = ''
	__pkName__ = ''
	__pkValue__ = 0
	__column__ = []
	__errorMsg__ = ''
	__script__ = ''
	__params__ = dict()
	__kwargs__ = dict()
	
	dbconn = None

	# __init__
	def __init__(self, **kwargs):
		global global_config
		if not 'global_config' in globals():
			global_config = lib.getConfigByJsonFile('/home/pi/www/python/config.json')

		self.__kwargs__ = kwargs
		urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

		for column in self.__column__ :
			if 'field' in column and 'default' in column :
				self.setField(column['field'], column['type'], column['default'])
			else :
				self.setField(column['field'], column['type'], 0)
				
		if not 'isEcho' in kwargs :
			kwargs['isEcho'] = False

		if 'db_config' in kwargs :
			self.__lib__['db'] = kwargs['db_config']
		else :
			self.__lib__['db'] = global_config['db']
			
		if 'db_handler' in kwargs :
			self.__lib__['conn'] = kwargs['db_handler']
			self.install()
		else :
			self.__lib__['conn'] = elcsoft.db.DBConn(**self.__lib__['db'])
			self.install()
			
	#getFields
	def getFields(self, label):
		result = ''
		
		for column in self.__column__ :
			if result != '' :
				result = result + ','
			
			result = result + label + '.' + column['field'] + ' AS ' + label + '_' + column['field']
		
		return result
	
	#getDefaultValue
	def getDefaultValue(self, column):
		if 'default' in column :
			return column['default']
		elif column['type'].upper() == 'INT' or column['type'].upper() == 'SMALLINT' or column['type'].upper() == 'MEDIUMINT' or column['type'].upper() == 'INTEGER' or column['type'].upper() == 'BIGINT' :
			return 0
		elif column['type'].upper() == 'DECIMAL' or column['type'].upper() == 'DEC' or column['type'].upper() == 'NUMERIC' or column['type'].upper() == 'FIXED' :
			return 0
		elif column['type'].upper() == 'FLOAT' or column['type'].upper() == 'DOUBLE' or column['type'].upper() == 'DOUBLE PRECISION' or column['type'].upper() == 'REAL' or column['type'].upper() == 'BIT' :
			return 0
		else :
			return ''

	def getForeignKey(self):
		return self.__tableName__ + "(" + self.__pkName__ + ")"
	
	#get
	def get(self, name, default=''):
		if name in self.__kwargs__ :
			return self.__kwargs__[name]
		else :
			return self.getVars(name, default)
	
	#getCookie
	def getCookie(self, name, default=''):
		if not 'http_handler' in self.__kwargs__ :
			return default
		
		return self.__kwargs__['http_handler'].getCookie(name, default)
	
	#getVars
	def getVars(self, name, default=''):
		if not 'http_handler' in self.__kwargs__ :
			return default
		
		print(self.__kwargs__['http_handler'])
		
		return self.__kwargs__['http_handler'].getVars(name, default)

	#getHost
	def getHost(self):
		if not 'http_handler' in self.__kwargs__ :
			raise Exception('Http Handler is not found.')
		
		return self.__kwargs__['http_handler'].getHost()
			
	#getUri
	def getUri(self):
		if not 'http_handler' in self.__kwargs__ :
			raise Exception('Http Handler is not found.')
		
		return self.__kwargs__['http_handler'].getUri()
			
	#getUrl
	def getUrl(self):
		if not 'http_handler' in self.__kwargs__ :
			raise Exception('Http Handler is not found.')
		
		return self.__kwargs__['http_handler'].getUrl()
			
	#getRemoteAddr
	def getRemoteAddr(self):
		if not 'http_handler' in self.__kwargs__ :
			raise Exception('Http Handler is not found.')
		
		return self.__kwargs__['http_handler'].getRemoteAddr()
	
	#setCookie
	def setCookie(self, name, value, expires_days=365):
		if not 'http_handler' in self.__kwargs__ :
			raise Exception('Http Handler is not found.')
		
		return self.__kwargs__['http_handler'].setCookie(name, value, expires_days)
		
	#set
	def setField(self, key, keytype, value) :
		if key == self.__pkName__ :
			if value == None or value == '':
				self.__pkValue__ = 0
			else :
				self.__pkValue__ = int(value)
		elif keytype.upper() == 'INT' or keytype.upper() == 'SMALLINT' or keytype.upper() == 'MEDIUMINT' or keytype.upper() == 'INTEGER' or keytype.upper() == 'BIGINT' :
			if value == None :
				setattr(self, key, 0)
			elif type(value) == 'int':
				setattr(self, key, value)
			else :
				setattr(self, key, int(value))
		elif keytype.upper() == 'DECIMAL' or keytype.upper() == 'DEC' or keytype.upper() == 'NUMERIC' or keytype.upper() == 'FIXED' :
			if value == None :
				setattr(self, key, 0)
			else :
				setattr(self, key, Decimal(value))
		elif keytype.upper() == 'FLOAT' or keytype.upper() == 'DOUBLE' or keytype.upper() == 'DOUBLE PRECISION' or keytype.upper() == 'REAL' or keytype.upper() == 'BIT' :
			if value == None :
				setattr(self, key, 0)
			else :
				setattr(self, key, float(value))
		elif keytype.upper() == 'JSON' :
			if value == None :
				setattr(self, key, dict())
			else :
				setattr(self, key, self.jsondecode(value))
		elif keytype.upper() == 'DATE' or keytype.upper() == 'TIME' or keytype.upper() == 'DATETIME' or keytype.upper() == 'TIMESTAMP' or keytype.upper() == 'YEAR' :
			if type(value) is str and value.upper() == "CURRENT_TIMESTAMP" :
				setattr(self, key, "")
			else :
				setattr(self, key, str(value))
		else :
			if value == None :
				setattr(self, key, "")
			else :
				setattr(self, key, str(value))

	# dropTable
	def dropTable(self, isEcho=False) :
		sql = "DROP TABLE " + self.__tableName__

		if isEcho :
			print(sql)
			sys.exit()

		self.__lib__['conn'].execute(sql)

		return True

	# createTable
	def createTable(self, isEcho=False) :
		sql = ""
		for column in self.__column__ :
			if sql != "" :
				sql = sql + ","

			if column['type'] == 'json' :
				sql = sql +  column['field'] + " longtext"
			else :
				sql = sql +  column['field'] + " " + column['type']

			if 'size' in column :
				sql = sql + "(%s)" % column['size']

			if 'option' in column :
				sql = sql + " " + column['option']

			if 'key' in column and column['key'] != "" :
				sql = sql + " NOT NULL"

			if 'default' in column :
				if type(column['default']) is str and column['default'] == 'CURRENT_TIMESTAMP' :
					sql = sql + " DEFAULT %s" % column['default']
				elif type(column['default']) is str :
					sql = sql + " DEFAULT '%s'" % column['default']
				else :
					sql = sql + " DEFAULT %s" % column['default']

			if 'extra' in column :
				sql = sql + " " + column['extra']

		for column in self.__column__ :
			if 'keytype' in column and column['keytype'] == 'primary' :
				sql = sql + ", PRIMARY KEY (" + column['key'] + ")"
			elif 'keytype' in column and column['keytype'] == 'foreign' :
				sql = sql + ", FOREIGN KEY (" + column['key'] + ") REFERENCES " + column['refrence']
			elif 'key' in column and column['key'] != '' :
				sql = sql + ", KEY " + column['key'] + "("  + column['key'] + ")"

		sql = "CREATE TABLE " + self.__tableName__ + "("+ sql + ")"

		if isEcho :
			print(sql)
			sys.exit()

		self.__lib__['conn'].execute(sql)

		return True

	# isTable
	def isTable(self, isEcho=False) :
		sql = "SHOW TABLES"
		if isEcho :
			print(sql)
			sys.exit()

		results = self.__lib__['conn'].query(sql)
		for result in results :
			key = 'Tables_in_' + self.__lib__['db']['name']
			if result[key] == self.__tableName__ :
				return True

		return False

	# install
	def install(self, isEcho=False) :
		if not self.isTable() :
			return self.createTable(isEcho)

		return True
	
	# getResult
	def getResult(self, **kwargs):
		if not 'rows' in kwargs :
			kwargs['rows'] = 1
		
		results = self.getResults(**kwargs)
		
		if len(results) <= 0 :
			return None
		
		return results[0]
	
	# getResults
	def getResults(self, **kwargs):
		if not 'table' in kwargs :
			kwargs['table'] = self.__tableName__
		
		return self.__lib__['conn'].select(**kwargs)			
	
	# getDataByCondition
	def getDataByCondition(self, condition, isEcho=False):
		self.__init__(**self.__kwargs__)
		results = self.getResults(where=condition,isEcho=isEcho)
		
		#print("%s %s" % (condition, len(results)))
		#print(results)

		if len(results) :
			self.fromDict(results[0])

	# getDataRecent
	def getDataRecent(self, isEcho=False):
		results = self.getResults(orderby="%s desc" % self.__pkName__, rows=1, isEcho=isEcho)

		if len(results):
			self.fromDict(results[0])

	# getData
	def getData(self, pkValue, isEcho=False):
		result = self.getDataByCondition(self.__pkName__ + "=%s" % pkValue, isEcho)
		return result
	
	# isData
	def isData(self, condition, isEcho=False):
		results = self.getResults(field="COUNT(*) as total",where=condition,isEcho=isEcho)
		if len(results) :
			data = results[0]
		
			if data['total'] > 0 :
				return True
		
		return False
	
	# getTotal
	def getTotal(self, condition="", isEcho=False):
		results = self.getResults(field="COUNT(*) as total",where=condition,isEcho=isEcho)
		data = results[0]

		return data['total']
	
	# getMax
	def getMax(self, field, condition="", default="", isEcho=False):
		f = "MAX(" + field + ") as " + field 
		results = self.getResults(field=f, where=condition, isEcho=isEcho)
		data = results[0]
		
		if data[field] == None :
			return default

		return data[field]
	
	# getSum
	def getSum(self, field, condition="", default="", isEcho=False):
		f = "SUM(" + field + ") as " + field 
		results = self.getResults(field=f, where=condition, isEcho=isEcho)
		data = results[0]
		
		if data[field] == None :
			return default

		return data[field]
	
	# getUnixTimestamp
	def getUnixTimestamp(self, dt):
		#print(dt)
				
		temp = dt.split(' ')
		t1 = temp[0].split('-')
		year = t1[0].strip()
		month = t1[1].strip()
		day = t1[2].strip()
		
		t2 = temp[1].split(':')
		hour = t2[0].strip()
		min = t2[1].strip()
		sec = t2[2].strip()
		
		#print("getUnixTimestamp : %s-%s-%s %s:%s:%s" % (year, month, day, hour, min, sec))
		
		return self.mktime(int(hour), int(min), int(sec), int(month), int(day), int(year))
		
	# displayDateTime
	def displayDateTime(self, field):
		d = getattr(self, field)
		
		return d
	
	def displayDate(self, field):
		d = getattr(self, field)
		
		temp = d.split(' ')
		return temp[0]
		
	def displayTime(self, field):
		d = getattr(self, field)
		
		temp = d.split(' ')
		return temp[1]
			
	#save
	def save(self, isEcho=False):
		name = ''
		value = ''

		if not self.isData("%s=%s" % (self.__pkName__, self.__pkValue__)) :
			data = []
			for column in self.__column__:
				key = column['field']
				keytype = column['type']

				if name == '' :
					name = key
				else :
					name = name + ',' + key

				if value == '' :
					value = '%s'
				else :
					value = value + ',%s'

				if keytype.upper() == 'JSON' :
					data.append(self.jsonencode(getattr(self, key)))
				elif key == self.__pkName__ :
					data.append(self.__pkValue__)
				else:
					data.append(getattr(self, key))

			sql = 'INSERT INTO ' + self.__tableName__ + ' (' + name + ') VALUES (' + value + ')'

			if isEcho :
				print(sql % tuple(data))
				
			curs, conn = result = self.__lib__['conn'].execute(sql, tuple(data))
			self.__pkValue__ = curs.lastrowid
			curs.close()
			conn.close()
		else :
			data = []
			for column in self.__column__:
				key = column['field']
				keytype = column['type']

				if key != self.__pkName__ :
					if name == '' :
						name = key + '=%s'
					else :
						name = name + ',' + key + '=%s'

					if keytype.upper() == 'JSON' :
						data.append(self.jsonencode(getattr(self, key)))
					else:
						data.append(getattr(self, key))
						
			sql = 'UPDATE ' + self.__tableName__ + ' SET ' + name + ' WHERE ' + self.__pkName__ + '=' + str(self.__pkValue__)
			
			if isEcho :
				print(sql % tuple(data))

			curs, conn = self.__lib__['conn'].execute(sql, tuple(data))
			curs.close()
			conn.close()

		return True

	# delete
	def delete(self, isEcho=False):
		sql  = "DELETE FROM " + self.__tableName__ + " WHERE %s='%s'" % (self.__pkName__, self.__pkValue__)
		result = self.__lib__['conn'].query(sql, isEcho)
		return True

	# deleteByCondition
	def deleteByCondition(self, condition, isEcho=False):
		sql  = "DELETE FROM " + self.__tableName__ + " WHERE %s" % condition
		result = self.__lib__['conn'].query(sql, isEcho)
		return True

	# setArguments
	def setArguments(self, rq):
		for column in self.__column__ :
			#print("%s : %s"% (column['field'], rq.getVars(column['field'])))
			if column['field'] in rq.request.arguments :
				name = column['field']
				value = rq.getVars(name, self.getDefaultValue(column))
				
				setattr(self, column['field'], value)
				
	# setKwargs
	def setKwargs(self, **kwargs):
		for column in self.__column__ :
			name = column['field']
			
			if name in kwargs :				
				value = kwargs[name]
				
				setattr(self, name, value)
	
	# setData
	def setData(self, data, label=''):
		if data != None:
			for column in self.__column__:
				if label == '' :
					name = column['field']
				else :
					name = label + '_' + column['field']
					
				if name in data :
					self.setField(column['field'], column['type'], data[name])

	# fromDict
	def fromDict(self, data):
		if data != None :
			for column in self.__column__:
				key = column['field']
				if key in data :
					self.setField(column['field'], column['type'], data[key])
				elif key == self.__pkName__ and key in data:
					self.__pkValue__ = data[key]

	# fromObj
	def fromObj(self, obj):
		self.__pkValue__ = obj.__pkValue__

		for column in self.__column__:
			key = column['Field']

			if key != self.__pkName__ and hasattr(obj, key) :
				setattr(self, key, getattr(obj, key))

	#toTxt
	def toTxt(self):
		result = ''
		for column in self.__column__:
			if result != '':
				result = result + ','
			result = result + column['Field']

		return result

	# toDict
	def toDict(self):
		result = {}
		for column in self.__column__:
			key = column['field']
			
			if self.ereg_match('_id$', key) and key != self.__pkName__:
				name = lib.ereg_replace('_id$', '', key) + 'Obj'
				name = lib.convert_variable_name(name)
				if hasattr(self, name) :
					result[name] = getattr(self, name).toDict()

			if key == self.__pkName__:
				result[key] = self.__pkValue__
			else :
				result[key] = getattr(self, key)
				#print("%s %s %s" % (key, result[key], type(result[key])))
		return result
	
	# toJson
	def toJson(self):
		result = '%s' % self.toDict()
		result = lib.jsondecode(result.replace("'", '"'))
		return result
	
	# check_blank
	def checkBlank(self, field):
		return self.check_blank(getattr(self, field))
	
	# check_blank
	def check_blank(self, str):
	    if str == None:
	        return True
	    elif str == 'None':
	        return True
	    elif str == '0000-00-00':
	        return True
	    elif str == '00:00:00':
	        return True
	    elif str == '0000-00-00 00:00:00':
	    		return True
	    elif str == '':
	        return True
	    return False
	
	#jsondecode
	def jsondecode(self, s):
		return lib.jsondecode(s)

	#jsonencode
	def jsonencode(self, obj):
		return lib.jsonencode(obj)
	   
	# replaceQuotes(text):
	def replaceQuotes(self, text):
	    return text.replace('"', "&quot;").replace("'", '&#039;')

	# replaceQuotes(text):
	def restoreQuotes(self, text):
	    return text.replace("&quot;",'"').replace('&#039;',"'")
	   	
	# NOW
	def now(self) :
	    dt = str(datetime.datetime.now()).split(".")
	    return dt[0]
	   
	# time
	def time(self):
		return self.getUnixTimestamp(self.now())
	
	# mktime
	def mktime(self, hour, min, sec, month, day, year):
	   	return int(datetime.datetime(year, month, day, hour, min, sec).timestamp()) 

	# date
	def date(self, format, ts):
		return datetime.datetime.fromtimestamp(ts).strftime(format)
	   	
	# ereg_match
	def ereg_match(self, regExpress, str, isIgnorecase=False):
	    if isIgnorecase == True :
	        regex = re.compile(regExpress, re.I)
	    else:
	        regex = re.compile(regExpress)
	
	    mo = regex.search(str)
	    if mo == None:
	        return False
	    else:
	        return True

	# displaySelectDbTag
	def displaySelectDbTag(self, **kwargs):
		tag = '<select'
		if 'formName' in kwargs :
			tag = tag + ' name="%s"' % kwargs['formName']
			
		if 'onchange' in kwargs :
			tag = tag + ' onchange="%s"' % kwargs['onchange']
			
		if 'option' in kwargs :
			tag = tag + ' ' + kwargs['option']
			
		tag = tag + '>'
		
		if 'initName' in kwargs :
			tag = tag + '<option value="">%s</option>' % kwargs['initName']
		
		results = self.getResults(**kwargs)
		
		fields = kwargs['field'].split(',')
		
		for result in results :
			obj = elcsoft.model.company.Company()
			obj.setData(result)
			
			if fields[0] == obj.__pkName__ :
				value = obj.__pkValue__
			else :
				value = getattr(obj, fields[0])
						
			name = getattr(obj, fields[1])
						
			tag = tag + '<option value="%s"' % value
			if 'default' in kwargs and obj.__pkValue__ == kwargs['default'] : 
				tag = tag + ' selected="selected" style="background:#EFEFEF;"'
			tag = tag + '>%s</option>' % name
			
		tag = tag + '</select>'
		
		#print(tag)
		return tag
	
	# displayPhone
	def displayPhoneNumber(self, phone):
	    phone = phone.replace("-", "").strip()
	    
	    if phone == '' or phone == '-' or phone == '--' :
	        return ''
	        
	    first = phone[0:3]
	    middle = phone[3:-4]
	    last = phone[-4:]
	    phone = "%s-%s-%s" % (first, middle, last)
	    
	    return phone

	# 서버 등록 후 가져오기
	def joinProcess(self):
		#print("%s joinProcess" % self.__tableName__)

		if self.__pkValue__ > 0 :
			self.__errorMsg__ = "%s 정보가 존재합니다." % self.__tableName__
			return False

		url = 'https://api2.hizib.watchbook.tv/%s' % (self.__class__.__name__)
		res = requests.post(url, json=self.toJson())

		if res.status_code == 200:
			data = lib.jsondecode(res.text)

			if data['result'] :
				self.fromDict(data)
				return self.save()
			else :
				self.__errorMsg__ = data['message']
		elif res.status_code == 401:
			self.__errorMsg__ = "접근 권한이 없습니다."
			return False
		else:
			self.__errorMsg__ = "알수 없는 에러로 중단되었습니다."
			return False

	# 서버에서 데이터 가져와서 동기화 시키기
	def downloadProcess(self, **kwargs):
		#print("%s downloadProcess" % self.__tableName__)

		if self.__pkName__ in kwargs:
			self.__pkValue__ = int(kwargs[self.__pkName__])

		if self.__pkValue__ <= 0 :
			self.__errorMsg__ = "%s 정보가 없습니다." % self.__tableName__
			return False

		url = 'https://api2.hizib.watchbook.tv/%s/%s' % (self.__class__.__name__, self.__pkValue__)
		res = requests.get(url)

		if res.status_code == 200:
			data = lib.jsondecode(res.text.strip())
			#print(data)
			self.fromDict(data)
			if not self.save():
				self.__errorMsg__ = "%s에 저장하는데 실패하였습니다." % self.__tableName__
				return False
			return True
		elif res.status_code == 400:
			data = lib.jsondecode(res.text.strip())
			self.__errorMsg__ = data['message']
			return False
		else:
			data = lib.jsondecode(res.text.strip())
			self.__errorMsg__ = data['message']
			return False

	# 서버 업데이트
	def updateProcess(self, **kwargs):
		#print("%s updateProcess" % self.__tableName__)

		if self.__pkValue__ <= 0 :
			self.__errorMsg__ = "%s 정보가 없습니다." % self.__tableName__
			return False

		url = 'https://api2.hizib.wikibox.kr/%s/%s' % (self.__class__.__name__, self.__pkValue__)
		#print(url)
		#print(self.toJson())
		res = requests.put(url, json=self.toJson())

		if res.status_code == 200:
			data = lib.jsondecode(res.text)
			#print(data)

			if data['result']:
				return True
			else:
				self.__errorMsg__ = data['message']
				return False
		elif res.status_code == 401:
			self.__errorMsg__ = "접근 권한이 없습니다."
			return False
		else:
			self.__errorMsg__ = "알수 없는 에러로 중단되었습니다."
			return False

	# updateByCondition
	def updateByCondition(self, update, condition, isEcho=False):
		sql = "UPDATE " + self.__tableName__ + " SET %s WHERE %s" % (update, condition)
		result = self.__lib__['conn'].query(sql, isEcho)
		return True

	# __str__
	def __str__(self):
		sb = []
		for key in self.__dict__:
			sb.append("{key}='{value}'".format(key=key, value=self.__dict__[key]))

		return ',\n '.join(sb)

	# __repr__
	def __repr__(self):
		return self.__str__()
