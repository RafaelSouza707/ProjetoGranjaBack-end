from flask_restful import Resource

class HomeResources(Resource):
    def get(self):
        return {"version": "1.1"}, 200