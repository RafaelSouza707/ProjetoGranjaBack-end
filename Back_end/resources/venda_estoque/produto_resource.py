from flask_restful import Resource
from flask import request, g
from helpers.validate_schema import validate_schema
from helpers.database.db_utils import session_scope
from helpers.cache.cache import cache
from helpers.cache.clean_cache import CacheService
from middlewares.auth_middleware import token_required
from middlewares.permission_type import permissao_required

from services.usuarios.access_user_granja_service import ValidarAcessoGranja
from services.venda_estoque.produto_service import ProdutoService as Servico
from schemas.venda_estoque.produto_schema import ProdutoSchema as Schema

schema = Schema()
schemas = Schema(many=True)

def deletar_cache(granja_id, pagina=None):
    CacheService.deletar_cache_produto(granja_id, pagina)

class ProdutoResource(Resource):

    @token_required
    @permissao_required("ESTOQUE")
    def get(self):
        user_id = g.user_id
        granja_id = request.args.get("granja_id", type=int)
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        pagina = request.args.get("pagina", type=int)
        per_page = 10

        if pagina == -1:
            cache_key = f"cache:granja:{granja_id}:produto"
            dados = cache.get(cache_key)
            if dados is not None:
                return dados, 200
            
            resultados = schemas.dump(Servico.listar(granja_id))
            resposta_json= {
                "dados": resultados,
                "pagination": None
            }
            cache.set(cache_key, resposta_json)
            return resposta_json, 200

        cache_key = f"cache:granja:{granja_id}:produto:pagina:{pagina}"
        dados = cache.get(cache_key)
        if dados is not None:
            return dados, 200

        paginacao = Servico.listar_paginado(granja_id, pagina, per_page)
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


    @token_required
    @permissao_required("ESTOQUE")
    def post(self):
        user_id = g.user_id

        json = request.get_json()
        data, error = validate_schema(schema, json)

        if error:
            return str(error)

        granja_id = data.get("granja_id")

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            novo = Servico.criar(data, granja_id)
            resultado = schema.dump(novo)

        deletar_cache(granja_id)
        return resultado, 201


    @token_required
    @permissao_required("ESTOQUE")
    def put(self, id):
        user_id = g.user_id

        json = request.get_json()
        data, error = validate_schema(schema, json, partial=True)

        if error:
            return str(error)

        granja_id = data["granja_id"]

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            atualizar = Servico.buscar_por_id(id)
            atualizado = Servico.atualizar(atualizar, data)
            resultado = schema.dump(atualizado)

        deletar_cache(granja_id)
        return resultado, 200


    @token_required
    @permissao_required("ESTOQUE")
    def delete(self, id):
        user_id = g.user_id
        granja_id = request.args.get("granja_id")
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            delete = Servico.buscar_por_id(id)
            Servico.deletar(delete)

        deletar_cache(granja_id)
        return "", 204