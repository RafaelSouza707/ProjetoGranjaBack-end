from flask_restful import Resource
from helpers.cache.cache import cache
from flask import g, request
from middlewares.auth_middleware import token_required
from middlewares.permission_type import permissao_required

from services.usuarios.access_user_granja_service import ValidarAcessoGranja
from services.aviario.lote_frango_service import LoteFrangoService as Servico

class CardsLoteFrango(Resource):

    @token_required
    @permissao_required("AVIARIO")
    def get(self):
        user_id = g.user_id
        granja_id = request.args.get("granja_id", type=int)

        lote_frango_id = request.args.get("lote_frango_id", type=int)

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        cache_key = f"cache:granja:{granja_id}:cards_lote_frango:{lote_frango_id}"
        dados = cache.get(cache_key)
        if dados is not None:
            return dados, 200
        
        resultado = {
            "mortalidade_lote_frango_mes":Servico.mortalidade_lote_mes(lote_frango_id),
            "total_aves_lote_frango": Servico.total_aves_lote_frango(lote_frango_id),
            "consumo_total_lote_frango": Servico.consumo_total_lote_frango(lote_frango_id)
        }

        cache.set(cache_key, resultado)
        return resultado, 200