# -*- coding:utf-8 -*-
import urllib
import urllib2
import time
import hashlib

def send(phone=None,strmsg=None):
    timestamp = str(int(round(time.time()*1000)))
    print timestamp
    username = 'cosmoplat'
    system = '65535'
    num = '528946'
    h1 = hashlib.md5()
    phone = '15060032237'
    #stri = username + system + phone + timestamp
    mds = "cosmoplatcosmoplatsys" + phone + timestamp
    h1.update(mds.encode(encoding='utf-8'))
    strmsg = h1.hexdigest()
    print strmsg
    data = {'username':'cosmoplat','phone':'15060032237','message':'欢迎使用“COSMOPlat”平台，验证码：453584。为了保障账号安全，请勿向他人泄露','strmsg':strmsg,'timestamp':timestamp}
    data_url = urllib.urlencode(data)
    #url = 'http://his.haier.net/sms/smsphone/sendPhoneByHis?
   # print url
    #import pdb;pdb.set_trace()
    print 'http://his.haier.net/sms/smsphone/sendPhoneByHis?%s'%data_url
    request = urllib2.Request('http://his.haier.net/sms/smsphone/sendPhoneByHis?%s'%data_url)

    response = urllib2.urlopen(request)
    print response.read()

def sendtest():
    url = 'http://192.168.123.251/api/v1/nodes'
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    print response.read()
if __name__=='__main__':
    send()

