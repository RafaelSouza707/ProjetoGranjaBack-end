from datetime import datetime

from sqlalchemy import extract, func

from helpers.database import db
from helpers.exceptions import NotFoundError
from elastic.despesa_sync import deletar_index_despesa
from models.financas.despesa import Despesa
from models.granja.granja import Granja
from models.granja.usuario_granja import UsuarioGranja

class DespesaService:

    @staticmethod
    def listar(granja_id):
        resultado = (
            db.session.query(Despesa)
            .join(Despesa.granja)
            .filter(Granja.id == granja_id)
            .all()
        )

        return resultado


    @staticmethod
    def buscar_por_id(id, granja_id):
        despesa = (
            db.session.query(Despesa)
            .join(Despesa.granja)
            .filter(Granja.id == granja_id, Despesa.id == id)
            .first()
        )

        if not despesa:
            raise NotFoundError("Despesa não encontrada")

        return despesa


    @staticmethod
    def maior_gasto_mes(granja_id=None):
        hoje = datetime.now()

        query = (
            db.session.query(Despesa)
            .join(Despesa.granja)
            .filter(
                extract("month", Despesa.data) == hoje.month,
                extract("year", Despesa.data) == hoje.year,
            )
        )

        if granja_id is not None:
            query = query.filter(Granja.id == granja_id)

        maior_gasto = query.order_by(Despesa.valor.desc()).first()

        if not maior_gasto: 
            return None

        return {
            "valor": float(maior_gasto.valor),
            "tipo_despesa":maior_gasto.tipo_despesa.nome
        }
    

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
    def deletar(despesa):
        db.session.delete(despesa)
        deletar_index_despesa(despesa.id)