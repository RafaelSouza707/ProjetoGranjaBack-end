from flask_restful import Resource
from flask import request
from helpers.validate_schema import validate_schema
from helpers.db_utils import session_scope

from services.financas.tipo_despesa_services import TipoDespesaService as Tipo
from schemas.financas.tipo_despesa_schema import TipoDespesaSchema

tipo_schema = TipoDespesaSchema()
tipos_schema = TipoDespesaSchema(many=True)

class TipoDespesaResource(Resource):

    def get(self, id=None):
        if id:
            with session_scope():
                resultado = Tipo.buscar_por_id(id)
            return tipo_schema.dump(resultado), 200
        with session_scope():
            resultados = Tipo.listar()
            return tipos_schema.dump(resultados), 200


    def post(self):
        json = request.get_json()
        
        data, error = validate_schema(tipo_schema, json)

        if error:
            return str(error)
        
        with session_scope():
            tipo = Tipo.criar(data)
            resultado = tipo_schema.dump(tipo)
        
        return resultado, 201
    

    def put(self, id):
        json = request.get_json()

        data, error = validate_schema(tipo_schema, json, partial=True)

        if error:
            return str(error)
        
        with session_scope():
            tipo = Tipo.buscar_por_id(id)
            atualizar = Tipo.atualizar(tipo, data)
            resultado = tipo_schema.dump(atualizar)
        
        return resultado, 200
    

    def delete(self, id):
        with session_scope():
            tipo = Tipo.buscar_por_id(id)
            Tipo.deletar(tipo)

        return "", 204