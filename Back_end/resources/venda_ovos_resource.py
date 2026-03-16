
from flask import request, current_app
from flask_restful import Resource
from helpers.database import db
from models.venda_ovos import VendaOvos
from schemas.venda_ovos_schema import VendaOvosSchema
from models.lote_frangos import LoteFrango
from datetime import datetime

venda_ovos_schema = VendaOvosSchema()
vendas_ovos_schema = VendaOvosSchema(many=True)


class VendaOvosResource(Resource):

    def get(self, id=None):
        if id:
            current_app.logger.info(f"Buscando venda realizada")
            venda = VendaOvos.query.get_or_404(id)

            return venda_ovos_schema.dump(venda)
        
        data_busca = request.args.get("data")
        if data_busca:
            data_convertida = datetime.strptime(data_busca, "%Y-%m-%d").date()
            resultados = VendaOvos.query.filter_by(data=data_convertida).all()
            
            return vendas_ovos_schema.dump(resultados)
        
        vendas_ovos = VendaOvos.query.all()
        current_app.logger.info(f"Buscando vendas realizadas")

        return vendas_ovos_schema.dump(vendas_ovos), 200
    
    def post(self):
        json_data = request.get_json()
        data = venda_ovos_schema.load(json_data)


        id_lote_frango = LoteFrango.query.get(data["id_lote_frango"])
        if not id_lote_frango:
            current_app.logger.info(f"Lote de frango não encontrado")
            return {"error": "Lote de frango não encontrado"}, 400
        
        venda = VendaOvos(**data)
        db.session.add(venda)

        db.session.commit()

        current_app.logger.info(f"Venda registrada com sucesso")

        return venda_ovos_schema.dump(venda), 201
    
    def put(self, id):
        venda = VendaOvos.query.get_or_404(id)
        json_data = request.get_json()
        data = venda_ovos_schema.load(json_data)

        current_app.logger.info(f"Atualização do registro do consumo diario do lote")

        lote_frango = LoteFrango.query.get(data["id_lote_frango"])
        if not lote_frango:
            current_app.logger.info("Lote de frangos não encontrado")
            return {"message": "Lote de frangos não encontrado"}
        
        venda.id_lote_frango = data["id_lote_frango"]

        venda.data = data["data"]
        venda.valor = data["valor"]
        venda.quantidade_ovos = data["quantidade_ovos"]

        db.session.commit()

        current_app.logger.info(f"Venda de ovos atualizada com sucesso id= {id}")

        return venda_ovos_schema.dump(venda), 200
    
    def delete(self, id):
        consumo = VendaOvos.query.get_or_404(id)
        current_app.logger.info("Deletando venda de ovos")
        db.session.delete(consumo)
        db.session.commit()
        current_app.logger.info(f"Venda de ovos deletetada com sucesso id={id}")

        return {"message": "Venda de ovos excluida com sucesso"}
