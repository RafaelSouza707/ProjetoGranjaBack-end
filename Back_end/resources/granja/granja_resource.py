from flask_restful import Resource
from flask import request, g
from helpers.validate_schema import validate_schema
from helpers.database.db_utils import session_scope
from middlewares.auth_middleware import token_required
from middlewares.permission_type import permissao_required
from helpers.cache.cache import cache
from helpers.cache.clean_cache import CacheService

from services.granja.granja_service import GranjaService as Servico
from schemas.granja.granja_schema import GranjaSchema as Schema

schema = Schema()
schemas = Schema(many=True)

def deletar_cache(user_id):
    CacheService.deletar_cache_granja(user_id)

class GranjaResource(Resource):

    @token_required
    def get(self):
        user_id = g.user_id
        
        cache_key = f"cache:user:{user_id}"
        dados = cache.get(cache_key)
        if dados is not None:
            return dados

        resultados = Servico.listar(user_id)

        resultado_final = [
            {
                **schema.dump(item["granja"]),
                "contexto": item["contexto"]
            }
            for item in resultados
        ]

        cache.set(cache_key, resultado_final)

        return resultado_final, 200


    @token_required
    def post(self):
        user_id = g.user_id

        json = request.get_json()
        data, error = validate_schema(schema, json)

        if error:
            return {str(error)}
        
        with session_scope():
            novo = Servico.criar(data, user_id)
            resultado = schema.dump(novo)
        
        deletar_cache(user_id)
        return resultado, 201
    

    @token_required
    def put(self, id):
        user_id = g.user_id

        json = request.get_json()
        data, error = validate_schema(schema, json, partial=True)

        if error:
            return {str(error)}
        
        with session_scope():
            atualizar = Servico.buscar_por_id(id)
            atualizado = Servico.atualizar(atualizar, data)
            resultado = schema.dump(atualizado)
        
        deletar_cache(user_id)
        return resultado, 200
    

    @token_required
    def delete(self, id):
        user_id = g.user_id

        with session_scope():
            delete = Servico.buscar_por_id(id)
            Servico.deletar(delete)

        deletar_cache(user_id)
        return "", 204