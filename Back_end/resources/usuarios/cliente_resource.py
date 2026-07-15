from flask_restful import Resource
from flask import request, g
from helpers.validate_schema import validate_schema
from helpers.db_utils import session_scope
from helpers.cache import cache
from helpers.clean_cache import CacheService
from middlewares.auth_middleware import token_required
from services.usuarios.access_user_granja_service import ValidarAcessoGranja

from services.usuarios.cliente_service import ClienteService as Servico
from schemas.usuarios.cliente_schema import ClienteSchema as Schema

schema = Schema()
schemas = Schema(many=True)

def deletar_cache(granja_id):
    CacheService.deletar_cache_cliente(granja_id)

class ClienteResource(Resource):

    @token_required
    def get(self):
        user_id = g.user_id
        granja_id = request.args.get("granja_id", type=int)
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        cache_key = f"cache:user:granja:{granja_id}:cliente"
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
        print(error)

        if error:
            return {str(error)}
        
        granja_id = data["granja_id"]
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)
        
        with session_scope():
            novo = Servico.criar(data)
            resultado = schema.dump(novo)
        

        deletar_cache(granja_id)
        return resultado, 201
    

    @token_required
    def put(self, id):
        user_id = g.user_id

        json = request.get_json()
        data, error = validate_schema(schema, json, partial=True)

        if error:
            return {str(error)}
        
        granja_id = granja_id = data["granja_id"]
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)
        
        with session_scope():
            atualizar = Servico.buscar_por_id(id)
            atualizado = Servico.atualizar(atualizar, data)
            resultado = schema.dump(atualizado)
        
        deletar_cache(granja_id)
        return resultado, 200
    

    @token_required
    def delete(self, id):
        user_id = g.user_id
        granja_id = request.args.get("granja_id", type=int)
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            delete = Servico.buscar_por_id(id)
            Servico.deletar(delete)

        deletar_cache(granja_id)
        return "", 204

