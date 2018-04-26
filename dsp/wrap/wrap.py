from functools import wraps
from flask_restful import reqparse

from flask import g, request, Response
from itsdangerous import JSONWebSignatureSerializer
from itsdangerous import TimedJSONWebSignatureSerializer
import simplejson as json


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        return f(*args, **kwargs)

    decorated.__wrapped_func = f

    return decorated


def require_features(features):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            lc = get_license(trial=True)
            available_features = lc.list_available_features()

            if not available_features.issuperset(features):
                raise forbidden_error("this operation is not permitted")

            return f(*args, **kwargs)

        return decorated

    return decorator


def json_response(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        response = view_func(*args, **kwargs)
        response_code = 200
        response_headers = dict()
        if isinstance(response, dict) or isinstance(response, list):
            response_body = json.dumps(response, indent=4)
        elif isinstance(response, tuple):
            if len(response) == 2:
                response_body, response_code = response
            else:
                response_body, response_code, response_headers = response

            response_body = json.dumps(response_body, indent=4)
        else:
            response_body = response

        return Response(response=response_body, status=response_code,
                        headers=response_headers, mimetype='application/json')

    return wrapper