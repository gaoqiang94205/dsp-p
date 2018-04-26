# -*- coding:utf-8 -*-
import json

from docker.types import TaskTemplate, ContainerSpec, RestartPolicy, ServiceMode, EndpointSpec, Mount
from flask import logging

from dsp.node.service import get_all_ip
from dsp.utils.constants import MANAGER_CLIENR

log = logging.getLogger(__name__)

# 启动应用
# docker service create --replicas 2 --restart-condition on-failure busybox sleep 3000
def run_service(service_name, image_name, command, restart_condition,
                networks, s_and_t, ports, mode='global', replicas=1):
    docker = MANAGER_CLIENR
    from dsp.image.valify import valify
    #if not valify(image_name):
     #   return "找不到应用指定的镜像！"
    # Mount对象的集合
    mounts = []
    image_name = '192.168.123.251/'+image_name
    for s_t in s_and_t:
        type = False
        if s_t.get('read_only', '') == 'yes':
            type = True
        m = Mount(source=s_t.get('source', ''), target=s_t.get('target', ''), read_only=type)
        mounts.append(m)
        print s_t.get('source', '')
    #containSpec = ContainerSpec( image=image_name, mounts=mounts, command=command, tty=True, open_stdin=True)
    containSpec = ContainerSpec( image=image_name, command=command, tty=True, open_stdin=True)

    # 声明TaskTemplate--->task
    # restart_condition --->none, on - failure, or any
    restart_policy = RestartPolicy(condition=restart_condition)
    task = TaskTemplate(container_spec=containSpec, restart_policy=restart_policy)
    # 应用启动模式
    if mode == "global":
        replicas = None
    service_mode = ServiceMode(mode=mode, replicas=replicas)
    # 接入点,包括负载均衡模式设置等
    end_point = EndpointSpec(ports=ports)

    service_id = docker.create_service(task_template=task, name=service_name,
                                       mode=service_mode, networks=networks, endpoint_spec=end_point)
    return service_id


# 删除应用
def rm_app(appids):
    docker = MANAGER_CLIENR
    for appid in appids:
        docker.remove_service(appid)
    return "successfully remove all services"

# 获取应用信息

def get_apps():
    docker = MANAGER_CLIENR
    services = docker.services()
    result = []
    for service in services:
        info = {}
        info['service_name'] = service.get('Spec',{}).get('Name', '')
        info['id'] = service.get('ID')
        info['image_name'] = service.get('Spec', {}) \
            .get('TaskTemplate', {}).get('ContainerSpec', {}) \
            .get('Image', '').split('@')[0]
        info['endpoint'] = service.get('Endpoint', {}).get('Spec')
        info['create_date'] = service.get('CreatedAt')
        info['replicas'] = service.get('Spec', {}).get('Mode', {}).get('Replicated', {}).get('Replicas')
        result.append(info)
    return result

def get_access_ip():
    return get_all_ip()

if __name__ == '__main__':
    service_name = 'busy_box'
    image_name = 'busybox:latest'
    command = 'sleep 1000'
    restart_condition='none'
    networks=[]
    s_and_t= [{"source":"/root","target":"/","read_only":"yes"}]
    #run_service(service_name, image_name, command, restart_condition,
     #           networks, s_and_t, mode='replicated', replicas=1, ports={})

    docker = MANAGER_CLIENR

    services = docker.services()

    result = []
    print services
    for service in services:
        info = {}
        info['service_name'] = service.get('Spec',{}).get('Name', '')
        id = service.get('ID')
        print id
        info['image_name'] = service.get('Spec',{}) \
            .get('TaskTemplate',{}).get('ContainerSpec', {})\
            .get('Image', '').split('@')[0]
        # print service.get('Spec',{}) \
        #     .get('TaskTemplate',{}).get('ContainerSpec', {}).get('Image','').split('@')[0]
        info['endpoint'] = service.get('Endpoint', {}).get('Spec')
        info['create_date'] = service.get('CreatedAt')
        info['replicas'] = service.get('Spec', {}).get('Mode', {}).get('Replicated', {}).get('Replicas')
        result.append(info)
    print  result