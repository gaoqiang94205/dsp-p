# -*- coding: utf-8 -*-  

'''
@author: yankay
'''
import json
import logging
import ssl
import time
from collections import OrderedDict
from urlparse import urlparse

import etcd
from etcd import EtcdKeyNotFound

from dsp.common.config import CLIENT_CERT_AUTH_CONFIG
from dsp.common.config import ETCD_URL
#from dsp.common.etcd_lock import EtcdLock

LOG = logging.getLogger(__name__)

ETCD_CLIENTS = {}

'''
存储路径规划
'''
BASE_DIR = '/DSP/v1'
ACCOUNT_DIR = '/'.join((BASE_DIR, 'account')) + '/'



"""
DOCKER PATH
"""
DOCKER_BASE_DIR = '/docker'
SWARM_BASE_DIR = '/'.join((DOCKER_BASE_DIR, 'swarm')) + '/'

SWARM_PRIMARY_PATH = SWARM_BASE_DIR + 'leader'


class ETCDClient(etcd.Client):
    def __init__(self, ssl_verify=True, *args, **kwargs):
        super(ETCDClient, self).__init__(*args, **kwargs)
        if not ssl_verify:
            # according to pyinstaller bug, we have to specify ssl_version manually
            ssl_version = getattr(ssl, 'PROTOCOL_TLS', None) or getattr(ssl, 'PROTOCOL_SSLv23')
            self.http.connection_pool_kw['ssl_version'] = ssl_version
            self.http.connection_pool_kw['cert_reqs'] = ssl.CERT_REQUIRED
            self.http.connection_pool_kw['assert_hostname'] = False


def etcd_client(etcd_url=ETCD_URL):
    global ETCD_CLIENTS

    if etcd_url not in ETCD_CLIENTS:
        url_parts = urlparse(ETCD_URL)
        cert, ca_cert = CLIENT_CERT_AUTH_CONFIG
        client = ETCDClient(
            ssl_verify=False,
            host=url_parts.hostname,
            port=url_parts.port,
            protocol='https',
            cert=cert,
            ca_cert=ca_cert,
        )
        ETCD_CLIENTS[etcd_url] = client

    return ETCD_CLIENTS[etcd_url]


def get_etcd_lock(lock_key, token=None):
    """
    :param lock_key:
    :param value: This param must be unique between other instances.
    :return:
    """
    return EtcdLock(etcd_client(), lock_key=lock_key, token=token)


def etcd_ls(key, recursive=False, load_json=True):
    try:
        leaf = etcd_client().read(key, recursive=recursive)
        res = OrderedDict()
        if len(leaf._children) == 0:
            return res
        for r in leaf.leaves:
            l = len(key)
            if not key.endswith('/'):
                l += 1
            k = r.key[l:]
            res[k] = r.value
            if r.value is not None and len(r.value) > 0 and load_json:
                res[k] = json.loads(r.value)
        return res
    except EtcdKeyNotFound:
        return {}


def etcd_mkdir(key):
    try:
        return etcd_client().get(key)
    except EtcdKeyNotFound:
        return etcd_client().write(key, value=None, dir=True,
                                   prevExist=False)


def etcd_get(key, load_json=True, quiet=True):
    try:
        r = etcd_client().get(key)
        res = r.value
        if r.value is not None and len(r.value) > 0 and load_json:
            res = json.loads(r.value)
        return res
    except EtcdKeyNotFound:
        if quiet:
            return None
        raise


def etcd_watch(key, timeout=0, recursive=None):
    while True:
        try:
            r = etcd_client().watch(key, timeout=timeout, recursive=recursive)
        except etcd.EtcdWatchTimedOut:
            LOG.info('etcd_watch timeout, rewatch now...')
        except Exception as e:
            LOG.error('etcd_watch error: %s' % e)
            time.sleep(1)
        else:
            if r:
                yield r


def etcd_exists(key):
    try:
        etcd_client().get(key)
        return True
    except EtcdKeyNotFound:
        return False


def etcd_version():
    ec = etcd_client()
    data = ec.api_execute('/version', ec._MGET).data.decode('utf-8')
    try:
        return json.loads(data)
    except (TypeError, ValueError):
        raise etcd.EtcdException("Cannot parse json data in the response")


def etcd_wait_ready():
    start = time.time()
    ec = etcd_client()
    while True:
        if time.time() - start > 30:
            return
        try:
            r = ec.api_execute('/version', ec._MGET)
            if r.status == 200:
                return
        except Exception:
            LOG.warning("Fetch etcd version failed, maybe etcd not ready, sleep 1 second to next check.")
        time.sleep(1)
