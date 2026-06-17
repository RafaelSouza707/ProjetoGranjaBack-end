from helpers.database import db
from helpers.exceptions import NotFoundError
from models.financas.tipo_despesa import TipoDespesa as Tipo

class TipoDespesaService:

    @staticmethod
    def listar():
        return db.session.query(Tipo)
    

    @staticmethod
    def buscar_por_id(id):
        tipo = db.session.get(Tipo, id)
        if not tipo:
            raise NotFoundError("Tipo de despesa não encontrado")
        
        return tipo
    

    @staticmethod
    def criar(data):
        novo_tipo = Tipo(**data)

        db.session.add(novo_tipo)
        db.session.flush()

        return novo_tipo
    

    @staticmethod
    def atualizar(tipo, data):
        for k, v in data.items():
            setattr(tipo, k, v)

        return tipo
    

    @staticmethod
    def deletar(tipo):
        db.session.delete(tipo)