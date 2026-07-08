from flask_restful import Resource
from flask import request, g
from helpers.cache import cache
from middlewares.auth_middleware import token_required

from services.financas.despesa_services import DespesaService
from services.financas.receita_service import ReceitaService
from services.usuarios.access_user_granja_service import ValidarAcessoGranja


class CardsFinancasResource(Resource):

    @token_required
    def get(self):
        user_id = g.user_id

        granja_id = request.args.get("granja_id", type=int)

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        cache_key = f"cache:granja:{granja_id}:despesa:cards_financas"
        dados = cache.get(cache_key)
        if dados is not None:
            return dados, 200
        
        despesas_valor = DespesaService.total_gasto_mes_granja(granja_id)
        receitas_valor = ReceitaService.card_receita_valor_total_receita_mes_graja(granja_id)
        lucro_mes = receitas_valor - despesas_valor

        return {
            "total_gasto_mes_granja": despesas_valor,
            "card_receita_total_receitas_mes_granja": receitas_valor,
            "lucro_granja_mes": lucro_mes
        }, 200