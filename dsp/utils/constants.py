import etcd

from dsp.utils.dsp_docker_client import DSPRESTClient

DOCKER_BASE_URL = 'unix://var/run/docker.sock'
MANAGER_URL='unix://var/run/docker.sock'

MANAGER_CLIENR=DSPRESTClient(MANAGER_URL)
ETCD_CLIENT = etcd.client.Client(
             host='0.0.0.0',
             port=2379,
             )

if __name__=='__main__':
    with open('host_port','rw+') as port_num:
        port = port_num.readline()
        #port_new =  int(port)+1
        port_num.write('10001rger')
