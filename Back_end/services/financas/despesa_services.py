from datetime import datetime

from sqlalchemy import extract, func

from helpers.database import db
from helpers.exceptions import NotFoundError
from models.financas.despesa import Despesa
from models.financas.tipo_despesa import TipoDespesa


class DespesaService:

    @staticmethod
    def listar():
        return db.session.query(Despesa).all()


    @staticmethod
    def buscar_por_id(id):
        despesa = db.session.get(Despesa, id)

        if not despesa:
            raise NotFoundError("Despesa não encontrada")

        return despesa


    @staticmethod
    def maior_gasto_mes():
        hoje = datetime.now()

        maior_gasto = (
            db.session.query(Despesa)
            .filter(
                extract("month", Despesa.data) == hoje.month,
                extract("year", Despesa.data) == hoje.year,
            )
            .order_by(Despesa.valor.desc())
            .first()
        )

        if not maior_gasto: 
            return None

        return (
            maior_gasto.valor,
            maior_gasto.tipo_despesa
        )

    
    @staticmethod
    def total_gasto_mes():
        hoje = datetime.now()
        
        total = (
            db.session.query(
                func.sum(Despesa.valor)
            )
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
    def delete(despesa):
        db.session.delete(despesa)