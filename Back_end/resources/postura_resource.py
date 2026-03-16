from flask import request, current_app
from flask_restful import Resource
from helpers.database import db
from models.postura import Postura
from schemas.postura_schema import PosturaSchema
from models.lote_frangos import LoteFrango
from datetime import datetime

postura_schema = PosturaSchema()
posturas_schema = PosturaSchema(many=True)


class PosturaResource(Resource):

    def get(self, id=None):
        if id:
            current_app.logger.info(f"Buscando relatorio de postura")
            postura = Postura.query.get_or_404(id)

            return postura_schema.dump(postura), 200
        
        data_busca = request.args.get("data")
        if data_busca:
            data_convertida = datetime.strptime(data_busca, "%Y-%m-%d").date()
            resultados = Postura.query.filter_by(data=data_convertida).all()
            
            return posturas_schema.dump(resultados)
        
        posturas = Postura.query.all()
        current_app.logger.info(f"Posturas localizadas com sucesso")

        return posturas_schema.dump(posturas), 200
    
    def post(self):
        json_data = request.get_json()
        data = postura_schema.load(json_data)

        lote_frango = LoteFrango.query.get(data["id_lote_frango"])
        if not lote_frango:
            current_app.logger.warning("Relatorio de postura não encontrado")
            return {"message": "Relatorio de postura não encontrado"}
        
        postura = Postura(**data)
        db.session.add(postura)

        db.session.commit()

        current_app.logger.info(f"Relatorio de postura realizado com sucesso")

        return postura_schema.dump(postura)
    
    def put(self, id):
        postura = Postura.query.get_or_404(id)
        json_data = request.get_json()
        data = postura_schema.load(json_data)

        current_app.logger.info(f"Atualização do relatorio de postura")

        lote_frango = LoteFrango.query.get(data["id_lote_frango"])
        if not lote_frango:
            current_app.logger.info("Lote de frango não encontrado")
            return {"message": "Lote de frango não encontrado"}
        
        postura.id_lote_frango = data["id_lote_frango"]

        postura.data = data["data"]
        postura.quantiade_ovos = data["quantidade_ovos"]
        postura.ovos_descartados = data["ovos_descartados"]

        db.session.commit()

        current_app.logger.info(f"Relatorio de postura atualizado com sucesso id= {id}")

        return postura_schema.dump(postura), 200
    
    def delete(self, id):
        consumo = Postura.query.get_or_404(id)
        current_app.logger.info("Deletando Relatorio de postura")
        db.session.delete(consumo)
        db.session.commit()
        current_app.logger.info(f"Relatorio de postura excluido id={id}")

        return {"message": "Relatorio de postura excluido com sucesso"}