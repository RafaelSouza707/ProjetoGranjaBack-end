from flask_restful import Resource
from flask import request
from helpers.validate_schema import validate_schema
from helpers.database.db_utils import session_scope

from services.granja.usuario_granja_service import UsuarioGranjaService as Servico
from schemas.granja.usuario_granja_schema import UsuarioGranjaSchema as Schema

schema = Schema()
schemas = Schema(many=True)

class UsuarioGranjaResource(Resource):

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