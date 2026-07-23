from helpers.database import db
from helpers.errors.exceptions import NotFoundError
from models.usuarios.cliente_schema import Cliente
from models.granja.granja import Granja
from models.granja.usuario_granja import UsuarioGranja


class ClienteService:

    @staticmethod
    def listar(user_id):
        resultados = (
            db.session.query(Cliente)
            .join(Cliente.granja)
            .join(Granja.usuarios)
            .filter(
                UsuarioGranja.usuario_id == user_id
            )
            .all()
        )

        return resultados
    
    
    @staticmethod
    def buscar_por_id(id):
        registro = (
            db.session.query(Cliente)
            .filter(
                Cliente.id == id
            )
            .first()
        )
        
        if not registro:
            raise NotFoundError("Registro não encontrado")
        
        return registro
    

    @staticmethod
    def criar(data):
        novo_registro = Cliente(**data)
        
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