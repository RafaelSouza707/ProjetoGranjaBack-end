from helpers.database import db
from helpers.errors.exceptions import NotFoundError
from models.financas.tipo_despesa import TipoDespesa
from models.granja.granja import Granja


def normalizar(data):
    if "nome" in data and isinstance(data["nome"], str):
        data["nome"] = data["nome"].strip().lower()


class TipoDespesaService:

    @staticmethod
    def listar(granja_id):
        resultado = (
            db.session.query(TipoDespesa)
            .join(TipoDespesa.granja)
            .filter(Granja.id == granja_id)
            .all()
        )
        return resultado

    @staticmethod
    def buscar_por_id(id):
        tipo = (
            db.session.query(TipoDespesa)
            .filter(TipoDespesa.id == id)
            .first()
        )
        if not tipo:
            raise NotFoundError("Tipo de despesa não encontrado")

        return tipo

    @staticmethod
    def criar(data):
        normalizar(data)

        novo_tipo = TipoDespesa(**data)

        db.session.add(novo_tipo)
        db.session.flush()

        return novo_tipo

    @staticmethod
    def atualizar(tipo, data):
        normalizar(data)

        for k, v in data.items():
            setattr(tipo, k, v)

        return tipo

    @staticmethod
    def deletar(tipo):
        db.session.delete(tipo)