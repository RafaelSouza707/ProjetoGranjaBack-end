from flask_restful import Resource
from flask import request, jsonify
from middlewares.auth_middleware import token_required

from services.usuarios.usuario_service import UsuarioService 

class LoginResource(Resource):

    def post(self):
        data = request.get_json()
        
        result = UsuarioService.login(
            data["email"],
            data["senha"]
        )

        resp = jsonify(result)
        resp.set_cookie(
            "granja_access_token",
            result["token"],
            httponly=True,
            samesite="Lax",
            max_age=60 * 60 * 12
        )

        return resp
    


    @token_required
    def get(self):
        return {
            "id": request.user["user_id"],
            "nome": request.user["username"]
        }, 200