from helpers.database import db
from helpers.errors.exceptions import NotFoundError
from models.aviario.tipo_racao import TipoRacao
from models.granja.granja import Granja


def normalizar(data):
    if "nome" in data and isinstance(data["nome"], str):
        data["nome"] = data["nome"].strip().lower()


class TipoRacaoService:

    @staticmethod
    def listar(granja_id):
        resultado = (
            db.session.query(TipoRacao)
            .join(TipoRacao.granja)
            .filter(Granja.id == granja_id)
            .all()
        )
        return resultado

    @staticmethod
    def buscar_por_id(id):
        registro = (
            db.session.query(TipoRacao)
            .filter(
                TipoRacao.id == id
            )
            .first()
        )
        if not registro:
            raise NotFoundError("Registro não encontrado")

        return registro

    @staticmethod
    def criar(data):
        normalizar(data)

        novo_registro = TipoRacao(**data)

        db.session.add(novo_registro)
        db.session.flush()

        return novo_registro

    @staticmethod
    def atualizar(registro, data):
        normalizar(data)

        for k, v in data.items():
            setattr(registro, k, v)

        return registro

    @staticmethod
    def deletar(registro):
        db.session.delete(registro)