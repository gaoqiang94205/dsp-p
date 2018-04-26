# -*- coding:utf-8 -*-
from flask import logging
from dsp.utils.constants import MANAGER_CLIENR

log = logging.getLogger(__name__)
#启动容器
def run_container(image_name,command,expose_port):
    docker = MANAGER_CLIENR
    if image_name.find(':')==-1:
        image_name = image_name+':latest'
    image_info = [image_info for image_info in docker.images() if image_name in image_info.get('RepoTags')]
    print image_info.__len__()
    status = 'faild run container,not find the image'
    if image_info.__len__():
        log.info(image_name)
        #先把{"11":"22"}转换{11：22}
        convert_port={}
        #当接受的是字典形式的数据
        # for k,v in expose_port.items():
        #     int_k = int(k)
        #     int_v = int(v)
        #     convert_port[int_k]=int_v

        #当接受的是字符串形式
        for p2p in expose_port.split(","):
            single = p2p.split(":")
            int_k = int(single[0])
            int_v = int(single[1])
            convert_port[int_k] = int_v

        ports = convert_port.keys()
        host_config = docker.create_host_config(port_bindings= convert_port)
        container_id = docker.create_container(image=image_name,hostname='busy', command=command,ports=ports, host_config=host_config, detach=True, stdin_open=True, tty=True);
        docker.start(container_id)
        status = 'running'
    return status

#批量删除容器
def rm_container(containers,volume,link,force):
    docker = MANAGER_CLIENR
    for container in containers:
        docker.remove_container(container,v=volume,link=link, force=force)
    re_status = 'remove containers successfully'
    return re_status

#获取容器信息
def get_containers():
    docker = MANAGER_CLIENR
    containers = docker.containers(trunc=True)
    results = []
    for container in containers:
        result = {}
        result['status'] = container.get('Status', '')
        result['name'] = container.get('Names', '')
        result['image'] = container.get('Image', '')
        result['state'] = container.get('State', '')
        result['id'] = container.get('Id','')
        ports = container.get('Ports')
        #获取容器镜像的简要信息
        image_name = container.get('Image', '').split('@')
        if len(image_name) >1:
            result['image'] = image_name[0]
        #print ports
        ip_port = []
        if ports.__len__():
            for port in ports:
                #ip = port.get("IP")
                ip = None
                port = port.get('PublicPort')
                tcp=None
                if  ip and port:
                   tcp = u'%s:%s'%(ip,port)
                elif ip:
                    tcp = ip
                else:
                    tcp = port

                ip_port.append(tcp)
        result['ip_port']=ip_port
        results.append(result)
    return results

if __name__=='__main__':
    #dic = run_container('busybox',command='/bin/bash')
    print get_containers()

