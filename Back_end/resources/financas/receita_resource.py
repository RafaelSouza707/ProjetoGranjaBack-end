from flask_restful import Resource
from flask import request, g
from helpers.validate_schema import validate_schema
from helpers.database.db_utils import session_scope
from middlewares.auth_middleware import token_required
from middlewares.permission_type import permissao_required
from middlewares.permission_type import permissao_required
from helpers.cache.cache import cache
from helpers.cache.clean_cache import CacheService

from services.financas.receita_service import ReceitaService
from schemas.financas.receita_schema import ReceitaSchema as Schema
from services.usuarios.access_user_granja_service import ValidarAcessoGranja

schema = Schema()
schemas = Schema(many=True)

def deletar_cache(granja_id):
    CacheService.limpar_cache_receita(granja_id)
    CacheService.limpar_cache_cards_receita_granja(granja_id)
    CacheService.limpar_cache_cards_financas(granja_id)

class ReceitaResource(Resource):

    @token_required
    @permissao_required("FINANCAS")
    def get(self):
        user_id = g.user_id

        granja_id = request.args.get("granja_id", type=int)

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        pagina = request.args.get("pagina", type=int)
        per_page = 10

        cache_key = f"cache:granja:{granja_id}:receita:pagina:{pagina}"
        dados = cache.get(cache_key)
        if dados is not None:
            return dados, 200
        
        paginacao = ReceitaService.listar(granja_id, pagina, per_page)
        resultados = schemas.dump(paginacao.items)

        resultado = {
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

        cache.set(cache_key, resultado)
        return resultado, 200

    @token_required
    @permissao_required("FINANCAS")
    def post(self):
        user_id = g.user_id

        json = request.get_json()
        data, error = validate_schema(schema, json)

        if error:
            return {str(error)}

        granja_id = data.get("granja_id")
        if granja_id is None:
            return {"error": "granja_id é obrigatório"}, 400

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            novo = ReceitaService.criar(data)
            resultado = schema.dump(novo)

        CacheService.limpar_cache_receitas(granja_id)
        return resultado, 201


    @token_required
    @permissao_required("FINANCAS")
    def put(self, id):
        user_id = g.user_id

        json = request.get_json()
        json.pop("tipo_receita", None)
        json.pop("venda", None)
        json.pop("id", None)
        json.pop("created_at", None)
        json.pop("updated_at", None)
        json.pop("status", None)
        data, error = validate_schema(schema, json, partial=True)

        if error:
            return {str(error)}

        granja_id = data.get("granja_id")

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            atualizar = ReceitaService.buscar_por_id(id)
            atualizado = ReceitaService.atualizar(atualizar, data)
            resultado = schema.dump(atualizado)

        CacheService.limpar_cache_receitas(granja_id)
        return resultado, 200


    @token_required
    @permissao_required("FINANCAS")
    def delete(self, id):
        user_id = g.user_id
        granja_id = request.args.get("granja_id", type=int)

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            delete = ReceitaService.buscar_por_id(id)
            ReceitaService.deletar(delete)

        CacheService.limpar_cache_receitas(granja_id)
        return "", 204