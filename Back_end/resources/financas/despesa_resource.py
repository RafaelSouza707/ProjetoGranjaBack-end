from flask_restful import Resource
from flask import request, g
from helpers.validate_schema import validate_schema
from helpers.db_utils import session_scope
from helpers.cache import cache
from helpers.clean_cache import CacheService
from middlewares.auth_middleware import token_required

from services.financas.despesa_services import DespesaService
from schemas.financas.despesa_schema import DespesaSchema
from elastic.despesa_sync import indexar_despesa
from services.usuarios.access_user_granja_service import ValidarAcessoGranja

schema = DespesaSchema()
schemas = DespesaSchema(many=True)

def deletar_cache(granja_id):
    CacheService.limpar_cache_cards_gastos_granja(granja_id)
    CacheService.limpar_cache_cards_financas(granja_id)
    CacheService.limpar_cache_despesa_granja(granja_id)

class DespesaResource(Resource):

    @token_required
    def get(self):
        user_id = g.user_id
        
        granja_id = request.args.get("granja_id", type=int)

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        pagina = request.args.get("pagina", type=int)
        per_page = 20

        cache_key = f"cache:granja:{granja_id}:despesa:pagina:{pagina}"
        cache.delete(cache_key)
        dados = cache.get(cache_key)
        if dados is not None:
            return dados, 200

        paginacao = DespesaService.listar(granja_id, pagina, per_page)
        resultados = schemas.dump(paginacao.items)

        cache.set(cache_key, resultados)
        return {
            "dados": resultados,
            "pagination": {
                "page": paginacao.page,
                "per_page": paginacao.per_page,
                "total": paginacao.total,
                "pages": paginacao.pages,
                "has_next": paginacao.has_next,
                "has_prev": paginacao.has_prev
            }
        }, 200


    @token_required
    def post(self):
        user_id = g.user_id
        granja_id = request.args.get("granja_id", type=int)

        json = request.get_json()
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