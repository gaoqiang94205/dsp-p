# -*- coding:utf-8 -*-
import os
import tarfile
from collections import Iterable
from io import BytesIO

from flask import logging
from dsp.error.errors import APIException, NodeException
from dsp.utils import constants
from dsp.utils.dsp_docker_client import DSPDockerClient, DockerHeavyClient, DSPRESTClient
from model import node

log = logging.getLogger(__name__)

default_docker = constants.DOCKER_BASE_URL
dsp_client = DSPRESTClient(base_url=default_docker)
# docker api
docker_hd = DockerHeavyClient(default_docker)


def get_nodes():
    nodes = []
    node_infos = dsp_client.nodes()
    if not isinstance(node_infos, Iterable):
        raise APIException(message="the object is not iterable")

    for node_info in node_infos:
        status = node_info.get('Status', {})
        state = status.get('State', 'down')
        host = node_info.get('Description', {}).get('Hostname')
        spec = node_info.get('Spec', {})
        role = spec.get('Role', '')
        Status = node_info.get('Status', {})
        if role== 'manager':
            Status = node_info.get('ManagerStatus', {})
        addr = Status.get('Addr', '')
        if state == 'ready':
            n = node()
            n.state = state
            n.host = host
            n.role = role
            n.address = addr
            nodes.append(n.__dict__)
    return nodes

def get_manager_ip():
    nodes = get_nodes()
    manager_ips = []
    for node in nodes:
        if node.get('_role') == 'manager':
            manager_ips.append(node.get('_address').split(":")[0])
    return manager_ips

def get_node_ips():
    nodes = get_nodes()
    node_ips = []
    for node in nodes:
        if node.get('_role') == 'worker':
            node_ips.append(node.get('_address').split(":")[0])
    return node_ips

def get_all_ip():
    nodes = get_nodes()
    node_ips = []
    for node in nodes:
        node_ips.append(node.get('_address').split(":")[0])
    return node_ips


def init_swarm(base_url=constants.MANAGER_URL,listen_addr='0.0.0.0:2377', force_new_cluster=False, swarm_spec={}):
    manager_client = DSPRESTClient(base_url=base_url)
    manager_client.init_swarm(listen_addr=listen_addr, force_new_cluster=force_new_cluster, swarm_spec=swarm_spec)

def join_swarm(ip, port):
    log.info("join th swarm")
    if ip in get_node_ips():
        raise NodeException
    base_url = "http://" + ip + ":" + port
    # import pdb
    # pdb.set_trace()
    dsp_remote_client = DSPRESTClient(base_url=base_url)
    swarm_dic = dsp_client.inspect_swarm()
    join_token = swarm_dic.get(u'JoinTokens').get(u'Worker')
    manager_ips = get_manager_ip()
    result = dsp_remote_client.join_swarm(remote_addrs=manager_ips, join_token=join_token)
    return result

# 离开swarm集群
def leave_swarm(node_ip, node_port, force=False):
    if node_ip in get_node_ips():
        base_url = "http://" + node_ip + ":" + node_port
        dsp_remote_client = DSPRESTClient(base_url=base_url)
        result = dsp_remote_client.leave_swarm(force=True)
        return result

# 创建.ssh文件夹
def create_ssh_dir():
    docker_hd = DockerHeavyClient(default_docker)
    container = docker_hd.containers.get("39386ddf4158")
    cd_root = 'echo "hello"'
    mk_dir = 'mkdir -p /root/.ssh'
    ssh_key = 'ssh-keygen -t rsa -P "" -f /root/.ssh/id_rsa'
    commands = list()
    commands.append(mk_dir)
    commands.append(ssh_key)
    commands.append(cd_root)
    for comm in commands:
        response = container.exec_run(comm)

# 生成tar包
def copy_ssh():
    docker_hd = DockerHeavyClient(default_docker)
    container = docker_hd.containers.get("39386ddf4158")
    container.exec_run("ssh-copy-id -i hadoop0")


def put_ssh_tar(containers_id):
    pw_tarstream = BytesIO()

    tarinfo = tarfile.TarInfo(name='gq.tar')
    tarinfo.size = os.path.getsize('/root/data/gq.tar')
    pw_tar = tarfile.TarFile(fileobj=pw_tarstream, mode='w')

    pw_tar.addfile(tarinfo, open('/root/data/gq.tar'))
    pw_tar.close()
    pw_tarstream.seek(0)
    # 根据container id上传tar包
    # import pdb ;pdb.set_trace()
    for c_id in containers_id:
        container = docker_hd.containers.get(c_id)
        container.put_archive(path='/root/gq/', data=pw_tarstream)
        # container.exec_run('mkdir /root/.ssh')
        pw_tarstream.seek(0)
        res = container.exec_run('tar -xvf /root/gq/gq.tar -C /root/gq')
        # 做第一次登陆
        # c_ip = container.get_ip
        container.exec_run('ssh -o stricthostkeychecking=no C_ip')
        print res
        # 如果执行成功了则进行首次登陆


def save_ssh_file():
    container = docker_hd.containers.get("39386ddf4158")
    (datas, stat) = container.get_archive(path='/root/.ssh', chunk_size=None)
    # 先将文件写到本地存储空间上，再拷贝到其他容器之上
    with open("/root/data/gq.tar", 'w') as f:
        for chunk in datas:
            print chunk
            f.write(chunk)

    '''
    print datas
    with tempfile.NamedTemporaryFile() as tmp:
        for chunk in datas:
            tmp.write(chunk)
        tmp.seek(0)
        with tarfile.open(mode='r', fileobj=tmp) as tar:
            tar.extractall(path='/root/data/ssh')
            tar.close()
            '''


if __name__ == "__main__":

    nodes = get_nodes()
    print nodes
    # node_dict = {'info': nodes}
    #    jstr = json.dumps(nodes)
    # print isinstance(nodes,Iterable)
    # join_swarm('192.168.124.11','2376')
    # connetc_docker()
    # get_manager_ip()
    # create_ssh()
    # put_ssh_file()
    # put_ssh_tar({'39386ddf4158'})
    # save_ssh_file()
    # for ip in get_node_ips():
    #     print ip
    #print join_swarm('192.168.124.11', '2376')
    print leave_swarm('192.168.124.11','2376',force=True)
