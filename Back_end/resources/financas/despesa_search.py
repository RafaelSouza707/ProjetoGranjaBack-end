from flask_restful import Resource
from flask import request

from schemas.financas.despesa_schema import DespesaSchema
from elastic.buscar_despesas import buscar_despesas
from middlewares.auth_middleware import token_required

class DespesaSearch(Resource):

    @token_required
    def get(self):
        termo = request.args.get("q", "")
        resultados = buscar_despesas(termo)
        
        return DespesaSchema(many=True).dump(resultados), 200