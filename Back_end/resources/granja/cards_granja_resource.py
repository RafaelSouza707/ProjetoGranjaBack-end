from flask_restful import Resource
from helpers.cache.cache import cache
from flask import g, request
from middlewares.auth_middleware import token_required
from middlewares.permission_type import permissao_required
from services.usuarios.access_user_granja_service import ValidarAcessoGranja

from services.aviario.lote_frango_service import LoteFrangoService as Servico

class CardsGranja(Resource):

    @token_required
    @permissao_required("AVIARIO")
    def get(self):
        user_id = g.user_id
        granja_id = request.args.get("granja_id", type=int)

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        cache_key = f"cache:granja:{granja_id}:cards"
        dados = cache.get(cache_key)
        if dados is not None:
            return dados
        
        resultado = {
            "mortalidade_granja_mes": Servico.mortalidade_granja_mes(granja_id),
            "total_aves_granja": Servico.total_aves_granja(granja_id),
            "baixa_quantidade_aves_lote_frango": Servico.baixa_quantidade_aves_granja(granja_id)
        }

        cache.set(cache_key, resultado)
        return resultado, 200