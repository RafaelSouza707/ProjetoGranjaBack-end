from flask_restful import Resource
from flask import request, g
from helpers.validate_schema import validate_schema
from helpers.database.db_utils import session_scope
from helpers.cache.cache import cache
from helpers.cache.clean_cache import CacheService
from middlewares.auth_middleware import token_required
from middlewares.permission_type import permissao_required

from services.aviario.mortalidade_service import MortalidadeService as Servico
from schemas.aviario.mortalidade_schema import MortalidadeSchema as Schema
from services.usuarios.access_user_granja_service import ValidarAcessoGranja

schema = Schema()
schemas = Schema(many=True)

def deletar_cache(granja_id, lote_frango_id=None):
    CacheService.deletar_cache_mortalidade(granja_id, lote_frango_id)
    CacheService.deletar_cache_cards_granja(granja_id)
    CacheService.deletar_cache_card_mortalidade_granja(granja_id)
    CacheService.limpar_cache_cards_lote_frango(granja_id)

class MortalidadeResource(Resource):

    @token_required
    @permissao_required("AVIARIO")
    def get(self):
        user_id = g.user_id

        granja_id = request.args.get("granja_id", type=int)
        lote_frango_id = request.args.get("lote_frango_id", type=int)

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        pagina = request.args.get("pagina", type=int)
        per_page = 10

        if lote_frango_id is not None:
            cache_key = f"cache:granja:{granja_id}:lote_frango:{lote_frango_id}:mortalidade"
            cache.delete(cache_key)
            dados = cache.get(cache_key)
            if dados is not None:
                return dados, 200

            paginacao = Servico.listar_de_lote_frango(lote_frango_id, pagina, per_page)
            resultados = schemas.dump(paginacao.items)
            
            resultado_final = {
                "dados": resultados,
                "pagination": {
                    "page": paginacao.page,
                    "per_page": paginacao.per_page,
                    "total": paginacao.total,
                    "pages": paginacao.pages,
                    "has_next": paginacao.has_next,
                    "has_prev": paginacao.has_prev
                }
            }

            cache.set(cache_key, resultado_final)
            
            return resultado_final, 200

        cache_key = f"cache:granja:{granja_id}:mortalidade"
        dados = cache.get(cache_key)
        if dados is not None:
            return dados, 200

        paginacao = Servico.listar(granja_id, pagina, per_page)
        resultados = schemas.dump(paginacao.items)

        cache.set(cache_key, resultados, timeout=300)
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
    @permissao_required("AVIARIO")
    def post(self):
        user_id = g.user_id
        granja_id = request.args.get("granja_id", type=int)
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        json = request.get_json()
        data, error = validate_schema(schema, json)

        print(json)

        if error:
            return {str(error)}

        lote_frango_id = data.get("lote_frango_id")

        with session_scope():
            novo = Servico.criar(data)
            resultado = schema.dump(novo)

        deletar_cache(granja_id, lote_frango_id)
        return resultado, 201
    

    @token_required
    @permissao_required("AVIARIO")
    def put(self, id):
        user_id = g.user_id

        json = request.get_json()
        data, error = validate_schema(schema, json, partial=True)

        if error:
            return {str(error)}

        lote_frango_id = data["lote_frango_id"]

        granja_id = request.args.get("granja_id", type=int)
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            atualizar = Servico.buscar_por_id(id)
            atualizado = Servico.atualizar(atualizar, data)
            resultado = schema.dump(atualizado)

        deletar_cache(granja_id, lote_frango_id)
        return resultado, 200


    @token_required
    @permissao_required("AVIARIO")
    def delete(self, id):
        user_id = g.user_id

        granja_id = request.args.get("granja_id", type=int)
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            delete = Servico.buscar_por_id(id)
            Servico.deletar(delete) 

        deletar_cache(granja_id)
        return "", 204