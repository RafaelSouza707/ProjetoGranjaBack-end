from flask_restful import Resource
from flask import make_response

class LogoutResource(Resource):

    def post(self):
        response = make_response({
            "message": "Logout realizado com sucesso"
        })

        response.delete_cookie(
            "granja_access_token",
            httponly=True,
            samesite="Lax"
        )

        return response