from flask import request, current_app
from flask_restful import Resource
from datetime import datetime
from helpers.database import db
from models.lote_frangos import LoteFrango
from models.mortalidade import Mortalidade
from schemas.mortalidade_schema import MortalidadeSchema

mortalidade_schema = MortalidadeSchema()
mortalidades_schema = MortalidadeSchema(many=True)


class MortalidadeResource(Resource):

    def get(self, id=None):
        if id: 
            mortalidades = Mortalidade.query.get_or_404(id)
            current_app.logger.info(f"Mortalidade id= {id} encontrada com sucesso")
            
            return mortalidade_schema.dump(mortalidades), 200
        
        data_busca = request.args.get("data")
        if data_busca:
            data_convertida = datetime.strptime(data_busca, "%Y-%m-%d").date()
            resultados = Mortalidade.query.filter_by(data=data_convertida).all()
            
            return mortalidades_schema.dump(resultados)
            
        mortalidades = Mortalidade.query.all()
        current_app.logger.info("Buscando todas as mortalidades")

        return mortalidades_schema.dump(mortalidades), 200
    
    def post(self):
        json_data = request.get_json()
        data = mortalidade_schema.load(json_data)
        
        lote = LoteFrango.query.get(data["id_lote_frango"])
        if not lote:
            return {"erro": "Lote de frango não existe"}, 400
    
        nova_mortalidade = Mortalidade(**data)
        db.session.add(nova_mortalidade)
        current_app.logger.info("Nova mortalidade sendo inserida")
        
        db.session.commit()
        current_app.logger.info(f"Mortalidade inserida com sucesso {nova_mortalidade}")
        
        return mortalidade_schema.dump(nova_mortalidade), 201
    
    def put(self, id):
        mortalidades = Mortalidade.query.get_or_404(id)
        json_data = request.get_json()
        data = mortalidade_schema.load(json_data)
        
        lote = LoteFrango.query.get(data["id_lote_frango"])
        if not lote:
            return {"erro": "Lote de frango não existe"}, 400
        
        current_app.logger.info(f"Atualizando mortalidade id= {id}")
        
        mortalidades.lote_frango_id = data["id_lote_frango"]
        mortalidades.data = data["data"]
        mortalidades.quantidade_mortes = data["quantidade_mortes"]
        
        db.session.commit()
        
        current_app.logger.info(f"Mortalidade atualizada com sucesso id= {id}")
        
        return mortalidade_schema.dump(mortalidades), 200
    
    def delete(self, id):
        mortalidades = Mortalidade.query.get_or_404(id)
        db.session.delete(mortalidades)
        current_app.logger.info(f"Deletando mortalidade id= {id}")
        
        db.session.commit()
        current_app.logger.info(f"Mortalidade deletada com sucesso id= {id}")
        
        return {"message": "Mortalidade removida com sucesso!"}