from flask_restful import Resource
from helpers.cache import cache
from flask import g, request
from middlewares.auth_middleware import token_required
from services.usuarios.access_user_granja_service import ValidarAcessoGranja

from services.aviario.lote_frango_service import LoteFrangoService as Servico

class CardsLoteFrango(Resource):

    @token_required
    def get(self):
        user_id = g.user_id
        granja_id = request.args.get("granja_id", type=int)

        lote_frango_id = request.args.get("lote_frango_id", type=int)

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)
        
        resultado = {
            "mortalidade_granja_mes": Servico.mortalidade_granja_mes(granja_id),
            "mortalidade_lote_frango_mes":Servico.mortalidade_lote_mes(lote_frango_id),
            "total_aves_lote_frango": Servico.total_aves_lote_frango(lote_frango_id),
            "total_aves_granja": Servico.total_aves_granja(granja_id),
            "baixa_quantidade_aves_lote_frango": Servico.baixa_quantidade_aves_granja(granja_id)
        }
        
        return resultado, 200