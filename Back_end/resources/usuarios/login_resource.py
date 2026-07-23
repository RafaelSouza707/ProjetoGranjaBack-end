from flask_restful import Resource
from flask import request, jsonify, g
from middlewares.auth_middleware import token_required
from middlewares.permission_type import permissao_required

from services.usuarios.usuario_service import UsuarioService
from schemas.usuarios.usuario_schema import UsuarioSchema

schema = UsuarioSchema()

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
        user_id = g.user_id

        usuario = UsuarioService.buscar_por_id(user_id)

        return schema.dump(usuario), 200