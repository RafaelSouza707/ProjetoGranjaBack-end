from flask_restful import Resource
from flask import request, g
from helpers.validate_schema import validate_schema
from helpers.database.db_utils import session_scope
from middlewares.auth_middleware import token_required
from middlewares.permission_type import permissao_required
from helpers.enum_status_associado import StatusAssociacao

from services.usuarios.usuario_associacao_service import UsuarioAssociacaoService
from schemas.usuarios.usuario_associacao_schema import UsuarioAssociacaoSchema
from schemas.granja.granja_schema import GranjaSchema


schema = UsuarioAssociacaoSchema()
schemas = UsuarioAssociacaoSchema(many=True)
granja_schema = GranjaSchema()

class UsuarioAssociacaoResource(Resource):

    @token_required
    def get(self):
        user_id = g.user_id

        enviadas = UsuarioAssociacaoService.listar_associacao_enviadas(user_id)

        if enviadas:
            agrupado = {}

            for associacao, granja, role_nome in enviadas:

                if associacao.id not in agrupado:
                    dados = schema.dump(associacao)

                    dados["granjas"] = []

                    agrupado[associacao.id] = dados

                if granja:
                    dados_granja = granja_schema.dump(granja)
                    dados_granja["role"] = role_nome

                    agrupado[associacao.id]["granjas"].append(dados_granja)

            return {
                "papel": "REMETENTE",
                "dados": list(agrupado.values())
            }, 200

        recebidas = UsuarioAssociacaoService.listar_associacao_recebidas(user_id)

        if recebidas:
            agrupado = {}

            for associacao, granja, role_nome in recebidas:

                if associacao.id not in agrupado:
                    dados = schema.dump(associacao)

                    dados["granjas"] = []

                    agrupado[associacao.id] = dados

                if granja:
                    dados_granja = granja_schema.dump(granja)
                    dados_granja["role"] = role_nome

                    agrupado[associacao.id]["granjas"].append(dados_granja)

            return {
                "papel": "DESTINATARIO",
                "dados": list(agrupado.values())
            }, 200

        return {
            "papel": None,
            "dados": []
        }, 200


    @token_required
    def post(self):
        user_id = g.user_id

        json = request.get_json()
        email_destino = json["email"]
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
        registro = UsuarioAssociacaoService.buscar_por_id_associacao(associassao_id)
        
        match resposta:
            
            case StatusAssociacao.ACEITO.value:
                with session_scope():
                    UsuarioAssociacaoService.aceitar_associacao(registro)
                    return "Aceito com sucesso!", 201
            
            case StatusAssociacao.RECUSADO.value:
                with session_scope():
                    UsuarioAssociacaoService.recusar_associacao(registro)
                    return "Recusado com sucesso!", 201

            case StatusAssociacao.CANCELADO.value:
                with session_scope():
                    UsuarioAssociacaoService.cancelar_associacao(registro)
                    return "Cancelado com sucesso!", 201


    @token_required
    def delete(self, id):
        with session_scope():
            registro = UsuarioAssociacaoService.buscar_por_id_associacao(id)
            UsuarioAssociacaoService.deletar_associacao(registro)

        return "", 204