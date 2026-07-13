from flask_restful import Resource
from flask import request, g
from helpers.validate_schema import validate_schema
from helpers.db_utils import session_scope
from helpers.cache import cache
from middlewares.auth_middleware import token_required

from services.financas.despesa_services import DespesaService
from schemas.financas.despesa_schema import DespesaSchema
from elastic.despesa_sync import indexar_despesa
from services.usuarios.access_user_granja_service import ValidarAcessoGranja

schema = DespesaSchema()
schemas = DespesaSchema(many=True)

def deletar_cache(granja_id):
    cache.delete(f"cache:granja:{granja_id}:despesa")
    cache.delete(f"cache:granja:{granja_id}:despesa:cards_gastos")
    cache.delete(f"cache:granja:{granja_id}:despesa:cards_financas")

class DespesaResource(Resource):

    @token_required
    def get(self):
        user_id = g.user_id
        
        granja_id = request.args.get("granja_id", type=int)

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        cache_key = f"cache:granja:{granja_id}:despesa"
        cache.delete(cache_key)
        dados = cache.get(cache_key)
        if dados is not None:
            return dados, 200

        resultados = schemas.dump(DespesaService.listar(granja_id))

        cache.set(cache_key, resultados)
        return resultados, 200


    @token_required
    def post(self):
        user_id = g.user_id
        granja_id = request.args.get("granja_id", type=int)

        json = request.get_json()
        print(json)
        data, error = validate_schema(schema, json)

        if error:
            return {str(error)}
        

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            despesa = DespesaService.criar(data)
            indexar_despesa(despesa)
            resultado = schema.dump(despesa)

        deletar_cache(granja_id)
        return resultado, 201
    

    @token_required
    def put(self, id):
        user_id = g.user_id

        json = request.get_json()
        data, error = validate_schema(schema, json, partial=True)


        if error:
            return {str(error)}
        
        granja_id = data["granja_id"]

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            despesa = DespesaService.buscar_por_id(id)
            atualizar = DespesaService.atualizar(despesa, data)
            resultado = schema.dump(atualizar)

        deletar_cache(granja_id)
        return resultado, 200
    
    
    @token_required
    def delete(self, id):
        user_id = g.user_id

        granja_id = request.args.get("granja_id", type=int)

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            despesa = DespesaService.buscar_por_id(id)
            DespesaService.deletar(despesa)

        deletar_cache(granja_id)
        return "", 204