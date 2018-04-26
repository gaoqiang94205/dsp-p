# -*- coding:utf-8 -*-
import json
import requests

def getall():
    allimages = []
    res = requests.get('http://0.0.0.0:5000/v2/_catalog')
    for iname in (json.loads(res.text).get('repositories')):
        tags = json.loads(requests.get('http://0.0.0.0:5000/v2/'+iname+'/tags/list').text).get('tags')
        try:
            for tag in tags:
                allimages.append(iname+':'+tag)
        except TypeError:
            print 'null'
    return json.dumps(allimages)

#根据name和tag删除容器
def delete(name,tag):
    #name = data.get('imagename')
    # tag = data.get('tag')
    headers = {'accept':'application/vnd.docker.distribution.manifest.v2+json'}
    res1 = requests.get('http://0.0.0.0:5000/v2/'+name+'/manifests/'+tag, headers = headers)
    digest = res1.headers.get('docker-content-digest')
    try:
        res2 = requests.delete('http://0.0.0.0:5000/v2/'+name+'/manifests/'+digest)
    except TypeError,e:
        return 'false'+e.message
    return 'true'


if __name__=='__main__':
    print getall()
    print delete()