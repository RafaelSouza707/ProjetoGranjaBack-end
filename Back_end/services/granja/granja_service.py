from helpers.database import db
from helpers.exceptions import NotFoundError
from models.granja.granja import Granja
from models.granja.usuario_granja import UsuarioGranja
from helpers.exceptions import NotFoundError
from services.granja.usuario_granja_service import UsuarioGranjaService

class GranjaService:

    @staticmethod
    def listar(user_id):
        resultados = (
            db.session.query(Granja)
            .join(Granja.usuarios)
            .filter(
                UsuarioGranja.usuario_id == user_id
            )
            .all()
        )
        print("LISTAR: ", resultados)

        return resultados

    
    @staticmethod
    def buscar_por_id(id, user_id):
        registro = db.session.query(Granja).join(Granja.usuarios).filter(UsuarioGranja.usuario_id == user_id).first()
        if not registro:
            raise NotFoundError("Registro não encontrado")
        
        return registro
    

    @staticmethod
    def criar(data, user_id):
        novo_registro = Granja(**data)
        
        db.session.add(novo_registro)
        db.session.flush()

        UsuarioGranjaService.criar({
            "usuario_id": user_id,
            "granja_id": novo_registro.id,
            "cargo_id": 1,
            "ativo": True
        })
        return novo_registro
    

    @staticmethod
    def atualizar(registro, data):
        for k, v in data.items():
            setattr(registro, k, v)

        return registro
    

    @staticmethod
    def deletar(registro):
        db.session.delete(registro)