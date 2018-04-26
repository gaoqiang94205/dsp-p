# encoding=utf-8
import docker
from werkzeug.exceptions import HTTPException
from werkzeug.http import HTTP_STATUS_CODES

class HTTPError(HTTPException, object):
    def __init__(self, description=None, response=None, code=None):

        super(HTTPError, self).__init__(description=description, response=response)
        self.response = response
        self.description = description
        self.code = code or self.status_code

    def __str__(self):
        err_type = ''
        message = HTTP_STATUS_CODES.get(self.code, 'Unknown Error')
        if self.is_client_error():
            err_type = 'Client Error: '
        elif self.is_server_error():
            err_type = 'Server Error: '
        if self.description:
            message = '{} {} {}("{}")'.format(self.status_code, err_type, message, self.description)
        return message

    __repr__ = __str__

    @property
    def status_code(self):
        if self.code:
            return self.code
        if self.response is not None:
            return self.response.status_code

    def is_client_error(self):
        if self.status_code is None:
            return False
        return 400 <= self.status_code < 500

    def is_server_error(self):
        if self.status_code is None:
            return False
        return 500 <= self.status_code < 600

class APIException(Exception):
    code = 400
    error = 'api_exception'

    def __init__(self, message=None, code=None, error=None):
        self.code = code or self.code
        self.error = error or self.error
        self.message = message or self.message

    @property
    def data(self):
        return {'message': self.message, 'error': self.error}

    def __str__(self):
        return '%s %s' % (self.code, self.message)

    __repr__ = __str__
#-------------------------以上为自定义service

class DockerAPIError(APIException):
    code = 400
    error = 'docker_api_error'


class InvalidName(APIException):
    error = 'invalid_name'
    message = u"无效的名称，只能包含大小写字母、中划线、下划线并且长度小于20个字符"


class InvalidValue(APIException):
    error = 'invalid_value'


class InvalidInterval(APIException):
    error = 'invalid_interval'
    # message = 'Interval should be integer and no more less than 5'
    message = u"轮询间隔必须为正数、大于等于 5 且小于等于 120"

#-----------自定义----------------
class AlreadyExist(APIException):
    error = 'already_exist'

class NodeException(APIException):
    error ='invalid_node'
    message = '该节点已经是swarm的成员'

class BindInUse(APIException):
    code = 400
    error = 'bind_in_use'
    # message = "Bind is in use, please disable it first"
    message = u"该绑定正在使用中，请先停用"

class RuleInUse(APIException):
    code = 400
    error = 'rule_in_use'
    # message = "Bind is in use, please disable it first"
    message = u"该规则已经绑定了服务，请先解绑"

class InvalidAddress(APIException):
    error = 'invalid_address'
    message = u"无效的访问地址，请检查你的输入"


class NoSuchPartition(APIException):
    code = 594
    error = 'no_such_partition'


class UnknownError(APIException):
    error = 'unknown_error'


class AccessKeyNotValid(APIException):
    error = 'access_key_not_valid'
    # message = 'Access Key Pair not found or not valid, please check your configuration'
    message = u"没有访问秘钥(AccessKey)或者无效，请检查你的配置"


class TooLong(APIException):
    code = 400
    error = 'too_long'
    message = u"输入长度应不大于 200 字符"
