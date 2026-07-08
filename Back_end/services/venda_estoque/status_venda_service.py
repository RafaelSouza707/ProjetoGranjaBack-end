from helpers.database import db
from helpers.exceptions import NotFoundError
from models.venda.tipo_venda import TipoVenda
from models.granja.granja import Granja

def normalizar(data):
    if "nome" in data and isinstance(data["nome"], str):
        data["nome"] = data["nome"].strip().lower()

class StatusVendaService:

    @staticmethod
    def listar(granja_id):
        return (
            db.session.query(TipoVenda)
            .join(TipoVenda.granja)
            .filter(Granja.id == granja_id)
            .all()
        )
    
    
    @staticmethod
    def buscar_por_id(id):
        registro = db.session.get(TipoVenda, id)
        if not registro:
            raise NotFoundError("Registro não encontrado")
        
        return registro
    

    @staticmethod
    def criar(data):
        normalizar(data)

        novo_registro = TipoVenda(**data)
        
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