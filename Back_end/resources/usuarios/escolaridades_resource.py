from flask_restful import Resource
from flask import request, g
from helpers.validate_schema import validate_schema
from helpers.db_utils import session_scope
from middlewares.auth_middleware import token_required

from services.usuarios.escolaridades_service import EscolaridadesService as Servico
from schemas.usuarios.escolaridades_schema import EscolaridadesSchema as Schema

schema = Schema()
schemas = Schema(many=True)

class EscolaridadesResource(Resource):

    @token_required
    def get(self):
        user_id = g.user_id

        resultados = schemas.dump(Servico.listar(user_id))

        return resultados, 200


    @token_required
    def post(self):
        json = request.get_json()
        data, error = validate_schema(schema, json)

        if error:
            return str(error)
        
        with session_scope():
            novo = Servico.criar(data)
            resultado = schema.dump(novo)
        
        return resultado, 201
    

    @token_required
    def put(self, id):
        json = request.get_json()
        data, error = validate_schema(schema, json, partial=True)

        if error:
            return str(error)
        
        with session_scope():
            atualizar = Servico.buscar_por_id(id, g.user_id)
            atualizado = Servico.atualizar(atualizar, data)
            resultado = schema.dump(atualizado)
        
        return resultado, 200
    

    @token_required
    def delete(self, id):
        with session_scope():
            delete = Servico.buscar_por_id(id, g.user_id)
            Servico.deletar(delete)

        return "", 204