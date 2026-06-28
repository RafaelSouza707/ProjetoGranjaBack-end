from helpers.database import db
from helpers.exceptions import NotFoundError
from models.venda_estoque.tipo_movimentacao import TipoMovimentacao as Model

def normalizar(data):
    if "nome" in data and isinstance(data["nome"], str):
        data["nome"] = data["nome"].strip().lower()

class TipoMovimentacaoService:

    @staticmethod
    def listar():
        return db.session.query(Model).all()
    
    
    @staticmethod
    def buscar_por_id(id):
        registro = db.session.get(Model, id)
        if not registro:
            raise NotFoundError("Registro não encontrado")
        
        return registro
    

    @staticmethod
    def criar(data):
        normalizar(data)

        novo_registro = Model(**data)
        
        db.session.add(novo_registro)
        db.session.flush()

        return novo_registro
    

    @staticmethod
    def atualizar(registro, data):
        normalizar(data)
        
        for k, v in data.items():
            setattr(registro, k, v)

        return registro
    

    @staticmethod
    def deletar(registro):
        db.session.delete(registro)