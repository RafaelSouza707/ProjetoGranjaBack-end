from flask_restful import Resource
from flask import request
from helpers.validate_schema import validate_schema
from helpers.db_utils import session_scope

from services.financas.despesa_services import DespesaService as Service
from schemas.financas.despesa_schema import DespesaSchema as Schema

class CardsGastosResource(Resource):

    def get(self):
        return {
            "maior_gasto": Service.maior_gasto_mes(),
            "total_gasto": Service.total_gasto_mes()
        }, 200
