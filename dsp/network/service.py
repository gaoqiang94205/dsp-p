# -*- coding:utf-8 -*-
import json

from dsp.utils import constants

def get_net():
    docker = constants.MANAGER_CLIENR
    networks = docker.networks()
    result = []
    for net in networks:
        netinfo={}
        netinfo['name'] = net.get('Name','')
        netinfo['driver'] = net.get('Driver','')
        netinfo['scope'] = net.get('Scope','')
        result.append(netinfo)

    return json.dumps(result)

if __name__ == '__main__':
    get_net()
