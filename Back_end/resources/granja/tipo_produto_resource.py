from flask_restful import Resource
from flask import request
from helpers.validate_schema import validate_schema
from helpers.db_utils import session_scope

from services.granja.tipo_produto_service import TipoProdutoService as Servico
from schemas.granja.tipo_produto_schema import TipoProdutoSchema as Schema

schema = Schema()
schemas = Schema(many=True)

class TipoProdutoResource(Resource):

    def get(self, id=None):
        if id:
            with session_scope():
                resultado = Servico.buscar_por_id(id)
                resultado_final = schema.dump(resultado)
            return resultado_final, 200
        with session_scope():
            resultados = Servico.listar()
            resultados_final = schemas.dump(resultados)
        return resultados_final, 200


    def post(self):
        json = request.get_json()
        
        data, error = validate_schema(schema, json)

        if error:
            return str(error)
        
        with session_scope():
            novo = Servico.criar(data)
            resultado = schema.dump(novo)
        
        return resultado, 201
    

    def put(self, id):
        json = request.get_json()

        data, error = validate_schema(schema, json, partial=True)

        if error:
            return str(error)
        
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