from flask import request, current_app
from flask_restful import Resource
from helpers.database import db
from models.despesa import Despesa
from schemas.despesa_schema import DespesaSchema
from models.tipo_despesa import TipoDespesa
from datetime import datetime

despesa_schema = DespesaSchema()
despesas_schema = DespesaSchema(many=True)


class DespesaResource(Resource):

    def get(self, id=None):
        if id:
            current_app.logger.info(f"Buscando despesa")
            despesa = Despesa.query.get_or_404(id)

            return despesa_schema.dump(despesa),200
        
        data_busca = request.args.get("data")
        if data_busca:
            data_convertida = datetime.strptime(data_busca, "%Y-%m-%d").date()
            resultados = Despesa.query.filter_by(data=data_convertida).all()
            
            return despesas_schema.dump(resultados)

        despesa = Despesa.query.all()
        current_app.logger.info(f"Despesas localizadas com sucesso")

        return despesas_schema.dump(despesa), 200
    
    def post(self):
        json_data = request.get_json()
        data = despesa_schema.load(json_data)

        tipo_despesa = TipoDespesa.query.get(data["id_tipo_despesa"])
        if not tipo_despesa:
            current_app.logger.warning(f"Tipo de despesa não encontrado")
            return {"message": "Tipo de despesa não encontrado"}

        despesa = Despesa(**data)
        db.session.add(despesa)

        db.session.commit()

        current_app.logger.info(f"Despesa registrada. {data}")

        return despesa_schema.dump(despesa), 201
    
    def put(self, id):
        despesa = Despesa.query.get_or_404(id)
        json_data = request.get_json()
        data = despesa_schema.load(json_data)
        
        current_app.logger.info(f"Atualização do registro de despesa")

        tipo_despesa = TipoDespesa.query.get(data["id_tipo_despesa"])
        if not tipo_despesa:
            current_app.logger.info(f"Tipo de despesa não localizado")
            return {"message": "Tipo de despesa não localizado"}
        
        despesa.id_tipo_despesa = data["id_tipo_despesa"]
        despesa.data = data["data"]
        despesa.valor = data["valor"]

        db.session.commit()

        current_app.logger.info(f"Despesa adicionada com sucesso id= {id}")

        return despesa_schema(despesa), 200
    
    def delete(self, id):
        despesa = Despesa.query.get_or_404(id)
        current_app.logger.info(f"Deletando despesa")
        db.session.delete(despesa)
        db.session.commit()
        current_app.logger.info(f"Despesa deletada id= {id}")

        return {"message": "Despesa deletado com sucesso"}