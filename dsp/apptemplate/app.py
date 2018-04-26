# -*- coding:utf-8 -*-
from flask import logging, request, json
from multiprocessing import Process

from dsp.apptemplate.template import getall, get, add
from dsp.apptemplate.templates.dao_2048.dao_2048_up import dao_2048
from dsp.utils.docker_stack import compose_up

log = logging.getLogger(__name__)

def apptemplate_routes(app):
    @app.route('/api/template/list',methods=['GET'])
    def get_template():
        return getall()
        #return ['dao_2048',]

    @app.route('/api/template/start', methods=['POST'])
    def start_up():
        data_json = request.get_json()
        name = data_json.get('name')
        template = get(name).encode('utf-8')
        tem_dir =  template.split(':')[1].split(',')[0]
        #temp = json.loads(template)
        #temp1 = temp.get('compose')
        print tem_dir
        compose_up(tem_dir)
        return "启动应用成功"

    @app.route('/api/template/start1', methods=['POST'])
    def start_up1():
        data_json = request.get_json()
        name = data_json.get('name')
        print name
        start_fun = eval(name)
        p = Process(target=start_fun)
        p.start()
        return '服务已经启动'

    @app.route('/master/dsp/apptemplate/add', methods=['POST'])
    def tmp_add():
        data_json = request.get_json()
        add(data_json)
        return '应用模板添加成功'

    @app.route('/master/dsp/apptemplate/getall', methods=['GET'])
    def tmp_getall():
        result = getall()
        return result

if __name__=='__main__':
    start_fun = eval('dao_2048')
    p = Process(target=start_fun)
    p.start()

