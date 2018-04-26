# -*- coding:utf-8 -*-
from flask import logging, request, json
from dsp.image import service

log = logging.getLogger(__name__)

def image_routes(app):
    @app.route('/api/images/list',methods=['GET'])
    def get_images():
        result = service.getall()
        return result

    @app.route('/api/images/delete',methods=['POST'])
    def delete_image():
        data_json = request.get_json()
        image_name = data_json.get("imagename")

        global name
        global tag
        if image_name.find(':') ==-1:
            name = image_name
            tag = 'latest'
        else:
            name = image_name.split(':')[0]
            tag = image_name.split(':')[1]
        print name, tag
        result = service.delete(name,tag)
        return json.dumps(result)
