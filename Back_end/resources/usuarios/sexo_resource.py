from flask_restful import Resource
from flask import request
from helpers.cache import cache
from helpers.clean_cache import CacheService
from helpers.validate_schema import validate_schema
from helpers.db_utils import session_scope

from services.usuarios.sexo_service import SexoService as Servico
from schemas.usuarios.sexo_schema import SexoSchema as Schema

schema = Schema()
schemas = Schema(many=True)

def deletar_cache():
    CacheService.deletar_cache_sexo()

class SexoResource(Resource):

    def get(self):
        cache_key = f"cache:sexo"
        dados = cache.get(cache_key)
        if dados is not None:
            return dados, 200
        
        resultados = schemas.dump(Servico.listar())

        cache.set(cache_key, resultados)
        return resultados, 200


    def post(self):
        json = request.get_json()
        
        data, error = validate_schema(schema, json)

        if error:
            return {str(error)}
        
        with session_scope():
            novo = Servico.criar(data)
            resultado = schema.dump(novo)
        
        deletar_cache()
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
        
        deletar_cache()
        return resultado, 200
    

    def delete(self, id):
        with session_scope():
            delete = Servico.buscar_por_id(id)
            Servico.deletar(delete)

        deletar_cache()
        return "", 204