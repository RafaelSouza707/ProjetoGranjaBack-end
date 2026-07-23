from flask_restful import Resource
from helpers.cache.cache import cache
from helpers.cache.clean_cache import CacheService
from flask import g, request
from middlewares.auth_middleware import token_required
from middlewares.permission_type import permissao_required
from services.usuarios.access_user_granja_service import ValidarAcessoGranja

from services.aviario.lote_racao_service import LoteRacaoService
from services.aviario.consumo_lote_diaria_service import ConsumoLoteDiariaService
from schemas.aviario.lote_racao_schema import LoteRacaoSchema

lote_racao_schema = LoteRacaoSchema()

class CardsLoteRacao(Resource):
    
    @token_required
    @permissao_required("AVIARIO")
    def get(self):
        user_id = g.user_id

        granja_id = request.args.get("granja_id", type=int)

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        cache_key = f"cache:granja:{granja_id}:lotes_racoes:cards"
        dados = cache.get(cache_key)
        if dados is not None:
            return dados
        
        consumo_mes = ConsumoLoteDiariaService.consumo_mensal(granja_id)
        consumo_diaria = ConsumoLoteDiariaService.consumo_mensal_diaria(consumo_mes)
        lote_menor_quantiade = lote_racao_schema.dump(LoteRacaoService.lote_menor_quantidade(granja_id))
        qtd_total_granja = LoteRacaoService.quantidade_total_racao_granja(granja_id)
                
        resultado = {
            "quantidade_total_racao_granja": qtd_total_granja,
            "quantidade_lotes_racao": LoteRacaoService.quantidade_lotes_racao(granja_id),
            "total_consumido_mes": {
                "mes": consumo_mes,
                "diaria": consumo_diaria
            },
            "lote_menor_quantiade": {
                "tipo_racao": lote_menor_quantiade["tipo_racao"]["nome"],
                "quantidade": lote_menor_quantiade["quilos"] or None
            },
            "previsao": LoteRacaoService.previsao_acabar(qtd_total_granja, consumo_diaria)
        }


        cache.set(cache_key, resultado)

        return resultado, 200