# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
import convertGPS
import json

"""
author@wuying
date@2017.5.14
"""


def getGPS(city, siteName):
    """
    :param SiteName: 站点名称
    :return: GPS经维度
    """
    # 地址
    url = "http://api.map.baidu.com/geocoder/v2/"
    # 提交的参数数据
    postData = {
        "output": "json",
        "ret_coordtype": "gcj02ll",
        "ak": "dDv7awtHK7vBOppUxYGzrRHdk5Fw0K9R",
        "callback": "showLocation",
        "city": city,
        "address": siteName
    }
    data = urllib.urlencode(postData)

    # 设置浏览器头
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
               'Referer': 'http://www.zhihu.com/articles'}
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

        jsonData = json.loads(response.read())
        GPS = 'None'
        if jsonData['status'] == 0 and jsonData['result']['level'] == u"收费处/收费站":
            GPS = city + ',' + str(jsonData['result']['location']['lat']) + ',' + str(jsonData['result']['location']['lng'])

        return GPS


def writeFile():
    """
    :return: 将GPS写入文件
    """
    feeSite = open("feeSites.txt")
    gps = open("feeSites_GPS_baidu.txt", "a")

    for line in feeSite:
        feeName = ''.join([line.strip().decode('utf-8') + u'收费站', u'']).encode('utf-8')
        print feeName

        cityList = ["广州", "深圳", "佛山", "东莞", "中山", "珠海", "江门", "肇庆", "惠州", "汕头", "潮州", "揭阳", "汕尾", "湛江",
                    "茂名", "阳江", "韶关", "清远", "云浮", "梅州", "河源"]
        for city in cityList:
            GPS = getGPS(city, feeName)
            if GPS != 'None':
                gps_list = str(GPS).split(',')
                city = gps_list[0]
                gcjLat = float(gps_list[1])
                gcjLng = float(gps_list[2])
                # 将百度地图的GCJ坐标系转化为WGS坐标系
                wgsLat, wgsLng = convertGPS.gcj2wgs(gcjLat, gcjLng)
                site_gps = city + ',' + feeName + ',' + str(wgsLat) + ',' + str(wgsLng)
                gps.write(site_gps + '\n')

    gps.close()
    feeSite.close()


if __name__ == '__main__':
    writeFile()
    # cityList = ["广州", "深圳", "佛山", "东莞", "中山", "珠海", "江门", "肇庆", "惠州", "汕头", "潮州", "揭阳", "汕尾",  "湛江",
    # "茂名", "阳江", "韶关", "清远", "云浮", "梅州", "河源"]
    # GPSList = []
    # for city in cityList:
    #     GPS = getGPS(city, "吴家围收费站")
    #     if GPS != 'None':
    #         if GPS[7::] not in GPSList:
    #             GPSList.append(GPS[7::])
    #             for each in GPSList:
    #                 print city + each



