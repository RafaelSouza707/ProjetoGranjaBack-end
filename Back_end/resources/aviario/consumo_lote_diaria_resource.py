from flask_restful import Resource
from flask import request, g
from helpers.validate_schema import validate_schema
from helpers.db_utils import session_scope
from helpers.cache import cache
from middlewares.auth_middleware import token_required

from services.aviario.consumo_lote_diaria_service import ConsumoLoteDiariaService
from schemas.aviario.consumo_lote_diaria_schema import ConsumoLoteDiariaSchema as Schema
from services.usuarios.access_user_granja_service import ValidarAcessoGranja


schema = Schema()
schemas = Schema(many=True)

def deletarCache(granja_id, lote_frango_id):
    cache.delete(f"cache:granja:{granja_id}:lote_frango:consumos_lote_diaria")
    cache.delete(f"cache:granja:{granja_id}:lote_frango:{lote_frango_id}:consumos_lote_diaria")
    cache.delete(f"cache:granja:{granja_id}:lote_frango:cards_lote_frango")


class ConsumoLoteDiariaResource(Resource):

    @token_required
    def get(self):
        user_id = g.user_id
            
        granja_id = request.args.get("granja_id", type=int)

        lote_frango_id = request.args.get("lote_frango_id", type=int)
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        if lote_frango_id is not None:
            cache_key = f"cache:granja:{granja_id}:lote_frango:{lote_frango_id}:consumos_lote_diaria"
            cache.delete(cache_key)
            dados = cache.get(cache_key)
            if dados is not None:
                return dados, 200
            
            resultados = schemas.dump(ConsumoLoteDiariaService.listar_de_lote_frango(lote_frango_id))
            
            cache.set(
                cache_key,
                resultados
            )

            return resultados, 200

        cache_key = f"cache:granja:{granja_id}:lote_frango:consumos_lote_diaria"
        dados = cache.get(cache_key)
        if dados is not None:
            return dados, 200

        resultados = schemas.dump(ConsumoLoteDiariaService.listar(granja_id))
        
        cache.set(
            cache_key,
            resultados,
        )

        return resultados, 200


    @token_required
    def post(self):
        user_id = g.user_id

        json = request.get_json()
        json.pop("lote_racao", None)
        data, error = validate_schema(schema, json)

        if error:
            return {str(error)}

        lote_frango_id = data["lote_frango_id"]
        granja_id = request.args.get("granja_id", type=int)

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            novo = ConsumoLoteDiariaService.criar(data)
            resultado = schema.dump(novo)

        deletarCache(granja_id, lote_frango_id)
        return resultado, 201


    @token_required
    def put(self, id):
        user_id = g.user_id

        json = request.get_json()
        json.pop("lote_racao", None)
        data, error = validate_schema(schema, json, partial=True)

        if error:
            return {str(error)}

        granja_id = request.args.get("granja_id", type=int)
        
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        lote_frango_id = data["lote_frango_id"]
        
        with session_scope():
            atualizar = ConsumoLoteDiariaService.buscar_por_id(id)
            atualizado = ConsumoLoteDiariaService.atualizar(atualizar, data)
            resultado = schema.dump(atualizado)

        deletarCache(granja_id, lote_frango_id)
        return resultado, 200
    

    @token_required
    def delete(self, id):
        user_id = g.user_id
        
        granja_id = request.args.get("granja_id", type=int)
        
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            delete = ConsumoLoteDiariaService.buscar_por_id(id)
            lote_frango_id = delete.lote_frango_id
            ConsumoLoteDiariaService.deletar(delete)

        deletarCache(granja_id, lote_frango_id)
        return "", 204