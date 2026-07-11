from flask_restful import Resource
from flask import request, g
from helpers.validate_schema import validate_schema
from helpers.db_utils import session_scope
from middlewares.auth_middleware import token_required
from helpers.cache import cache
from services.usuarios.access_user_granja_service import ValidarAcessoGranja

from services.granja.granja_service import GranjaService
from schemas.granja.granja_schema import GranjaSchema

schema = GranjaSchema()

class AssociarUserGranjaResource(Resource):

    @token_required
    def post(self):
        user_id = g.user_id

        json = request.get_json()

        granja_id = json.get("granja_id")

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        user_associar_id = json.get("user_asssociar_id")
        tipo_user = json.get("tipo_user")
        with session_scope():
            resultado = GranjaService.associar_granja(user_associar_id, granja_id, tipo_user)
            resultado_final = schema.dump(resultado)

        return resultado_final, 201