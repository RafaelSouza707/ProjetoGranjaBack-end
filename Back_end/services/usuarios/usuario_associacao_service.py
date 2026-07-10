from helpers.database import db
from helpers.exceptions import NotFoundError
from models.usuarios.usuario import Usuario
from models.usuarios.usuario_associacao import UsuarioAssociacao
from helpers.enum_status_associado import StatusAssociacao

class UsuarioAssociacaoService:

    @staticmethod
    def listar_associacao_user(user_id):
        resultado = (
            db.session.query(UsuarioAssociacao)
            .filter(
                (UsuarioAssociacao.usuario_destino_id == user_id)
                |
                (UsuarioAssociacao.usuario_origem_id == user_id)
            )
            .all()
        )
        return resultado


    @staticmethod
    def pedir_associacao(origem, email_destino):
        destino = db.session.query(Usuario.id).filter(Usuario.email == email_destino).scalar()

        verificacao = (
            db.session.query(UsuarioAssociacao)
            .filter(
                (
                    (UsuarioAssociacao.usuario_origem_id == origem) &
                    (UsuarioAssociacao.usuario_destino_id == destino)
                ) 
                |
                (
                    (UsuarioAssociacao.usuario_destino_id == origem) &
                    (UsuarioAssociacao.usuario_origem_id == destino)
                )
            )
            .first()
        )

        if verificacao is None:
            novo = UsuarioAssociacao(
                usuario_origem_id=origem,
                usuario_destino_id=destino,
                status=StatusAssociacao.PENDENTE.value
            )
            db.session.add(novo)
            db.session.flush()

            return ("Pedido enviado")
        
        raise("Relação já existente")
    

    @staticmethod
    def aceitar_associacao(associassao_id):
        associacao = (
            db.session.query(UsuarioAssociacao)
            .filter(UsuarioAssociacao.id == associassao_id)
            .first()
        )

        if associacao is None:
            raise NotFoundError("Associação não encontrada")
        
        associacao.status = StatusAssociacao.ACEITO.value

        return ("Pedido aceito")
    

    @staticmethod
    def recusar_associacao(associassao_id):
        associacao = (
            db.session.query(UsuarioAssociacao)
            .filter(UsuarioAssociacao.id == associassao_id)
            .first()
        )

        if associacao is None:
            raise NotFoundError("Associação não encontrada")
        
        associacao.status = StatusAssociacao.RECUSADO.value

        return ("Pedido recusado")
    

    @staticmethod
    def cancelar_associacao(associassao_id):
        associacao = (
            db.session.query(UsuarioAssociacao)
            .filter(UsuarioAssociacao.id == associassao_id)
            .first()
        )

        if associacao is None:
            raise NotFoundError("Associação não encontrada")
        
        associacao.status = StatusAssociacao.CANCELADO.value

        return ("Pedido cancelado")