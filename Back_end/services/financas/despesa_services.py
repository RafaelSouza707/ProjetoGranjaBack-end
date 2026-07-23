from datetime import datetime

from sqlalchemy import extract, func

from helpers.database import db
from helpers.errors.exceptions import NotFoundError
from elastic.despesa_sync import deletar_index_despesa
from models.financas.despesa import Despesa
from models.granja.granja import Granja

class DespesaService:

    @staticmethod
    def listar(granja_id, pagina, per_page):
        return (
            db.session.query(Despesa)
            .join(Despesa.granja)
            .filter(Granja.id == granja_id)
            .order_by(Despesa.data.desc())
            .paginate(
                page=pagina,
                per_page=per_page,
                error_out=False
            )
        )


    @staticmethod
    def buscar_por_id(id):
        despesa = (
            db.session.query(Despesa)
            .filter(Despesa.id == id)
            .first()
        )

        if not despesa:
            raise NotFoundError("Despesa não encontrada")

        return despesa
    

    @staticmethod
    def maior_gasto_mes_granja(granja_id):
        hoje = datetime.now()

        maior_gasto = (
            db.session.query(Despesa)
            .join(Despesa.granja)
            .filter(
                extract("month", Despesa.data) == hoje.month,
                extract("year", Despesa.data) == hoje.year,
                Granja.id == granja_id,
            )
            .order_by(Despesa.valor.desc())
            .first()
        )

        return maior_gasto
    

    @staticmethod
    def total_gasto_mes_granja(granja_id):
        hoje = datetime.now()
        total = (
            db.session.query(
                func.sum(Despesa.valor)
            )
            .filter(Despesa.granja_id == granja_id)
            .filter(
                extract("month", Despesa.data) == hoje.month,
                extract("year", Despesa.data) == hoje.year,
            )
            .scalar()
        )

        return float(total or 0)


    @staticmethod
    def criar(data):
        nova_despesa = Despesa(**data)

        db.session.add(nova_despesa)
        db.session.flush()

        return nova_despesa


    @staticmethod
    def atualizar(despesa, data):
        for k, v in data.items():
            setattr(despesa, k, v)

        return despesa


    @staticmethod
    def deletar(despesa):
        db.session.delete(despesa)
        deletar_index_despesa(despesa.id)