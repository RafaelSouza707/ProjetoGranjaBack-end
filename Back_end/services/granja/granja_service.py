from helpers.database import db
from helpers.errors.exceptions import NotFoundError
from models.granja.granja import Granja
from models.granja.usuario_granja import UsuarioGranja
from helpers.errors.exceptions import NotFoundError
from services.granja.usuario_granja_service import UsuarioGranjaService
from seeds.seed_granja_tipos_status import criar_dados_padrao_granja
from models.controle_banco_de_dados.role import Role
from seeds.roles_permissoes import ROLES
from services.granja.permissoes_service import PermissoesService

class GranjaService:

    @staticmethod
    def listar(user_id):
        granjas = (
            db.session.query(Granja)
            .join(UsuarioGranja, UsuarioGranja.granja_id == Granja.id)
            .filter(
                UsuarioGranja.usuario_id == user_id,
                UsuarioGranja.ativo == True
            )
            .all()
        )

        resultado = []

        for granja in granjas:
            contexto = PermissoesService.obter_contexto_usuario(
                user_id,
                granja.id
            )

            resultado.append({
                "granja": granja,
                "contexto": contexto
            })

        return resultado

    
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
    def associar_granja(user_associado_id, granja_id, tipo_user):      
        role_master = Role.query.filter_by(nome=tipo_user).first()

        verificacao = (
            db.session.query(UsuarioGranja)
            .filter(
                UsuarioGranja.usuario_id == user_associado_id,
                UsuarioGranja.granja_id == granja_id,
            )
            .first()
        )

        if verificacao is not None:
            verificacao.role_id = role_master.id
            
            return verificacao

        resultado = UsuarioGranjaService.criar({
            "usuario_id": user_associado_id,
            "granja_id": granja_id,
            "role_id": role_master.id,
            "ativo": True
        })

        return resultado
    

    @staticmethod
    def desassociar_granja(usuario_id, granja_id):
        (
            db.session.query(UsuarioGranja)
            .filter(
                UsuarioGranja.usuario_id == usuario_id,
                UsuarioGranja.granja_id == granja_id
            )
            .delete(synchronize_session=False)
        )
        

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