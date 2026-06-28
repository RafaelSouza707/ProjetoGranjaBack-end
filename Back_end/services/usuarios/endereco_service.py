from helpers.database import db
from helpers.exceptions import NotFoundError
from models.usuarios.endereco import Endereco
from models.usuarios.usuario import Usuario

class EnderecoService:

    @staticmethod
    def listar(user_id):
        resultado = (
            db.session.query(Endereco)
            .join(Endereco.usuario)
            .filter(
                Usuario.id == user_id
            )
            .all()
        )

        return resultado
    
    
    @staticmethod
    def buscar_por_id(id, user_id):
        registro = (
            db.session.query(Endereco)
            .join(Endereco.usuario)
            .filter(
                Usuario.id == user_id,
                Endereco.id == id
            )
            .first()
        )

        if not registro:
            raise NotFoundError("Registro não encontrado")
        
        return registro
    

    @staticmethod
    def criar(data):
        novo_registro = Endereco(**data)
        
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