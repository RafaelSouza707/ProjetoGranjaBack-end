from flask_restful import Resource
from flask import request, g
from helpers.validate_schema import validate_schema
from helpers.database.db_utils import session_scope
from middlewares.auth_middleware import token_required
from services.usuarios.access_user_granja_service import ValidarAcessoGranja
from helpers.cache.cache import cache
from helpers.cache.clean_cache import CacheService
from middlewares.permission_type import permissao_required

from services.venda_estoque.tipo_unidade_medida_service import TipoUnidadeMedidaService as Servico
from schemas.venda_estoque.tipo_unidade_medida_schema import TipoUnidadeMedidaSchema as Schema
from services.usuarios.access_user_granja_service import ValidarAcessoGranja

schema = Schema()
schemas = Schema(many=True)

def deletar_cache(granja_id):
    CacheService.deletar_cache_tipo_unidade_medida(granja_id)

class TipoUnidadeMedidaResource(Resource):

    @token_required
    @permissao_required("ESTOQUE")
    def get(self, id=None):
        user_id = g.user_id
        granja_id = request.args.get("granja_id", type=int)
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        cache_key = f"cache:granja:{granja_id}:tipo_unidade_medida"
        dados = cache.get(cache_key)
        if dados is not None:
            return dados, 200
        
        resultados = schemas.dump(Servico.listar(granja_id))
        
        cache.set(
            cache_key,
            resultados
        )
        return resultados, 200


    @token_required
    @permissao_required("ESTOQUE")
    def post(self):
        user_id = g.user_id

        json = request.get_json()
        data, error = validate_schema(schema, json)
        if error:
            return str(error)
        
        granja_id = data["granja_id"]
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            novo = Servico.criar(data)
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
        
        granja_id = data.get("granja_id")
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
        granja_id = request.args.get("graja_id", type=int)
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            delete = Servico.buscar_por_id(id)
            Servico.deletar(delete)

        deletar_cache(granja_id)
        return "", 204