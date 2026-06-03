from flask_restful import Resource
from flask import request
from helpers.validate_schema import validate_schema
from helpers.db_utils import session_scope

from services.financas.despesa_services import DespesaService
from schemas.financas.despesa_schema import DespesaSchema

despesa_schema = DespesaSchema()
despesas_schema = DespesaSchema(many=True)

class DespesaResource(Resource):

    def get(self, id=None):
        if id:
            with session_scope():
                resultado = DespesaService.buscar_por_id(id)
            return despesa_schema.dump(resultado), 200
        
        with session_scope():
            resultados = DespesaService.listar()
            return despesas_schema.dump(resultados), 200
    

    def post(self):
        json = request.get_json()
        data, error = validate_schema(despesa_schema, json)

        if error:
            return str(error)
        
        with session_scope():
            despesa = DespesaService.criar(data)
            resultado = despesa_schema.dump(despesa)

        return resultado, 201
    

    def put(self, id):
        json = request.get_json()
        data, error = validate_schema(despesa_schema, json, partial=True)

        if error:
            return str(error)
        
        with session_scope():
            despesa = DespesaService.buscar_por_id(id)
            atualizar = DespesaService.atualizar(despesa, data)
            resultado = despesa_schema.dump(atualizar)

        return resultado, 200
    

    def delete(self, id):
        with session_scope():
            despesa = DespesaService.buscar_por_id(id)
            DespesaService.delete(despesa)
        
        return "", 204