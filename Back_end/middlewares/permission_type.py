from functools import wraps
from flask import request, g
from helpers.exceptions import ForbiddenError
from services.granja.permissoes_service import PermissoesService


def permissao_required(*permissoes):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            granja_id = (
                kwargs.get("granja_id")
                or request.args.get("granja_id", type=int)
            )

            contexto = PermissoesService.obter_contexto_usuario(
                g.user_id,
                granja_id
            )

            if contexto is None:
                raise ForbiddenError("Usuário não pertence à granja.")

            if not any(
                permissao in contexto["permissoes"]
                for permissao in permissoes
            ):
                raise ForbiddenError("Sem permissão.")

            return func(*args, **kwargs)

        return wrapper

    return decorator