from helpers.database import db

from models.controle_banco_de_dados.role import Role
from models.controle_banco_de_dados.permissoes import Permissao
from models.controle_banco_de_dados.role_permissao import RolePermissao

from seeds.roles_permissoes import (
    ROLES,
    PERMISSOES,
    ROLE_PERMISSOES
)


def seed_rbac():

    for nome in ROLES:
        existe = Role.query.filter_by(nome=nome).first()

        if not existe:
            db.session.add(Role(nome=nome))

    db.session.flush()


    for nome in PERMISSOES:
        existe = Permissao.query.filter_by(nome=nome).first()

        if not existe:
            db.session.add(Permissao(nome=nome))

    db.session.flush()

    roles = {
        role.nome: role
        for role in Role.query.all()
    }

    permissoes = {
        permissao.nome: permissao
        for permissao in Permissao.query.all()
    }


    for role_nome, permissoes_lista in ROLE_PERMISSOES.items():

        role = roles[role_nome]

        for permissao_nome in permissoes_lista:

            permissao = permissoes[permissao_nome]

            existe = RolePermissao.query.filter_by(
                role_id=role.id,
                permissao_id=permissao.id
            ).first()

            if not existe:
                db.session.add(
                    RolePermissao(
                        role_id=role.id,
                        permissao_id=permissao.id
                    )
                )

    db.session.commit()

    print("RBAC criado com sucesso.")