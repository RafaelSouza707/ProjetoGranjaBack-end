from flask_restful import Resource
from flask import request, g
from helpers.validate_schema import validate_schema
from helpers.database.db_utils import session_scope
from helpers.cache.cache import cache
from helpers.cache.clean_cache import CacheService
from middlewares.auth_middleware import token_required
from middlewares.permission_type import permissao_required

from services.usuarios.access_user_granja_service import ValidarAcessoGranja
from services.venda_estoque.producao_service import ProducaoService as Servico
from schemas.venda_estoque.producao_schema import ProducaoSchema as Schema

schema = Schema()
schemas = Schema(many=True)


def deletar_cache(granja_id, lote_frango_id):
    CacheService.deletar_cache_producao(granja_id, lote_frango_id)


class ProducaoResource(Resource):

    @token_required
    @permissao_required("ESTOQUE")
    def get(self):
        user_id = g.user_id

        granja_id = request.args.get("granja_id", type=int)
        lote_frango_id = request.args.get("lote_frango_id", type=int)
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)
        
        pagina = request.args.get("pagina", type=int)
        per_page = 10

        if lote_frango_id is not None:
            cache_key = f"cache:granja:{granja_id}:lote_frango:{lote_frango_id}:producao"
            dados = cache.get(cache_key)
            if dados is not None:
                return dados, 200
            
            paginacao = Servico.listar_do_lote_frango(lote_frango_id, pagina, per_page)
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
            }

            cache.set(cache_key, resultado)
            return resultado, 200

        cache_key = f"cache:granja:{granja_id}:producao"
        dados = cache.get(cache_key)
        if dados is not None:
            return dados, 200

        resultados = schemas.dump(Servico.listar(granja_id))
        
        cache.set(cache_key, resultados)
        return resultados, 200
    

    @token_required
    @permissao_required("ESTOQUE")
    def post(self):
        user_id = g.user_id
        granja_id = request.args.get("granja_id", type=int)
        lote_frango_id = request.args.get("lote_frango_id", type=int)
        
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        json = request.get_json()
        data, error = validate_schema(schema, json)

        if error:
            return {str(error)}


        with session_scope():
            novo = Servico.criar(data)
            resultado = schema.dump(novo)

        deletar_cache(granja_id, lote_frango_id)
        return resultado, 201


    @token_required
    @permissao_required("ESTOQUE")
    def put(self, id):
        user_id = g.user_id
        granja_id = request.args.get("granja_id", type=int)
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        lote_frango_id = request.args.get("lote_frango_id", type=int)

        json = request.get_json()
        data, error = validate_schema(schema, json, partial=True)

        if error:
            return str(error)


        with session_scope():
            atualizar = Servico.buscar_por_id(id)
            atualizado = Servico.atualizar(atualizar, data)
            resultado = schema.dump(atualizado)

        deletar_cache(granja_id, lote_frango_id)
        return resultado, 200
    

    @token_required
    @permissao_required("ESTOQUE")
    def delete(self, id):
        user_id = g.user_id
        granja_id = request.args.get("granja_id", type=int)

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)
        
        lote_frango_id = request.args.get("lote_frango_id", type=int)

        with session_scope():
            delete = Servico.buscar_por_id(id)
            Servico.deletar(delete)

        deletar_cache(granja_id, lote_frango_id)
        return "", 204