from flask_restful import Api, Resource

def load_auth(app):
    api = Api(app)
    api.add_resource(MyAccountAPI,"/api/auth/my-account")

class MyAccountAPI(Resource):
    def get(self):
        return True
    def post(self):
        pass
    def delete(self):
        pass
    def put(self):
        pass