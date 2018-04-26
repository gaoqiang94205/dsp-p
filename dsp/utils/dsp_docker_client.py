# encoding=utf-8

import requests
import requests.exceptions
import urllib3
from docker import APIClient as Client
from docker import DockerClient
from docker.tls import TLSConfig
from docker.transport import SSLAdapter, UnixAdapter
from docker.utils.utils import kwargs_from_env
from requests.auth import HTTPBasicAuth

from dsp.error.errors import DockerAPIError
from dsp.settings import PROD

try:
    from docker.transport import NpipeAdapter
except ImportError:
    pass

urllib3.disable_warnings()
SWARM_CLIENT = None
DOCKER_CLIENTS = {}
DOCKER_CLIENTS_HEAVY = {}
DEFAULT_TIMEOUT_SECONDS = 180

class DockerHeavyClient(DockerClient):
    def __init__(self, *args, **kwargs):
        super(DockerHeavyClient, self).__init__(*args, **kwargs)
class DSPRESTClient(Client):
    def __init__(self, *args, **kwargs):
        super(DSPRESTClient, self).__init__(*args, **kwargs)

class DSPDockerClient(Client):
    def __init__(self, base_url=None, token=None, hostname='', username=None, password=None,
                 tls=False, num_pools=25):
        super(DSPDockerClient, self).__init__()
        self._hostname = ''
        if base_url.startswith('http+unix://'):
            self._custom_adapter = UnixAdapter(
                base_url, pool_connections=num_pools
            )
            self.mount('http+docker://', self._custom_adapter)
            self.base_url = 'http+docker://localunixsocket'
        else:
            if isinstance(tls, TLSConfig):
                tls.configure_client(self)
            elif tls:
                self._custom_adapter = SSLAdapter(pool_connections=num_pools)
                self.mount('https://', self._custom_adapter)
            self.base_url = base_url
            self.token = token
            self.username = username
            self.password = password
            if username and password:
                self.auth = HTTPBasicAuth(username, password)
            if token:
                self.headers['X-DSP-Access-Token'] = token


    def __repr__(self):
        return "<DSPDockerClient '%s'>" % self.base_url

    @property
    def hostname(self):
        if not self._hostname:
            self._hostname = self.info()['Name']
        return self._hostname

    def create_service_raw(self, service_spec, auth_header=None):
        headers = {}
        if auth_header:
            headers['X-Registry-Auth'] = auth_header

        url = self._url('/services/create')
        return self._result(self._post_json(url, data=service_spec, headers=headers), True)

    def update_service_raw(self, service_id, version, service_spec):
        url = self._url('/services/%s/update?version=%s' % (service_id, version))
        return self._result(self._post_json(url, data=service_spec), json=False)

    def _raise_for_status(self, response):
        """Raises stored :class:`APIError`, if one occurred."""
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise self.create_api_error_from_http_exception(e)

    def create_api_error_from_http_exception(self, e):
        """
        Create a suitable APIError from requests.exceptions.HTTPError.
        """
        response = e.response
        try:
            explanation = response.json()['message']
        except ValueError:
            explanation = response.content.strip()
        cls = DockerAPIError
        if response.status_code == 404:
            cls = NotFound
            if explanation and ('No such image' in str(explanation) or
                                        'not found: does not exist or no pull access'
                                    in str(explanation) or
                                        'registry does not exist' in str(explanation)):
                pass
        raise cls(message='Error while calling Docker API: %s' % explanation, code=response.status_code)


def check_kv_store_configured(docker_address):
    c = docker_client(base_url=docker_address, tls=True)
    info = c.info()
    cluster_store = info.get('ClusterStore')
    cluster_advertise = info.get('ClusterAdvertise')
    return True if (cluster_advertise and cluster_store) else False


def docker_client(base_url='http+unix://var/run/docker.sock', token=None, username=None, password=None,
                  hostname=''):
    global DOCKER_CLIENTS
    if not PROD and base_url.endswith('.sock'):
        return DSPDockerClient('http://192.168.100.30:1234', username='admin', password='admin')
        # return DCEDockerClient('http://106.75.116.205:31000', username='admin', password='GqJoy4QZUibWgMZI')
    key = tuple(map(str, [base_url, token, username, password, hostname,]))
    if not base_url in DOCKER_CLIENTS:
        kwargs = kwargs_from_env(assert_hostname=False)
        kwargs['base_url'] = base_url
        kwargs['hostname'] = hostname
        kwargs['username'] = username
        kwargs['password'] = password
        kwargs['token'] = token
        DOCKER_CLIENTS[key] = DSPDockerClient(**kwargs)

    return DOCKER_CLIENTS[key]

def docker_heavy(base_url = 'unix://var/run/docker.sock',username="admin",password="admin"):
    global DOCKER_CLIENTS_HEAVY
    key = tuple(map(str,[username,password]))
    if not PROD and base_url.endswith('.sock'):
        return DockerHeavyClient(base_url=base_url)
    else:
        #DOCKER_CLIENTS_HEAVY[] = DockerHeavyClient(base_url=base_url)
        pass
def swarm_client(swarm_url):
    pass





if __name__ == '__main__':
    #oc = DockerOOClient()
    #print json.dumps(oc.services.list()[0].app_name, indent=2)
    t = tuple(map(str,["aa","bb","cc"]))
    print t
    print str