from helpers.database import db
from helpers.exceptions import NotFoundError
from models.controle_banco_de_dados.cargos import Cargo
from models.granja.usuario_granja import UsuarioGranja

def normalizar(data):
    if "nome" in data and isinstance(data["nome"], str):
        data["nome"] = data["nome"].strip().lower()


class CargoService:

    @staticmethod
    def listar(user_id):
        resultado = (
            db.session.query(Cargo)
            .join(Cargo.usuarios)
            .filter(
                UsuarioGranja.usuario_id == user_id
            )
            .all()
        )
        return resultado
    
    
    @staticmethod
    def buscar_por_id(id, user_id):
        registro = (
            db.session.query(Cargo)
            .join(Cargo.usuarios)
            .filter(
                UsuarioGranja.usuario_id == user_id,
                Cargo.id == id
            )
            .first()
        )
        if not registro:
            raise NotFoundError("Registro não encontrado")
        
        return registro
    

    @staticmethod
    def criar(data):
        normalizar(data)

        novo_registro = Cargo(**data)
        
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