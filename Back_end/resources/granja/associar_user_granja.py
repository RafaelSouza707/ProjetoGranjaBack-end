from flask_restful import Resource
from flask import request, g
from helpers.database.db_utils import session_scope
from middlewares.auth_middleware import token_required
from middlewares.permission_type import permissao_required
from services.usuarios.access_user_granja_service import ValidarAcessoGranja

from services.granja.granja_service import GranjaService
from schemas.granja.granja_schema import GranjaSchema

schema = GranjaSchema()

class AssociarUserGranjaResource(Resource):

    @token_required
    @permissao_required("MOVER_USUARIOS")
    def post(self):
        user_id = g.user_id

        json = request.get_json()

        granja_id = request.args.get("granja_id", type=int)

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        user_associado_id = json.get("user_associado_id")
        tipo_user = json.get("tipo_user")
        with session_scope():
            resultado = GranjaService.associar_granja(user_associado_id, granja_id, tipo_user)
            resultado_final = schema.dump(resultado)

        return resultado_final, 201
    

    @token_required
    @permissao_required("MOVER_USUARIOS")
    def delete(self, id):
        user_id = g.user_id
        granja_id = request.args.get("granja_id", type=int)
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            GranjaService.desassociar_granja(id, granja_id)
        
        return "", 201