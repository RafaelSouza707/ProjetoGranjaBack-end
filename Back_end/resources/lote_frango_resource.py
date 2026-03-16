from flask import request, current_app
from flask_restful import Resource
from helpers.database import db
from models.lote_frangos import LoteFrango
from schemas.lote_frango_schema import LoteFrangoSchema
from sqlalchemy import func
from models.mortalidade import Mortalidade

lote_frango_schema = LoteFrangoSchema()
lotes_frangos_schema = LoteFrangoSchema(many=True)


class LoteFrangoResource(Resource):
    
    def get(self, id=None, data=None):
        if id:
            lote_frango = LoteFrango.query.get_or_404(id)
            current_app.logger.info(f"Lote de frangos id= {id} encontrado com sucesso")

            total_mortes = (db.session.query(func.sum(Mortalidade.quantidade_mortes)).filter(Mortalidade.id_lote_frango == id).scalar()) or 0

            aves_viva = lote_frango.quantidade_inicial - total_mortes

            resultado = lote_frango_schema.dump(lote_frango)

            resultado["total_mortes"] = total_mortes
            resultado["aves_viva"] = aves_viva

            return resultado, 200
        
        current_app.logger.info(f"Buscando todos os lotes de frangos")
        lotes = LoteFrango.query.all()

        current_app.logger.info(f"{len(lotes)} lotes de frangos encontrados")
        return lotes_frangos_schema.dump(lotes), 200
    
    def post(self):
        json_data = request.get_json()
        data = lote_frango_schema.load(json_data)

        novo_lote = LoteFrango(**data)
        db.session.add(novo_lote)
        current_app.logger.info("Novo lote de frangos sendo inserido")

        db.session.commit()
        current_app.logger.info(f"Lote de frangos inserido com sucesso {novo_lote}")

        return lote_frango_schema.dump(novo_lote), 201
    
    def put(self, id):
        lote = LoteFrango.query.get_or_404(id)
        json_data = request.get_json()
        data = lote_frango_schema.load(json_data)

        current_app.logger.info(f"Atualizando lote de frangos id= {id}")

        lote.quantidade_inicial = data["quantidade_inicial"]
        lote.data_entrada_aves = data["data_entrada_aves"]
        lote.data_ninhada = data["data_ninhada"]
        lote.fornecedor = data["fornecedor"]
        lote.tipo_lote = data["tipo_lote"]
        lote.galpao = data["galpao"]
        lote.status = data["status"]
        lote.peso_medio = data["peso_medio"]

        db.session.commit()

        current_app.logger.info(f"Lote de frangos atualizado com sucesso id= {id}")

        return lote_frango_schema.dump(lote), 200
    
    def delete(self, id):
        lote = LoteFrango.query.get_or_404(id)
        current_app.logger.info(f"Lote de frangos sendo apagado id= {id}")
        db.session.delete(lote)
        db.session.commit()
        current_app.logger.info(f"Lote de frangos apagado com sucesso id= {id}")

        return {"message": "Lote de frangos removido com sucesso"}