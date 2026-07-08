from helpers.database import db
from models.granja.usuario_granja import UsuarioGranja
from models.granja.granja import Granja
from helpers.exceptions import NotFoundError

class ValidarAcessoGranja():

    @staticmethod
    def validar_acesso_granja(user_id, granja_id):
        pertence = (
            db.session.query(UsuarioGranja)
            .filter(
                UsuarioGranja.usuario_id == user_id,
                UsuarioGranja.granja_id == granja_id,
                UsuarioGranja.ativo == True
            )
            .first()
        )

        if not pertence:
            raise NotFoundError("Granja não encontrada")