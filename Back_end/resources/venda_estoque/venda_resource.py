from flask_restful import Resource
from flask import request, g
from helpers.validate_schema import validate_schema
from helpers.database.db_utils import session_scope
from helpers.cache.cache import cache
from helpers.cache.clean_cache import CacheService
from middlewares.auth_middleware import token_required
from middlewares.permission_type import permissao_required

from services.usuarios.access_user_granja_service import ValidarAcessoGranja
from services.venda_estoque.venda_service import VendaService
from services.venda_estoque.item_venda_service import ItemVendaService
from schemas.venda_estoque.venda_schema import VendaSchema as Schema
from schemas.venda_estoque.item_venda_schema import ItemVendaSchema

item_venda_schema = ItemVendaSchema()
itens_venda_schemas = ItemVendaSchema(many=True)

schema = Schema()
schemas = Schema(many=True)

def deletar_cache(granja_id):
    CacheService.deletar_cache_venda(granja_id)

class VendaResource(Resource):

    @token_required
    @permissao_required("VENDA")
    def get(self):
        user_id = g.user_id
        granja_id = request.args.get("granja_id", type=int)
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        pagina = request.args.get("pagina", type=int)
        per_page = 10

        cache_key = f"cache:granja:{granja_id}:venda:pagina:{pagina}"
        dados = cache.get(cache_key)
        if dados is not None:
            return dados, 200

        paginacao = VendaService.listar(granja_id, pagina, per_page)
        resultados = schemas.dump(paginacao.items)

        for venda in resultados:
            itens = ItemVendaService.listar(venda["id"])
            venda["itens"] = itens_venda_schemas.dump(itens)

        resposta = {
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

        cache.set(cache_key, resposta)

        return resposta, 200
    

    @token_required
    @permissao_required("VENDA")
    def post(self):
        user_id = g.user_id

        json = request.get_json()
        itens = json.get("itens")
        
        data, error = validate_schema(schema, json)

        if error:
            return str(error)

        granja_id = data["granja_id"]

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            nova_venda = VendaService.criar(data)
            resultado = schema.dump(nova_venda)

            for item in itens:
                item["venda_id"] = nova_venda.id
                
                data, error = validate_schema(item_venda_schema, item)
                ItemVendaService.criar(data)


        deletar_cache(granja_id)
        return resultado, 201


    @token_required
    @permissao_required("VENDA")
    def put(self, id):
        user_id = g.user_id

        json = request.get_json()
        data, error = validate_schema(schema, json, partial=True)

        if error:
            return str(error)

        granja_id = request.args.get("granja_id", type=int)

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            atualizar = VendaService.buscar_por_id(id)
            atualizado = VendaService.atualizar(atualizar, data)
            resultado = schema.dump(atualizado)

        deletar_cache(granja_id)
        return resultado, 200
    

    @token_required
    @permissao_required("VENDA")
    def delete(self, id):
        user_id = g.user_id
        granja_id = request.args.get("granja_id", type=int)
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            delete = VendaService.buscar_por_id(id)
            VendaService.deletar(delete)

        deletar_cache(delete.granja_id)
        return "", 204