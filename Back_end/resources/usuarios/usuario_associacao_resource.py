from flask_restful import Resource
from flask import request, g
from helpers.validate_schema import validate_schema
from helpers.db_utils import session_scope
from middlewares.auth_middleware import token_required
from helpers.enum_status_associado import StatusAssociacao

from services.usuarios.usuario_associacao_service import UsuarioAssociacaoService
from schemas.usuarios.usuario_associacao_schema import UsuarioAssociacaoSchema

schema = UsuarioAssociacaoSchema()
schemas = UsuarioAssociacaoSchema(many=True)

class UsuarioAssociacaoResource(Resource):

    @token_required
    def get(self):
        user_id = g.user_id

        resultado = schemas.dump(UsuarioAssociacaoService.listar_associacao_user(user_id))

        return resultado, 200


    @token_required
    def post(self):
        user_id = g.user_id

        json = request.get_json()
        print(json)
        email_destino = json["email"]
        print(email_destino)
        with session_scope():
            resultado = UsuarioAssociacaoService.pedir_associacao(user_id, email_destino)
            resultado_final = schemas.dump(resultado)

        return resultado_final, 201
    

    @token_required
    def put(self):
        user_id = g.user_id

        json = request.get_json()
        resposta = json.get("resposta")
        associassao_id = json.get("id")
        
        match resposta:
            
            case StatusAssociacao.ACEITO.value:
                with session_scope():
                    UsuarioAssociacaoService.aceitar_associacao(user_id)
            
            case StatusAssociacao.RECUSADO.value:
                with session_scope():
                    UsuarioAssociacaoService.recusar_associacao(associassao_id)

            case StatusAssociacao.CANCELADO.value:
                with session_scope():
                    UsuarioAssociacaoService.cancelar_associacao(associassao_id)