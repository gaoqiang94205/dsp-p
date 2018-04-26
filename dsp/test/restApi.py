#!/usr/bin/env python
# coding: utf-8

import hashlib
import httplib
import base64
import urllib

httpClient = None
try:
    cre = "admin:admin"

    headers = {"Content-type": "application/x-www-form-urlencoded"
        , "Accept": "text/plain", "Date": time_str,
               "Authorization": "HTAUTH", username: signature, "Host": "rest.hugetable.com"}
    httpClient = httplib.HTTPConnection("10.133.47.163", 9092, timeout=300)
    httpClient.request("GET", "/data/yiliaoyun", None, headers)

    response = httpClient.getresponse()
    #     response.ContentType = "text/xml";
    #     response.Charset = "UTF-8";
    xx = response.read()
    xmlstr = ""
    xmlstr += str(response.status) + response.reason + str(response.msg) + str(response.version) + "\n"
    print "--------------------" + xx
    print xmlstr
except Exception, e:
    print e
finally:
    if httpClient:
        httpClient.close()