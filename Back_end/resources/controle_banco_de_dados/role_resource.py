from flask_restful import Resource
from flask import request
from helpers.validate_schema import validate_schema
from helpers.db_utils import session_scope

from services.controle_banco_de_dados.role_service import RoleService as Servico
from schemas.controle_banco_de_dados.role_schema import RoleSchema as Schema

schema = Schema()
schemas = Schema(many=True)

class RoleResource(Resource):

    def get(self):
        resultados = schemas.dump(Servico.listar())
        return resultados, 200


    def post(self):
        json = request.get_json()
        
        data, error = validate_schema(schema, json)

        if error:
            return {str(error)}
        
        with session_scope():
            novo = Servico.criar(data)
            resultado = schema.dump(novo)
        
        return resultado, 201
    

    def put(self, id):
        json = request.get_json()

        data, error = validate_schema(schema, json, partial=True)

        if error:
            return {str(error)}
        
        with session_scope():
            atualizar = Servico.buscar_por_id(id)
            atualizado = Servico.atualizar(atualizar, data)
            resultado = schema.dump(atualizado)
        
        return resultado, 200
    

    def delete(self, id):
        with session_scope():
            delete = Servico.buscar_por_id(id)
            Servico.deletar(delete)

        return "", 204