from flask_restful import Resource
from flask import request, g
from helpers.validate_schema import validate_schema
from helpers.db_utils import session_scope
from helpers.cache import cache
from helpers.clean_cache import CacheService
from middlewares.auth_middleware import token_required

from services.aviario.mortalidade_service import MortalidadeService as Servico
from schemas.aviario.mortalidade_schema import MortalidadeSchema as Schema
from services.aviario.lote_frango_service import LoteFrangoService
from services.usuarios.access_user_granja_service import ValidarAcessoGranja

schema = Schema()
schemas = Schema(many=True)

def deletar_cache(granja_id, lote_frango_id):
    CacheService.limpar_cache_mortalidade(granja_id, lote_frango_id)
    CacheService.limpar_cache_cards_granja(granja_id)

class MortalidadeResource(Resource):

    @token_required
    def get(self):
        user_id = g.user_id

        granja_id = request.args.get("granja_id", type=int)
        lote_frango_id = request.args.get("lote_frango_id", type=int)

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        if lote_frango_id is not None:
            cache_key = f"cache:granja:{granja_id}:lote_frango:{lote_frango_id}:mortalidade"

            dados = cache.get(cache_key)
            if dados is not None:
                return dados, 200

            resultados = schemas.dump(Servico.listar_de_lote_frango(lote_frango_id, granja_id))
            
            cache.set(cache_key, resultados)
            return resultados, 200

        cache_key = f"cache:granja:{granja_id}:lote_frango:mortalidade"
        dados = cache.get(cache_key)
        if dados is not None:
            return dados, 200

        resultados = schemas.dump(Servico.listar(granja_id))

        cache.set(cache_key, resultados, timeout=300)
        return resultados, 200
    

    @token_required
    def post(self):
        user_id = g.user_id

        json = request.get_json()
        data, error = validate_schema(schema, json)

        if error:
            return {str(error)}

        lote_frango_id = data["lote_frango_id"]
        
        granja_id, _ = request.args.get("granja_id", type=int)
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            novo = Servico.criar(data, granja_id)
            resultado = schema.dump(novo)

        deletar_cache(granja_id, lote_frango_id)
        return resultado, 201
    

    @token_required
    def put(self, id):
        user_id = g.user_id

        json = request.get_json()
        data, error = validate_schema(schema, json, partial=True)

        if error:
            return {str(error)}

        lote_frango_id = data["lote_frango_id"]

        granja_id, _ = request.args.get("granja_id", type=int)
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            atualizar = Servico.buscar_por_id(id)
            atualizado = Servico.atualizar(atualizar, data)
            resultado = schema.dump(atualizado)

        deletar_cache(granja_id, lote_frango_id)
        return resultado, 200


    @token_required
    def delete(self, id):
        user_id = g.user_id

        granja_id = request.args.get("granja_id", type=int)
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        lote_frango_id = request.args.get("lote_frango_id", type=int)

        with session_scope():
            delete = Servico.buscar_por_id(id)
            Servico.deletar(delete, granja_id)

        deletar_cache(granja_id, lote_frango_id)
        return "", 204