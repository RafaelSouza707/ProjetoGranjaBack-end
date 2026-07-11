from helpers.database import db
from helpers.exceptions import NotFoundError
from models.granja.usuario_granja import UsuarioGranja as Model
from models.controle_banco_de_dados.role import Role

class UsuarioGranjaService:

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
        novo_registro = Model(**data)
        
        db.session.add(novo_registro)
        db.session.flush()

        return novo_registro
    

    @staticmethod
    def atualizar(registro, data):
        for k, v in data.items():
            setattr(registro, k, v)

        return registro
    

    @staticmethod
    def deletar(registro):
        db.session.delete(registro)