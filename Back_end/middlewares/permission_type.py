from functools import wraps
from flask import request, g
from helpers.exceptions import ForbiddenError
from services.granja.permissoes_service import PermissoesService


def permissao_required(permissao):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            contexto = PermissoesService.obter_contexto_usuario(
                g.user_id,
                request.args.get("granja_id", type=int)
            )

            if contexto is None:
                raise ForbiddenError("Usuário não pertence à granja.")

            if permissao not in contexto["permissoes"]:
                raise ForbiddenError("Sem permissão.")

            return func(*args, **kwargs)

        return wrapper

    return decorator