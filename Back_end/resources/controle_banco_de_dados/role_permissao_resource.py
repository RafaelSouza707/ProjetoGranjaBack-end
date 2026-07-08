from flask_restful import Resource
from flask import request
from helpers.validate_schema import validate_schema
from helpers.db_utils import session_scope

from services.controle_banco_de_dados.role_permissao_service import RolePermissaoService as Servico
from schemas.controle_banco_de_dados.role_permissao_schema import RolePermissaoSchema as Schema

schema = Schema()
schemas = Schema(many=True)

class RolePermissaoResource(Resource):

    def get(self):
        resultados = Servico.listar()
        resultados_final = schemas.dump(resultados)
        return resultados_final, 200


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