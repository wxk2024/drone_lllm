from typing import List
from langchain.tools import BaseTool
import json
from urllib.request import urlopen, quote
import requests,csv

class BaiduDitu(BaseTool):
  name:str = "BaiduDitu"
  description:str = "use region's name and query's location to determine latitude and longtitude"
  def _run(self,region:str,query:str):
    url = 'https://api.map.baidu.com/place/v2/search'
    output = 'json'
    ak = 'phz4cmP55L8115sy2GjiF7GQVgU4FOiE' #'你申请的密钥***'
    reg = quote(region) #由于本文城市变量为中文，为防止乱码，先用quote进行编码
    que = quote(query)
    #先确定搜索结果的总数
    uri = url + '?' + 'query=' + que + '&region=' + reg + '&page_size=20&output=' + output + '&ak=' + ak
    req = urlopen(uri)
    res = req.read().decode() #将其他编码的字符串解码成unicode
    temp = json.loads(res) #对json数据进行解析
    # print(temp)
    total = temp['total']    #将json中的搜索结果总数输出
    
    page_num = int(total/20)+1
    jiaotong = []   #创建一个空列表，记录所有的搜索记录
    for i in range(page_num):    #将每页的20条搜索结果输出
        page_num_str = str(i)
        uri1 = url + '?' + 'query=' + que + '&region=' + reg + '&page_size=20&page_num=' + page_num_str + '&output=' + output + '&ak=' + ak
        req1 = urlopen(uri1)
        res1 = req1.read().decode() #将其他编码的字符串解码成unicode
        temp1 = json.loads(res1) #对json数据进行解析
        l = len(temp1['results'])
        for j in range(l):
            dic = dict()    #创建一个空字典，记录所需的搜索结果
            lat = temp1['results'][j]['location']['lat']
            lon = temp1['results'][j]['location']['lng']
            name = temp1['results'][j]['name']
            add = temp1['results'][j]['address']
            dic['city'] = region
            dic['name'] = name
            dic['add'] = add
            dic['lon'] = lon
            dic['lat'] = lat
            jiaotong.append(dic)
    fanhui = []
    for q in range(len(jiaotong)):
       one = dict()
       one['region'] = jiaotong[q]['city']
       one['address'] = jiaotong[q]['add']
       one['name'] = jiaotong[q]['name']
       one['lat'] = jiaotong[q]['lat']
       one['lon'] = jiaotong[q]['lon']
       fanhui.append(one)
    return fanhui
    
