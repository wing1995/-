# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import convertGPS

"""
author@wuying
date@2016.3.16
update@2017.5.14
"""


def getGPS(siteName):
    """
    :param SiteName: 站点名称
    :return: GPS经维度
    """
    # 地址
    url = "http://restapi.amap.com/v3/place/text"
    # 提交的参数数据
    postData = {
            "keywords": siteName,
            "key": "8325164e247e15eea68b59e89200988b",
            "page": "1",
            "offset": "10",
            "city": "440300",
            "callback": "jsonp_480469_",
            "s": "rsv3",
            "platform": "JS",
            "logversion": "2.0",
            "sdkversion": "1.3",
            "appname": "http://lbs.amap.com/console/show/picker"
            }
    data = urllib.urlencode(postData)

    # 设置浏览器头
    headers = {'User-Agent': "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11",\
               'Referer': 'http://www.zhihu.com/articles' }
    # request = urllib2.Request(url, data, headers)
    proxies = {'http': 'http://218.106.96.197:81'}
    try:
        response = urllib.urlopen(url, data, headers, proxies)
    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason
    else:
        data = response.read()[14: -1]
        jsonData = json.loads(data)

        GPS = 'None'
        counts = jsonData['count']
        if counts != "0":
            counts = int(counts)
            for each in range(min(counts, 3)):
                if jsonData['pois'][each]['type'] == u"道路附属设施;收费站;收费站" and jsonData['pois'][each]['pname'] == u"广东省"\
                        and siteName.decode('utf-8') in jsonData['pois'][each]['name']:
                    GPS = jsonData['pois'][each]['location']
                    break
        return GPS


def writeFile():
    """
    :return: 将GPS写入文件
    """
    feeSite = open("feeSites.txt")
    gps = open("feeSites_GPS_gaode.txt", "a")
    
    for line in feeSite:
        feeName = ''.join([line.strip().decode('utf-8') + u'收费站', u'']).encode('utf-8')
        print feeName
        
        GPS = getGPS(feeName)
        print GPS
        if GPS != 'None':
            gps_list = str(GPS).split(',')
            gcjLat = float(gps_list[1])
            gcjLng = float(gps_list[0])
            # 将高德的GCJ坐标系转化为WGS坐标系
            wgsLat, wgsLng = convertGPS.gcj2wgs(gcjLat, gcjLng)
            site_gps = feeName + ',' + str(wgsLat) + ',' + str(wgsLng)
            gps.write(site_gps + '\n')
        else:
            gps.write(feeName + ',' +'-1,-1' + '\n')
    gps.close()
    feeSite.close()

if __name__ == '__main__':
    writeFile()
    # print getGPS("新塘北收费站")
    
    

