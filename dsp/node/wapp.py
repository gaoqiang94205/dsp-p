import json
import logging

from flask import request

from dsp.node.service import join_swarm

log = logging.getLogger(__name__)
def node_routes(app):
    @app.route('/master/api/v1/nodes',methods=['PUT'])
    def join_node():
        data_json = request.get_json()
        node_ip = data_json.get('node_ip')
        node_port = data_json.get('node_port')
        result = join_swarm(ip=node_ip, port=node_port)
        return json.dumps(result)