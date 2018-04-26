from flask import logging, request, json

from dsp.container import service

log = logging.getLogger(__name__)

def container_routes(app):

    @app.route('/api/container/create',methods=['POST'])
    def run_container():
        data_json = request.get_json()
        image = data_json.get('image')
        command = data_json.get('command')
        exports = data_json.get('exports')
        map_dict = service.run_container(image, command,expose_port=exports)
        return json.dumps(map_dict)

    @app.route('/api/container/list',methods=['GET'])
    def get_containers():
        results = service.get_containers()
        return json.dumps(results)

    @app.route('/api/container/delete', methods=['post'])
    def rm_container():
        data_json = request.get_json()
        containers = data_json.get("list")
        force = data_json.get("force")
        volume = data_json.get("volume")

        if force=="True":
            force = True
        else:
            force = False

        if volume == "True":
            volume = True
        else:
            volume = False
        print containers
        result = service.rm_container(containers,volume,link=False,force=force)
        return json.dumps(result)