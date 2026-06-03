from helpers.database import db
from helpers.exceptions import NotFoundError
from models.financas.despesa import Despesa

class DespesaService:

    @staticmethod
    def listar():
        return db.session.query(Despesa).all()
    
    
    @staticmethod
    def buscar_por_id(id):
        depesa = db.session.get(Despesa, id)
        if not depesa:
            raise NotFoundError("Despesa não encontrado")
        
        return depesa
    

    @staticmethod
    def criar(data):
        nova_despesa = Despesa(**data)
        
        db.session.add(nova_despesa)
        db.session.flush()

        return nova_despesa
    

    @staticmethod
    def atualizar(depesa, data):
        for k, v in data.items():
            setattr(depesa, k, v)

        return depesa
    

    @staticmethod
    def delete(depesa):
        db.session.delete(depesa)