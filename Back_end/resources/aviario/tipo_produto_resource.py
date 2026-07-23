from flask_restful import Resource
from flask import request, g
from helpers.validate_schema import validate_schema
from helpers.database.db_utils import session_scope
from helpers.cache.cache import cache
from helpers.cache.clean_cache import CacheService
from middlewares.auth_middleware import token_required
from middlewares.permission_type import permissao_required

from services.aviario.tipo_produto_service import TipoProdutoService as Servico
from schemas.aviario.tipo_produto_schema import TipoProdutoSchema as Schema
from services.usuarios.access_user_granja_service import ValidarAcessoGranja

schema = Schema()
schemas = Schema(many=True)

def deletar_cache(granja_id):
    CacheService.limpar_cache_tipo_produto(granja_id)

class TipoProdutoResource(Resource):

    @token_required
    @permissao_required("AVIARIO")
    def get(self):
        user_id = g.user_id

        granja_id = request.args.get("granja_id", type=int)

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        cache_key = f"cache:granja:{granja_id}:tipo_produto"
        dados = cache.get(cache_key)
        if dados is not None:
            return dados, 200

        resultados = Servico.listar(granja_id)
        resultados_final = schemas.dump(resultados)

        cache.set(cache_key, resultados_final)
        return resultados_final, 200


    @token_required
    @permissao_required("AVIARIO")
    def post(self):
        user_id = g.user_id

        json = request.get_json()
        data, error = validate_schema(schema, json)

        if error:
            return str(error)

        granja_id = data.get("granja_id")

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            novo = Servico.criar(data)
            resultado = schema.dump(novo)

        deletar_cache(granja_id)
        return resultado, 201


    @token_required
    @permissao_required("AVIARIO")
    def put(self, id):
        user_id = g.user_id

        json = request.get_json()
        data, error = validate_schema(schema, json, partial=True)

        if error:
            return str(error)

        granja_id = data.get("granja_id")

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            atualizar = Servico.buscar_por_id(id)
            atualizado = Servico.atualizar(atualizar, data)
            resultado = schema.dump(atualizado)

        deletar_cache(granja_id)
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