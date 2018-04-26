# -*- coding:utf-8 -*-
from flask import logging, request, json
from dsp.network import service

log = logging.getLogger(__name__)

def network_routes(app):
    @app.route('/api/net/list',methods=['GET'])
    def get_nets():
        result = service.get_net()
        return result
