# -*- coding:utf-8 -*-
from flask import logging, request, json

from dsp.apps import service
from dsp.apps.service import run_service
import dsp.apps.service

log = logging.getLogger(__name__)

def application_routes(app):
    @app.route('/api/app/create',methods=['POST'])
    def run_app():
        data_json = request.get_json()
        name = data_json.get('service_name')
        print name
        image = data_json.get('image')
        command = data_json.get('command')
        restart = data_json.get('restart','none') #none, on-failure, or any (string)
        networks = data_json.get('networks',{})#network name or id
        mode = data_json.get('mode','global') #单机的或全局的 replicated or global(string)
        source2target = data_json.get('source2target',[]) #挂载点，可以是主机的路径或volume name list-->(string)

        try:#对字符串转换的时候可能会出现错误
            rep = data_json.get('replicas') #容器的运行个数 int
            replicas = int(rep)
        except:
            replicas = 1
        ports_origin = data_json.get('ports') #服务暴露的端口
        pps = ports_origin.split(",")
        global port
        print pps
        for por in pps:
            pors = por.split(':')
            if len(pors) == 2:
                port = {}
                port[int(pors[0])]=int(pors[1])
            else:
                port = None
        print port
        map_dict = run_service(service_name=name,image_name=image, command=command,
                               restart_condition=restart, networks=networks,
                               s_and_t=source2target, mode=mode, replicas=replicas, ports=port)
        return json.dumps(map_dict)

    @app.route('/api/apps/list',methods=['GET'])
    def get_apps():
        results = service.get_apps()
        return json.dumps(results)

    @app.route('/api/apps/delete', methods=['post'])
    def rm_app():
        data_json = request.get_json()
        apps = data_json.get("apps")
        print apps
        result = service.rm_app(apps)
        return json.dumps(result)

    @app.route('/api/apps/access', methods=['GET'])
    def access_ip():
        result = service.get_access_ip()
        return json.dumps(result)

    @app.route('/undefined/api/user/login', methods=['POST'])
    def user_login():
        data_json = request.get_json()
        name_pwd = {"admin":"admin","test":"test","gaoqiang":"root"}
        name = data_json.get("name")
        pwd = data_json.get("pwd")
        result = False
        if name in name_pwd.keys():
            if pwd == name_pwd[name]:
                result = True

        return json.dumps(result)

    @app.route('/api/user/login', methods=['POST'])
    def user_login1():
        data_json = request.get_json()
        name_pwd = {"admin": "admin", "test": "test", "gaoqiang": "root"}
        name = data_json.get("name")
        pwd = data_json.get("pwd")
        result = False
        if name in name_pwd.keys():
            if pwd == name_pwd[name]:
                result = True

        return json.dumps(result)

if __name__=='__main__':
    ports_origin = "123:456,223:456"
    pps = ports_origin.split(",")
    port = {}
    for por in pps:
        pors = por.split(':')
        print len(pors)
        port[int(pors[0])] = int(pors[1])
    print port