# -*- coding: utf-8 -*-
import multiprocessing
import os
import tempfile


def clean_url(base_url):
    if base_url.endswith('/'):
        base_url = base_url[:-1]
    return base_url


def str2bool(v):
    if v is None:
        return v
    return v.lower() in ("yes", "true", "t", "1")


def str2int(v):
    return int(v)


def cpu_count():
    try:
        return multiprocessing.cpu_count()
    except:
        return 4


'''
基本设置
'''
API_PREFIX = os.getenv('API_PREFIX', '/dce')
PROD = str2bool(os.getenv('PROD', "False"))  # 开启线上环境，减少日志，禁止DEBUG
WEB_CONCURRENCY = str2int(os.getenv('WEB_CONCURRENCY', min(max(cpu_count(), 4), 8)))  # Worker数量，默认cpu_count,
SECRET_KEY = 'DaoCloud-DCE'
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'dangerous')
CONTROLLER_ADVERTISE = os.getenv('CONTROLLER_ADVERTISE', '127.0.0.1')
SERVER_NAME = os.getenv('SERVER_NAME', 'http://dce_controller_1')
DEPLOYMENT_GC_INTERVAL = str2int(os.getenv('DEPLOYMENT_GC_INTERVAL', 86400))
DOCKER_REGISTRY_URL = clean_url(os.getenv('DOCKER_REGISTRY_URL', 'https://registry-1.docker.io'))
DOCKER_REGISTRY_AUTH_SERVER_URL = clean_url(os.getenv('DOCKER_REGISTRY_AUTH_SERVER_URL', 'https://auth.docker.io/token'))
DCE_CLOUD_URL = clean_url(os.getenv('DCE_CLOUD_URL', 'https://dce.daocloud.io'))
LICENSE_SERVER_URL = 'https://license.daocloud.io'
DEFAULT_RESET_PASSWORD = os.getenv('DEFAULT_RESET_PASSWORD', '123456')
TEMP_DIRECTORY = tempfile.gettempdir()
MAILGUN_DOMAIN = 'enterprise.daocloud.io'
MAILGUN_API_KEY = 'key-a541646b8c03b8da9fb73aa0f672b9ec'
GOTTY_MAX_LIFETIME = str2int(os.getenv('GOTTY_MAX_LIFETIME', '1296000'))
GOTTY_GC_INTERVAL = str2int(os.getenv('GOTTY_GC_INTERVAL', '2592000'))
GOTTY_BINARY_PATH = os.getenv('GOTTY_BINARY_PATH', '/usr/local/bin/gotty')
DOCKER_BINARY_PATH = os.getenv('DOCKER_BINARY_PATH', '/usr/local/bin/docker')
KUBECTL_BINARY_PATH = os.getenv('KUBECTL_BINARY_PATH', '/usr/local/bin/kubectl')
HA_CONTROLLER_CONF_PATH = os.getenv('HA_CONTROLLER_CONF_PATH', '/etc/nginx/conf.d/hacluster.lconf')
BUILDIN_REGISTRY_NGINX_CONF_PATH = os.getenv('BUILDIN_REGISTRY_NGINX_CONF_PATH', '/etc/nginx/conf.d/buildin_registry.lconf')
BUILDIN_REGISTRY_CONF_PATH = os.getenv('BUILDIN_REGISTRY_CONF_PATH', '/etc/docker/registry/conf.yml')
# STAGE = str2bool(os.getenv('STAGE', 'True'))
INTEGRATION_PATH = os.getenv('INTEGRATION_PATH', '/usr/share/nginx/integration')
CUSTOM_NAMESERVERS = filter(lambda s: len(s) > 0, os.getenv('CUSTOM_NAMESERVERS', '223.5.5.5').split(' '))
MAX_JOBS_PER_PROJECT = str2int(os.getenv('MAX_JOBS_PER_PROJECT', 100))
CLIENT_CERTIFICATION_PATH = os.getenv('CLIENT_CERTIFICATION_PATH', '/etc/ssl/private/client/client-cert.pem')
CLIENT_PRIVATE_KEY_PATH = os.getenv('CLIENT_PRIVATE_KEY_PATH', '/etc/ssl/private/client/client-key.pem')
CLIENT_CERTIFICATION_CA_PATH = os.getenv('CLIENT_CERTIFICATION_CA_PATH', '/etc/ssl/private/client/ca.pem')
CLIENT_CERT_AUTH_CONFIG = ((CLIENT_CERTIFICATION_PATH, CLIENT_PRIVATE_KEY_PATH), CLIENT_CERTIFICATION_CA_PATH)
KUBE_ADMIN_CERTIFICATION_PATH = os.getenv('KUBE_ADMIN_CERTIFICATION_PATH', '/etc/ssl/private/client/kube-admin-cert.pem')
KUBE_ADMIN_PRIVATE_KEY_PATH = os.getenv('KUBE_ADMIN_PRIVATE_KEY_PATH', '/etc/ssl/private/client/kube-admin-key.pem')
KUBE_ADMIN_CERTIFICATION_CA_PATH = os.getenv('KUBE_ADMIN_CERTIFICATION_CA_PATH', '/etc/ssl/private/client/ca.pem')
KUBE_ADMIN_CERT_AUTH_CONFIG = ((KUBE_ADMIN_CERTIFICATION_PATH, KUBE_ADMIN_PRIVATE_KEY_PATH), KUBE_ADMIN_CERTIFICATION_CA_PATH)
SSL_PKEY_FILE = os.getenv('SSL_PKEY_FILE', '/etc/ssl/private/https/dce.key')
SSL_CERT_FILE = os.getenv('SSL_CERT_FILE', '/etc/ssl/private/https/dce.crt')
OEM_CONFIG_PATH = os.getenv('OEM_CONFIG_PATH', '/etc/dce/oem.yml')
CONTROLLER_EXPORTED_PORT = str2int(os.getenv('CONTROLLER_EXPORTED_PORT', 80))
CONTROLLER_SSL_EXPORTED_PORT = str2int(os.getenv('CONTROLLER_SSL_EXPORTED_PORT', 443))
REFRESH_PRIMARY_LOCK_INTERVAL = str2int(os.getenv('REFRESH_PRIMARY_LOCK_INTERVAL', 5))
NODES_LIST_FILE = os.getenv('NODES_LIST_FILE', '/tmp/dce-nodes')
NODES_DISCOVERY_INTERVAL = str2int(os.getenv('NODES_DISCOVERY_INTERVAL', 10))
CONTROLLER_PROCESS_LOCK = os.getenv('CONTROLLER_PROCESS_LOCK', '/tmp/dce-controller.lock')
SWARM_BINARY_PATH = os.getenv('SWARM_BINARY_PATH', '/usr/local/bin/swarm')
MODE = os.getenv('MODE', 'docker')
NETWORK_DRIVER = os.getenv('NETWORK_DRIVER', 'calico')

NGINX_INDEX_HTTPS_PATH = os.getenv('NGINX_INDEX_HTTPS_PATH', '/etc/nginx/conf.d/index_https.lconf')

GIT_SHA = os.getenv('GIT_SHA', '')
BUILD_NUMBER = os.getenv('BUILD_NUMBER', '')

"""
Swarm的位置
"""

SWARM_URL = os.getenv('SWARM_URL', 'tcp://dce_controller_1:2375')
SWARM_NONE_TLS_URL = os.getenv('SWARM_NONE_TLS_URL', 'tcp://dce_controller_1:80')
DOCKER_SELF_HOST_URL = os.getenv('DOCKER_SELF_HOST_URL', 'http+unix:///var/run/docker.sock')

"""
Kubernetes API Server 对位置
"""
KUBE_API_SERVER_URL = os.getenv('KUBE_API_SERVER_URL', 'http://dce_kube-controller_1:8080')

"""
Etcd的位置
"""
ETCD_URL = os.getenv('ETCD_URL', 'etcd://localhost:2379')

"""
Stream Server 相关配置
"""

STREAM_URL = clean_url(os.getenv('STREAM_URL', 'http://127.0.0.1/stream'))
STREAM_ROOM_KEY = os.getenv('STREAM_ROOM_KEY')

"""
Buildin Registry Auth配置
"""
BUILDIN_REGISTRY_SERVICE = 'DCE-BUILDIN-REGISTRY'
BUILDIN_REGISTRY_ISSUER = 'DCE-REGISTRY-AUTH-SERVER'

"""
REDIS的位置
"""
REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0')

'''
NEW_RELIC相关
'''
NEW_RELIC_LICENSE_KEY = os.getenv('NEW_RELIC_LICENSE_KEY', '')
NEW_RELIC_APP_NAME = os.getenv('NEW_RELIC_APP_NAME', '')

'''
getsentry相关
'''
SENTRY_DSN = os.getenv('SENTRY_DSN',
                       'http://e1adc5766fcb4dd28cb4926d234d941e:688a404ffc464a1693d481cac495f6f7@apps.getsentry.com/67104?timeout=30&verify_ssl=0')

"""
temp-blob相关
"""
TEMP_BLOB_UPLOAD_PATH = os.getenv('TEMP_BLOB_UPLOAD_PATH', '/usr/share/nginx/uploads/temp-blob')
TEMP_BLOB_CLEAN_INTERVAL = str2int(os.getenv('TEMP_BLOB_CLEAN_INTERVAL', 60 * 60))

"""image 相关"""
HUB_PREFIX = os.getenv('HUB_PREFIX', 'daocloud.io/daocloud')

