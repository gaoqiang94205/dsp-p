import etcd
import json

import os

from dsp.utils.constants import ETCD_CLIENT
etcd_client = ETCD_CLIENT
def getall():
    # import pdb;pdb.set_trace()
    allapptemplate = []
    try:
        directory = etcd_client.get('/dsp/apptemplate')
        for result in directory.children:
            allapptemplate.append (result.key.split('/')[3])
        print json.dumps(allapptemplate)
        return json.dumps(allapptemplate)
    except etcd.EtcdValueError:
        return "value error"
    except etcd.EtcdKeyError:
        return "key error"

def get(name):
    #name = data.get("name")
    dbkey = '/dsp/apptemplate/' + name
    try:
        tem = etcd_client.read(dbkey).value
        return tem
    except etcd.EtcdKeyError:
        return "key error"


def add(data):
    print data
    name = data.get("name")
    dbkey = '/dsp/apptemplate/' + name
    print dbkey
    try:
        etcd_client.set(dbkey,data)
    except etcd.EtcdKeyError:
        return "key error"
    except etcd.EtcdValueError:
        return "value error"
    return "true"


def set(data):
    name = data.get("name")
    dbkey = '/dsp/apptemplate/' + name
    try:
        etcd_client.set(dbkey, data)
    except etcd.EtcdKeyError:
        return "key error"
    except etcd.EtcdValueError:
        return "value error"
    return "true"


def delete(data):
    name = data.get("name")
    dbkey = '/dsp/apptemplate/' + name
    try:
        etcd_client.delete(dbkey)
    except etcd.EtcdKeyError:
        return "key error"
    except etcd.EtcdValueError:
        return "value error"
    return "true"

if __name__=='__main__':
    getall()
    abs_path = os.path.abspath('.')
    path = os.path.join(abs_path, 'templates/dao-2048.yaml')
    print path
    data = {u'compose': path, u'describe': u'a demo for dao_2048', u'name': u'dao-2048'}
    add(data)