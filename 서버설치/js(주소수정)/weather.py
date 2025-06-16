# ~/www/kiosk/python/weather.py

# -*- coding: utf-8 -*-
import lib
import time
import argparse
import elcsoft.model.weather

#현재시간 해당 지역 날씨
def search(areacode) :
    now = time
    timecode = now.strftime("%Y%m%d%H")

    obj = elcsoft.model.weather.Weather()
    obj.getDataByCondition("areacode='%s' AND timecode='%s'" % (areacode, timecode))

    if obj.__pkValue__ <= 0 :
        url = 'https://api2.hizib.wikibox.kr/Weather/%s' % areacode
        
        try :
            data = lib.restapi(method="get", url=url)
            obj.fromDict(data)
            if not obj.save() :
                raise Exception(obj.__errorMsg__)
        except Exception as e:
            lib.log(e)

    if obj.__pkValue__ <= 0:
        obj.getDataByCondition("areacode='%s' ORDER BY timecode desc LIMIT 1" % areacode)

    return obj.toDict()


def main():
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('-areacode', '-a', help='Areacode Code', required=True)
    args = parser.parse_args()

    results = dict()

    try :
        data = search(args.areacode)
        results['result'] = True
        results['data'] = data
    except Exception as e:
        results['result'] = False
        results['message'] = getattr(e, 'message', str(e))
    rs = lib.jsonencode(results)
    print(rs)

if __name__ == '__main__':
    main()

