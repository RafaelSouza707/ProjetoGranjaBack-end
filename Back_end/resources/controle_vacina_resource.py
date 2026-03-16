from flask import request, current_app
from flask_restful import Resource
from helpers.database import db
from models.controle_vacinas import ControleVacinas
from schemas.controle_vacina_schema import ControleVacinaSchema
from models.lote_frangos import LoteFrango
from datetime import datetime

controle_vacina = ControleVacinaSchema()
controles_vacinas = ControleVacinaSchema(many=True)


class ControleVacinasResource(Resource):

    def get(self, id=None):
        if id:
            current_app.logger.info(f"Buscando controle vacina")
            controle = ControleVacinas.query.get_or_404(id)

            return controle_vacina.dump(controle)
        
        data_busca = request.args.get("data")
        if data_busca:
            data_convertida = datetime.strptime(data_busca, "%Y-%m-%d").date()
            resultados = ControleVacinas.query.filter_by(data=data_convertida).all()
            
            return controles_vacinas.dump(resultados)
        
        lotes = ControleVacinas.query.all()
        current_app.logger.info(f"Controles de vacinas localizados com sucesso")

        return controles_vacinas.dump(lotes), 200
    
    def post(self):
        json_data = request.get_json()
        data = controle_vacina.load(json_data)

        lote_frango = LoteFrango.query.get(data["id_lote_frango"])
        if not lote_frango:
            current_app.logger.warning("Lote de frango não econtrado!")
            return {"message": "Lote de frango não econtrado!"}


        controle = ControleVacinas(**data)
        db.session.add(controle)

        db.session.commit()

        current_app.logger.info("Novo relatiorio de controle de vacinas criado")

        return controle_vacina.dump(controle), 201
    
    def put(self, id):
        controle = ControleVacinas.query.get_or_404(id)
        json_data = request.get_json()
        data = controle_vacina.load(json_data)

        current_app.logger.info(f"Atualização do controle de vacinas")

        lote_frango = LoteFrango.query.get(data["id_lote_frango"])
        if not lote_frango:
            current_app.logger.info(f"Lote de frango não encontrado")
            return {"message": "Lote de frango não encontrado"}
        
        controle.id_lote_frango = data["id_lote_frango"]

        controle.medicamento_aplicado = data["medicamento_aplicado"]
        controle.data = data["data"]
        controle.responsavel_aplicacao = data["responsavel_aplicacao"]

        db.session.commit()

        current_app.logger.info(f"Controle vacina atualizado")

        return controle_vacina.dump(controle), 200
    
    def delete(self, id):
        consumo = ControleVacinas.query.get_or_404(id)
        current_app.logger.info("Deletando controle de vacina")
        db.session.delete(consumo)
        db.session.commit()
        current_app.logger.info(f"Controle de vacina excluida id={id}")

        return {"message": "Controle de vacina excluido com sucesso"}