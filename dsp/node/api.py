# -*- coding:utf-8 -*-

import json

from flask import request
from flask_restful import Api, Resource, reqparse

from service import get_nodes, join_swarm, leave_swarm, init_swarm

def load_nodes(app):
    api = Api(app)
    api.add_resource(NodeResource,"/api/v1/nodes")

class NodeResource(Resource):
  def get(self):
      nodes = get_nodes()
      jstr = json.dumps(nodes)
      return jstr

  #初始化集群
  def post(self):
      # args = reqparse.RequestParser() \
      # .add_argument('node_ip', required=True) \
      # .add_argument('node_port', required=True) \
      # .add_argument('swarm_spec',required=True) \
      # .parse_args()
      #
      data_json = request.get_json()
      swarm_spec = data_json.get('swarm_spec')
      print swarm_spec
      node_ip = data_json.get("node_ip")
      node_port = data_json.get("node_port")
      base_url = "http://" + node_ip + ":" + node_port
      print base_url
      init_swarm(base_url=base_url,swarm_spec={})
      return 'success'
  #加入集群
  def put(self):
      data_json = request.get_json()
      node_ip=data_json.get('node_ip')
      node_port=data_json.get('node_port')
      join_swarm(node_ip, node_port)
      return 'success'

#离开swarm集群
  def delete(selfself):
      node_ip=request.args.get('node_ip')
      node_port=request.args.get('node_port')
      force=request.args.get('force')
      if force=='True':
          force = True
      result = leave_swarm(node_ip=node_ip,node_port=node_port, force=True)
      if result:
        return '成功移除节点'
      return "移除失败，可能需要手动移除：docker swarm leave --force"
if __name__=="__main__":
    #print InvalidUsage('error',404,{'aa':'bb'}).to_dict()
    #join_swarm()
    pass