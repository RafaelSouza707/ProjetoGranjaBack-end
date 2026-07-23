from flask_restful import Resource
from flask import request, g
from helpers.cache.cache import cache
from middlewares.auth_middleware import token_required
from middlewares.permission_type import permissao_required

from services.financas.receita_service import ReceitaService
from services.usuarios.access_user_granja_service import ValidarAcessoGranja

class CardsReceitasResource(Resource):

    @token_required
    @permissao_required("FINANCAS")
    def get(self):
        user_id = g.user_id

        granja_id = request.args.get("granja_id", type=int)

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        cache_key = f"cache:granja:{granja_id}:receita:cards_receitas"
        dados = cache.get(cache_key)
        if dados is not None:
            return dados
        
        maior_receita = ReceitaService.card_receita_maior_receita_mes(granja_id)
        
        resultado = {
            "card_receita_valor_total_venda_mes_graja": ReceitaService.card_receita_valor_total_receita_mes_graja(granja_id),
            "card_receita_total_vendas_mes_granja": ReceitaService.card_receita_total_receitas_mes_granja(granja_id),
            "card_receita_maior_receita_mes": {
                "id": maior_receita.id,
                "valor": float(maior_receita.valor)
            }
            if maior_receita
            else None
        }
        
        return resultado