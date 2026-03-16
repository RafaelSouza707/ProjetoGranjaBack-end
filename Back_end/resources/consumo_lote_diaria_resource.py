from models.lote_frangos import LoteFrango
from models.lote_racao import LoteRacao
from flask import request, current_app
from flask_restful import Resource
from helpers.database import db
from models.consumo_lote_diaria import ConsumoLoteDiaria
from schemas.consumo_lote_diaria_schema import ConsumoLoteDiariaSchema
from datetime import datetime

consumo_chema = ConsumoLoteDiariaSchema()
consumos_schema = ConsumoLoteDiariaSchema(many=True)


class ConsumoLoteDiariaResource(Resource):

    def get(self, id=None):
        if id:
            current_app.logger.info(f"Buscando consumo de lote")
            consumo = ConsumoLoteDiaria.query.get_or_404(id)

            return consumo_chema.dump(consumo), 200
        
        data_busca = request.args.get("data")
        if data_busca:
            data_convertida = datetime.strptime(data_busca, "%Y-%m-%d").date()
            resultados = ConsumoLoteDiaria.query.filter_by(data=data_convertida).all()
            
            return consumos_schema.dump(resultados)

        consumo = ConsumoLoteDiaria.query.all()
        current_app.logger.info(f"Consumos localizados com sucesso")

        return consumos_schema.dump(consumo), 200
    

    def post(self):
        json_data = request.get_json()
        data = consumo_chema.load(json_data)

        lote_frango = LoteFrango.query.get(data["id_lote_frango"])
        if not lote_frango:
            current_app.logger.warning("Lote de frango não econtrado!")
            return {"message": "Lote de frango não econtrado!"}
        
        lote_racao = LoteRacao.query.get(data["id_lote_racao"])
        if not lote_racao:
            current_app.logger.warning("Lote de ração não encontrado")
            return {"message": "Lote de ração não encontrado"}
        
        quantidade = data["quilos"]

        if lote_racao.quilos < quantidade:
            current_app.logger.warning("Estoque insuficiente de ração")
            return {"error": "Estoque insuficiente de ração"}, 400
        
        lote_racao.quilos -= quantidade

        consumo = ConsumoLoteDiaria(**data)
        db.session.add(consumo)

        db.session.commit()

        current_app.logger.info(f"Consumo registrado. {quantidade}kg abatidos do lote de ração {lote_racao.id}")

        return consumo_chema.dump(consumo), 201

    def put(self, id):
        consumo = ConsumoLoteDiaria.query.get_or_404(id)
        json_data = request.get_json()
        data = consumo_chema.load(json_data)

        current_app.logger.info(f"Atualização do registro do consumo diario do lote")

        lote_frango = LoteFrango.query.get(data["id_lote_frango"])
        if not lote_frango:
            current_app.logger.info("Lote de frango não encontrado")
            return {"message": "Lote de frango não encontrado"}
        
        consumo.id_lote_frango = data["id_lote_frango"]

        lote_racao = LoteRacao.query.get(data["id_lote_racao"])
        if not lote_racao:
            current_app.logger.info("Lote de ração não encontrado")
            return {"message": "Lote de ração não econtrado"}
        
        consumo.id_lote_racao = data["id_lote_racao"]
        
        consumo.data = data["data"]
        consumo.quilos = data["quilos"]

        db.session.commit()

        current_app.logger.info(f"Diaria de consumo atualizada com sucesso id= {id}")

        return consumo_chema.dump(consumo), 200

    def delete(self, id):
        consumo = ConsumoLoteDiaria.query.get_or_404(id)
        current_app.logger.info("Deletando consumo diario do lote")
        db.session.delete(consumo)
        db.session.commit()
        current_app.logger.info(f"Diaria de consumo excluida id={id}")

        return {"message": "Diaria de consumo excluido com sucesso"}