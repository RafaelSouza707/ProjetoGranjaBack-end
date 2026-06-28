from flask_restful import Resource
from flask import request, g
from helpers.validate_schema import validate_schema
from helpers.db_utils import session_scope
from middlewares.auth_middleware import token_required
from helpers.cache import cache

from services.financas.tipo_despesa_services import TipoDespesaService as Tipo
from schemas.financas.tipo_despesa_schema import TipoDespesaSchema
from services.usuarios.access_user_granja_service import ValidarAcessoGranja

schema = TipoDespesaSchema()
schemas = TipoDespesaSchema(many=True)


def deletar_cache(granja_id):
    cache.delete(f"cache:granja:{granja_id}:tipo_despesa")


class TipoDespesaResource(Resource):

    @token_required
    def get(self):
        user_id = g.user_id
        granja_id = request.args.get("granja_id", type=int)

        if granja_id is None:
            return {"error": "granja_id é obrigatório"}, 400

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        cache_key = f"cache:granja:{granja_id}:tipo_despesa"
        dados = cache.get(cache_key)
        if dados is not None:
            return dados, 200

        resultados = schemas.dump(Tipo.listar(granja_id))

        cache.set(cache_key, resultados)
        return resultados, 200


    @token_required
    def post(self):
        user_id = g.user_id

        json = request.get_json()
        data, error = validate_schema(schema, json)

        if error:
            return str(error)

        granja_id = data.get("granja_id")
        if granja_id is None:
            return {"error": "granja_id é obrigatório"}, 400

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            tipo = Tipo.criar(data)
            resultado = schema.dump(tipo)

        deletar_cache(granja_id)
        return resultado, 201
    

    @token_required
    def put(self, id):
        user_id = g.user_id

        json = request.get_json()
        data, error = validate_schema(schema, json, partial=True)

        if error:
            return str(error)

        granja_id = data.get("granja_id")
        if granja_id is None:
            return {"error": "granja_id é obrigatório"}, 400

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            tipo = Tipo.buscar_por_id(id, granja_id)
            atualizar = Tipo.atualizar(tipo, data)
            resultado = schema.dump(atualizar)

        deletar_cache(granja_id)
        return resultado, 200
    

    @token_required
    def delete(self, id):
        user_id = g.user_id
        granja_id = request.args.get("granja_id", type=int)

        if granja_id is None:
            return {"error": "granja_id é obrigatório"}, 400

        ValidarAcessoGranja.validar_acesso_granja(user_id, granja_id)

        with session_scope():
            tipo = Tipo.buscar_por_id(id, granja_id)
            Tipo.deletar(tipo)

        deletar_cache(granja_id)
        return "", 204