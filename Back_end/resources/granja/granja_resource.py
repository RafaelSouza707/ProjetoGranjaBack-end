from flask_restful import Resource
from flask import request, g
from helpers.validate_schema import validate_schema
from helpers.db_utils import session_scope
from middlewares.auth_middleware import token_required
from helpers.cache import cache

from services.granja.granja_service import GranjaService as Servico
from schemas.granja.granja_schema import GranjaSchema as Schema

schema = Schema()
schemas = Schema(many=True)


def deletar_cache(user_id):
    cache.delete(f"cache:user:{user_id}:granja")

class GranjaResource(Resource):

    @token_required
    def get(self):
        user_id = g.user_id

        print(user_id)

        #cache_key = f"cache:user:{user_id}:granja"
        #dados = cache.get(cache_key)
        #if dados is not None:
        #    print("Dados: ", dados)
        #    return dados, 200

        resultados = schemas.dump(Servico.listar(user_id))
        print("Resultados: ", resultados)
        #cache.set(
        #    cache_key,
        #    resultados
        #)
        return resultados, 200


    @token_required
    def post(self):
        user_id = g.user_id
        print(user_id)

        json = request.get_json()
        data, error = validate_schema(schema, json)

        print(data)

        if error:
            print(error)
            return str(error)
        
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
            return str(error)
        
        with session_scope():
            atualizar = Servico.buscar_por_id(id, user_id)
            atualizado = Servico.atualizar(atualizar, data)
            resultado = schema.dump(atualizado)
        
        deletar_cache(user_id)
        return resultado, 200
    

    @token_required
    def deletar(self, id):
        user_id = g.user_id

        with session_scope():
            delete = Servico.buscar_por_id(id, user_id)
            Servico.deletar(delete)

        deletar_cache(user_id)
        return "", 204