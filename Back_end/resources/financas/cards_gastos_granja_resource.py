from flask_restful import Resource
from flask import request, g
from helpers.cache import cache
from middlewares.auth_middleware import token_required

from services.financas.despesa_services import DespesaService
from services.usuarios.access_user_granja_service import ValidarAcessoGranja

class CardsGastosGranjaResource(Resource):

    @token_required
    def get(self):
        user_id = g.user_id

        granja_id = request.args.get("granja_id", type=int)
        if granja_id is None:
            return {"error": "granja_id é obrigatório"}, 400

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        cache_key = f"cache:granja:{granja_id}:despesa:cards_gastos"
        dados = cache.get(cache_key)
        if dados is not None:
            return dados, 200
        
        maior_gasto = DespesaService.maior_gasto_mes_granja(granja_id)
        
        resultado = {
            "maior_gasto_mes_granja": {"id": maior_gasto.id, "valor": float(maior_gasto.valor),},
            "total_gasto_mes_granja": DespesaService.total_gasto_mes_granja(granja_id),
        }

        cache.set(cache_key, resultado)

        return resultado