from flask_restful import Resource
from flask import request, g
from helpers.validate_schema import validate_schema
from helpers.db_utils import session_scope
from helpers.cache import cache
from middlewares.auth_middleware import token_required

from services.venda_estoque.item_venda_service import ItemVendaService as Servico
from services.venda_estoque.produto_service import ProdutoService
from schemas.venda_estoque.item_venda_schema import ItemVendaSchema as Schema

schema = Schema()
schemas = Schema(many=True)

def deletar_cache(granja_id):
    cache.delete(f"cache:granja:{granja_id}:item_venda")

class ItemVendaResource(Resource):

    @token_required
    def get(self):
        user_id = g.user_id

        produto = ProdutoService.buscar_por_id(request.args.get("produto_id", type=int))
        granja_id = produto.granja_id

        cache_key = f"cache:granja:{granja_id}:item_venda"
        dados = cache.get(user_id)
        if dados is not None:
            return dados, 200
        
        resultados = schemas.dump(Servico.listar(granja_id))
        
        cache.set(
            cache_key,
            resultados
        )
        return resultados, 200


    @token_required
    def post(self):
        json = request.get_json()        
        data, error = validate_schema(schema, json)

        if error:
            return str(error)
        
        produto = ProdutoService.buscar_por_id(data["produto_id"])
        granja_id = produto.granja_id


        with session_scope():
            novo = Servico.criar(data)
            resultado = schema.dump(novo)
        
        deletar_cache(granja_id)
        return resultado, 201
    

    @token_required
    def put(self, id):
        json = request.get_json()
        data, error = validate_schema(schema, json, partial=True)

        if error:
            return str(error)
        
        produto = ProdutoService.buscar_por_id(data["produto_id"])
        granja_id = produto.granja_id

        with session_scope():
            atualizar = Servico.buscar_por_id(id)
            atualizado = Servico.atualizar(atualizar, data)
            resultado = schema.dump(atualizado)
        
        deletar_cache(granja_id)
        return resultado, 200
    

    @token_required
    def delete(self, id):
        with session_scope():
            delete = Servico.buscar_por_id(id)
            produto = ProdutoService.buscar_por_id(delete.produto_id)
            granja_id = produto.granja_id
            Servico.deletar(delete)

        deletar_cache(granja_id)
        return "", 204