from flask import logging, request

from dsp.bigdata import service

log = logging.getLogger(__name__)

def bigdata_routes(app):
    @app.route('/api/data/init', methods=['POST'])
    def init_hadoop():
        data_json = request.get_json()
        number = data_json.get('slaves')
        service.hadoop_up('./docker-compose.yaml')