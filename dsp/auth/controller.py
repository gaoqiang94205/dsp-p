from flask_restful import Api, Resource, reqparse

from dsp.api_loader import API


def load_config(app):
    api = API(app)
    api.add_resource(AccessKeyAPI,'/api/config/access-key')

class AccessKeyAPI(Resource):
    @require_admin
    def get(self):
        return AccessKey.load()._asdict()

    @require_admin
    def post(self):
        args = reqparse.RequestParser() \
            .add_argument('access_key', required=True) \
            .add_argument('secret_key', required=True) \
            .parse_args()
        return set_access_key(args)