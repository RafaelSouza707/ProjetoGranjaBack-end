from flask_restful import Resource
from flask import request, g
from helpers.cache import cache
from middlewares.auth_middleware import token_required

from services.financas.despesa_services import DespesaService as Service


class CardsGastosResource(Resource):

    @token_required
    def get(self):
        user_id = g.user_id

        cache_key = f"cache:granja:despesa:cards_gastos"
        dados = cache.get(cache_key)
        if dados is not None:
            return dados, 200

        return {
            "maior_gasto": Service.maior_gasto_mes(),
            "total_gasto": Service.total_gasto_mes(),
        }, 200