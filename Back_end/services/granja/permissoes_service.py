from helpers.database import db

from models.granja.usuario_granja import UsuarioGranja
from models.controle_banco_de_dados.role import Role
from models.controle_banco_de_dados.role_permissao import RolePermissao
from models.controle_banco_de_dados.permissoes import Permissao


class PermissoesService:

    @staticmethod
    def obter_contexto_usuario(user_id, granja_id):

        usuario_granja = (
            db.session.query(UsuarioGranja)
            .filter(
                UsuarioGranja.usuario_id == user_id,
                UsuarioGranja.granja_id == granja_id,
                UsuarioGranja.ativo == True
            )
            .first()
        )

        if usuario_granja is None:
            return None

        role = (
            db.session.query(Role)
            .filter(Role.id == usuario_granja.role_id)
            .first()
        )

        permissoes = (
            db.session.query(Permissao.nome)
            .join(
                RolePermissao,
                RolePermissao.permissao_id == Permissao.id
            )
            .filter(
                RolePermissao.role_id == usuario_granja.role_id
            )
            .all()
        )

        return {
            "role": role.nome,
            "permissoes": [p.nome for p in permissoes]
        }