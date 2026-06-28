from flask_restful import Resource
from flask import request, g
from helpers.validate_schema import validate_schema
from helpers.db_utils import session_scope
from helpers.cache import cache
from middlewares.auth_middleware import token_required

from services.controle_banco_de_dados.cargos_service import CargoService as Servico
from schemas.controle_banco_de_dados.cargos_schema import CargosSchema as Schema

schema = Schema()
schemas = Schema(many=True)

def deletar_cache(user_id):
    cache.delete(f"cache:controle_bd:user:{user_id}:cargos")

class CargoResource(Resource):

    @token_required
    def get(self):
        user_id = g.user_id

        cache_key = f"cache:controle_bd:user:{user_id}:cargos"
        dados = cache.get(cache_key)
        if dados is not None:
            return dados, 200
        
        resultados = schemas.dump(Servico.listar(user_id))
        
        cache.set(
            cache_key,
            resultados
        )

        return resultados, 200


    @token_required
    def post(self):
        user_id = g.user_id

        json = request.get_json()
        data, error = validate_schema(schema, json)

        if error:
            return str(error)
        
        novo = Servico.criar(data)
        resultado = schema.dump(novo)
        
        deletar_cache(user_id)
        return resultado, 201
    

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
        
        return resultado, 200
    

    def delete(self, id):
        user_id = g.user_id

        with session_scope():
            delete = Servico.buscar_por_id(id, user_id)
            Servico.deletar(delete)

        deletar_cache(user_id)
        return "", 204