# -*- coding:utf-8 -*-
from dsp.image.service import getall

def valify(image):
    return allow_image(image)

def is_image(name,tag):
    images = getall()
    search = name +':'+ tag
    if search in images:
        return True
    return False

#判断一个镜像地址是否在可操作的范围内
def allow_image(image):
    name,tag = ''
    if image.find(':') ==-1:
        name = image
        tag = 'latest'
    else:
        name = image.split(':')[0]
        tag = image.split(':')[1]
    isimage = is_image(image)
    return isimage

if __name__=="__main__":
    #print getall()
    print is_image('daocloud/busybox','latest')
