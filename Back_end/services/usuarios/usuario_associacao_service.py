from helpers.database import db
from helpers.exceptions import NotFoundError
from models.usuarios.usuario import Usuario
from models.usuarios.usuario_associacao import UsuarioAssociacao
from helpers.enum_status_associado import StatusAssociacao
from models.granja.usuario_granja import UsuarioGranja
from models.granja.granja import Granja
from models.granja.usuario_granja import UsuarioGranja

class UsuarioAssociacaoService:

    @staticmethod
    def listar_associacao_enviadas(user_id):
        associacoes = (
            db.session.query(UsuarioAssociacao, Granja)
            .join(UsuarioGranja, UsuarioGranja.granja_id == Granja.id) 
            .join(Usuario, Usuario.id == UsuarioGranja.usuario_id)
            .filter(
                UsuarioAssociacao.usuario_origem_id == user_id,
                UsuarioGranja.usuario_id == UsuarioAssociacao.usuario_destino_id
            )
            .all()
        )
        return associacoes


    @staticmethod
    def listar_associacao_recebidas(user_id):
        resultado = (
            db.session.query(UsuarioAssociacao)
            .filter(           
                (UsuarioAssociacao.usuario_destino_id == user_id)
            )
            .all()
        )
        
        return resultado


    @staticmethod
    def buscar_por_id_associacao(id):
        resultado = db.session.get(UsuarioAssociacao, id)
        if not resultado:
            raise NotFoundError("Registro não encontrado")
        
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
    def aceitar_associacao(registro):
        registro.status = StatusAssociacao.ACEITO.value

        return ("Pedido aceito")
    

    @staticmethod
    def recusar_associacao(registro):
        registro.status = StatusAssociacao.RECUSADO.value

        return ("Pedido recusado")
    

    @staticmethod
    def cancelar_associacao(registro):
        registro.status = StatusAssociacao.CANCELADO.value

        return ("Pedido cancelado")
    

    @staticmethod
    def deletar_associacao(registro):
        (
            db.session.query(UsuarioGranja)
            .filter(
                UsuarioGranja.usuario_id == registro.usuario_destino_id
            )
            .delete(synchronize_session=False)
        )
        db.session.delete(registro)

        return ("Associação excluida")