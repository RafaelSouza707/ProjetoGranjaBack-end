from flask_restful import Resource
from helpers.cache.cache import cache
from flask import g, request
from middlewares.auth_middleware import token_required
from middlewares.permission_type import permissao_required
from services.usuarios.access_user_granja_service import ValidarAcessoGranja

from services.aviario.mortalidade_service import MortalidadeService
from schemas.aviario.mortalidade_schema import MortalidadeSchema

schemas = MortalidadeSchema(many=True)


class CardMortalidadeGranja(Resource):

    @token_required
    @permissao_required("GRANJA")
    def get(self):
        user_id = g.user_id

        granja_id = request.args.get("granja_id", type=int)
        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        cache_key = f"granja:{granja_id}:card:mortalidade:"
        dados = cache.get(cache_key)
        if dados is not None:
            return dados, 200

        resultados = MortalidadeService.grafico_mortalidade_granja(granja_id)
        cache.set(cache_key, resultados)
        return resultados, 200
