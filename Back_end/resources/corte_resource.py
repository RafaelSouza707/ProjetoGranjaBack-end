from flask import request, current_app
from flask_restful import Resource
from helpers.database import db
from models.lote_frangos import LoteFrango
from models.corte import Corte
from schemas.corte_schema import CorteSchema

corte_schema = CorteSchema()
cortes_schema = CorteSchema(many=True)


class CorteResource(Resource):

    def get(self, id=None):
        if id:
            corte = Corte.query.get(id)
            
            if not corte:
                current_app.logger.warning(f"Corte id = {id} não encontrado")
                return {"message": f"Corte id = {id} não encontrado"}, 404
            
            current_app.logger.info(f"Corte id = {id} encontrado com sucesso")
            return corte_schema.dump(corte), 200
        
        cortes = Corte.query.all()
        current_app.logger.info("Buscando todos os cortes")
        return cortes_schema.dump(cortes), 200
    
    
    def post(self):
        json_data = request.get_json() 
        data = corte_schema.load(json_data) 
        
        lote = LoteFrango.query.get(data["id_lote_frango"]) 
        if not lote:
            return {"erro": "Lote de frango não existe"}, 400
        
        novo_corte = Corte(**data) 
        db.session.add(novo_corte) 
        current_app.logger.info("Novo corte sendo inserido")
        
        db.session.commit()
        current_app.logger.info(f"Corte inserido com sucesso {novo_corte}")
        
        return corte_schema.dump(novo_corte), 201
    
    def put(self, id):
        corte = Corte.query.get_or_404(id) 
        json_data = request.get_json() 
        data = corte_schema.load(json_data) 
        
        lote = LoteFrango.query.get(data["id_lote_frango"]) 
        if not lote:
            return {"erro": "Lote de frango não existe"}, 400
        
        current_app.logger.info(f"Atualizando corte id= {id}")
        
        corte.lote_frango_id = data["id_lote_frango"] 
        corte.data = data["data"] 
        corte.peso = data["peso"]
        
        db.session.commit()
        
        current_app.logger.info(f"Corte atualizado com sucesso id= {id}")
        
        return corte_schema.dump(corte), 200
    
    def delete(self, id):
        corte = Corte.query.get_or_404(id) 
        db.session.delete(corte) 
        db.session.commit() 
        current_app.logger.info(f"Corte id= {id} deletado com sucesso")
        
        return {"message": "Corte deletado com sucesso"}, 200