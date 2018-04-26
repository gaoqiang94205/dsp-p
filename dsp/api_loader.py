from flask_restful import Api, Resource

#from dsp.auth import load_config
from node.api import load_nodes
from settings import API_VERSION

class API(Resource):
    def get(self):
        return 'Hello API', 200, {'API-Version': API_VERSION}


def load_api(app):
    Api(app).add_resource(API, '/api')
    load_nodes(app)
#    load_config(apps)
