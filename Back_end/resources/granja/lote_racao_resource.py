from flask_restful import Resource
from flask import request
from helpers.validate_schema import validate_schema
from helpers.db_utils import session_scope
from helpers.cache import cache

from services.granja.lote_racao_service import LoteRacaoService as Servico
from schemas.granja.lote_racao_schema import LoteRacaoSchema as Schema

schema = Schema()
schemas = Schema(many=True)

class  LoteRacaoResource(Resource):

    def get(self, id=None):
        if id:
            cache_key = f"lote_racao:{id}"
            dados = cache.get(cache_key)
            if dados is not None:
                print("CACHE USADO") # Apenas para testar o uso do cache. O print Será retirado na proxima atualização.
                return dados
            print("CACHE NÃO USADO") # Apenas para testar o uso do cache. O print Será retirado na proxima atualização.
            with session_scope():
                resultado = Servico.buscar_por_id(id)
                resultado_final = schema.dump(resultado)

            cache.set(
                cache_key,
                resultado_final,
                timeout=300
            )
            return resultado_final, 200
        
        cache_key = "lote_racao"
        dados = cache.get(cache_key)
        if dados is not None:
            print("CACHE USADO") # Apenas para testar o uso do cache. O print Será retirado na proxima atualização.
            return dados
        print("CACHE NÃO USADO") # Apenas para testar o uso do cache. O print Será retirado na proxima atualização.
        with session_scope():
            resultados = Servico.listar()
            resultados_final = schemas.dump(resultados)

        cache.set(
            cache_key,
            resultados_final,
            timeout=300
        )
        return resultados_final, 200


    def post(self):
        json = request.get_json()
        
        data, error = validate_schema(schema, json)

        if error:
            return str(error)
        
        with session_scope():
            novo = Servico.criar(data)
            resultado = schema.dump(novo)
        
        cache.delete("lote_racao")
        return resultado, 201
    

    def put(self, id):
        json = request.get_json()

        data, error = validate_schema(schema, json, partial=True)

        if error:
            return str(error)
        
        with session_scope():
            atualizar = Servico.buscar_por_id(id)
            atualizado = Servico.atualizar(atualizar, data)
            resultado = schema.dump(atualizado)
        
        cache.delete("lote_racao")
        cache.delete(f"lote_racao:{id}")
        return resultado, 200
    

    def delete(self, id):
        with session_scope():
            delete = Servico.buscar_por_id(id)
            Servico.deletar(delete)

        cache.delete("lote_racao")
        cache.delete(f"lote_racao:{id}")
        return "", 204