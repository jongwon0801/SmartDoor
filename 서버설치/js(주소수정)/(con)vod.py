# ~/www/python/elcsoft/controller/vod.py

import lib
import os
import datetime
import base64
import elcsoft.controller.smartdoor
import elcsoft.controller.smartdoor_vod

global_config = lib.getConfigByJsonFile('/home/pi/www/python/config.json')

def saveFile(**kwargs):
  if not 'file' in kwargs:
    raise Exception("파일 데이터가 없어 업로드할 수 없습니다.")

  gcode = kwargs.get('gcode', datetime.datetime.now().strftime('%Y%m%d'))
  code = kwargs.get('code', datetime.datetime.now().strftime('%H%M'))

  path = "/home/pi/www/vod/%s" % gcode
  file = "%s.mp4" % code

  if not os.path.isdir(path):
      os.mkdir(path)

  filepath = os.path.join(path, file)

  data_start_index = kwargs['file'].find(',') + 1
  base64_data = kwargs['file'][data_start_index:]
  decoded_data = base64.b64decode(base64_data)

  with open(filepath, "wb") as file:
      file.write(decoded_data)

  if not os.path.exists(filepath) :
     raise Exception("녹화영상 업로드에 실패하였습니다.")
  
  return elcsoft.controller.smartdoor_vod.joinProcess(gcode=gcode, code=code, filepath=filepath)

def getFolders(**kwargs):
  global global_config

  path = kwargs.get('path', global_config['record']['path'])

  return lib.getFolders(path=path,reverse=True)

def getFiles(**kwargs):

  path = kwargs.get('path', None)

  if path is None:
      raise Exception("폴더 정보가 없습니다.")

  return lib.getFiles(path=path,reverse=True)

def streamProcess(**kwargs):
  global global_config

  path = kwargs.get('path', global_config['record']['path'])
  gcode = kwargs.get('gcode', '')
  code = kwargs.get('code', '')

  gcode_path = os.path.join(path, gcode)

  # 폴더가 존재하는지 검사
  if not os.path.exists(gcode_path):
      raise FileNotFoundError(f"폴더가 존재하지 않습니다: {gcode_path}")
  
  code_path = os.path.join(gcode_path, file)

  # 파일이 존재하는지 검사
  if not os.path.exists(code_path):
      raise FileNotFoundError(f"파일이 존재하지 않습니다: {code_path}")

  url = 'https://api2.hizib.wikibox.kr/Smartdoor/stream'
  lib.log("%s : %s" % (url, code_path))

  token = elcsoft.controller.smartdoor.getToken()

  with open(code_path, 'rb') as file:
      files = {'file': file}
      result = lib.restapi(method="file", url=url, data={'gcode':gcode,'code':code}, files=files, token=token, isDebug=True)

  return True

def unstreamProcess(**kwargs):
  global global_config

  path = kwargs.get('path', global_config['record']['path'])
  gcode = kwargs.get('gcode', '')
  code = kwargs.get('code', '')

  gcode_path = os.path.join(path, gcode)

  # 폴더가 존재하는지 검사
  if not os.path.exists(gcode_path):
      raise FileNotFoundError(f"폴더가 존재하지 않습니다: {gcode_path}")
  
  code_path = os.path.join(gcode_path, file)

  # 파일이 존재하는지 검사
  if not os.path.exists(code_path):
      raise FileNotFoundError(f"파일이 존재하지 않습니다: {code_path}")

  url = 'https://api2.hizib.wikibox.kr/Smartdoor/unstream'
  lib.log("%s : %s" % (url, code_path))

  token = elcsoft.controller.smartdoor.getToken()

  result = lib.restapi(method="post", url=url, data={'gcode':gcode,'code':code}, token=token, isDebug=True)
  lib.log(result)

  return True
