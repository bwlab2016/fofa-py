# -*- coding: utf-8 -*-
import base64
import json
import urllib
import urllib2
import re
import datetime


class Client:
    def __init__(self,email,key):
        self.email = email
        self.key = key
        self.base_url = "https://fofa.so"
        self.search_api_url = "/api/v1/search/all"
        self.login_api_url = "/api/v1/info/my"
        self.get_userinfo() #check email and key

    def get_userinfo(self):
        api_full_url = "%s%s" % (self.base_url,self.login_api_url)
        param = {"email":self.email,"key":self.key}
        res = self.__http_get(api_full_url,param)
        return json.loads(res)

    def get_data(self,query_str,page=1,size=100,fields=""):
        res = self.get_json_data(query_str,page,fields)
        return json.loads(res)

    def get_json_data(self,query_str,page=1,size=100,fields=""):
        api_full_url = "%s%s" % (self.base_url,self.search_api_url)
        param = {"qbase64":base64.b64encode(query_str),"email":self.email,"key":self.key,"page":page,"fields":fields,"size":size}
        res = self.__http_get(api_full_url,param)
        return res

    def get_lasttime(self, ip, port):
        query_str = 'ip="%s" && port="%s"' % (ip, port)
        print(query_str)
        param = {"qbase64": base64.b64encode(query_str)}
        param = urllib.urlencode(param)
        url = "https://fofa.so/result"
        url = "%s?%s" % (url, param)
        try:
            req = urllib2.Request(url)
            res = urllib2.urlopen(req).read()
            regex = re.compile(r'fa fa-clock-o" aria-hidden="true"></i> (.*?)</li>\n')
            timestr = regex.findall(res)[0]
            lasttime = (datetime.datetime.strptime(timestr, '%Y-%m-%d') - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        except urllib2.HTTPError, e:
            print "errmsg：" + e.read(),
            raise e
        return lasttime
    def __http_get(self,url,param):
        param = urllib.urlencode(param)
        url = "%s?%s" % (url,param)
        try:
            req = urllib2.Request(url)
            res = urllib2.urlopen(req).read()
            if "errmsg" in res:
                raise RuntimeError(res)
        except urllib2.HTTPError,e:
            print "errmsg："+e.read(),
            raise e
        return res