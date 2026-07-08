from helpers.database import db
from helpers.exceptions import NotFoundError
from models.granja.granja import Granja
from models.granja.usuario_granja import UsuarioGranja
from helpers.exceptions import NotFoundError
from services.granja.usuario_granja_service import UsuarioGranjaService
from seeds.seed_granja_tipos_status import criar_dados_padrao_granja
from models.controle_banco_de_dados.role import Role

class GranjaService:

    @staticmethod
    def listar(user_id):
        granjas = (
            db.session.query(Granja)
            .join(Granja.usuarios)
            .filter(
                UsuarioGranja.usuario_id == user_id
            )
            .all()
        )
    
        return granjas

    
    @staticmethod
    def buscar_por_id(id):
        granja = (
            db.session.query(Granja)
            .filter(
                Granja.id == id
            )
            .first()
        )
        if not granja:
            raise NotFoundError("Registro não encontrado")
        
        return granja
    

    @staticmethod
    def criar(data, user_id):
        granja = Granja(**data)
        
        db.session.add(granja)
        db.session.flush()

        role_master = Role.query.filter_by(nome="MASTER").first()

        criar_dados_padrao_granja(granja.id)

        UsuarioGranjaService.criar({
            "usuario_id": user_id,
            "granja_id": granja.id,
            "role_id": role_master.id,
            "ativo": True
        })


        return granja
    

    @staticmethod
    def atualizar(registro, data):
        for k, v in data.items():
            setattr(registro, k, v)

        return registro
    

    @staticmethod
    def deletar(registro):
        db.session.delete(registro)