# coding=utf-8
import logging

from flask import g, Flask
from flask_restful import reqparse

LOG = logging.getLogger(__name__)

app=Flask(__name__)

@app.api_route('/tenants', methods=['GET'])
@require_auth
@json_response
def list_tenants_api():
    user = g.user

    tenants = user.get_tenants()
    return [t._as_viewdict() for t in tenants], 200



