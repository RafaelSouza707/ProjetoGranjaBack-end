from datetime import datetime
from helpers.database import db
from sqlalchemy import extract, func
from helpers.exceptions import NotFoundError
from models.financas.receita import Receita
from models.granja.granja import Granja


class ReceitaService:

    @staticmethod
    def listar(granja_id, pagina, per_page):
        return (
            db.session.query(Receita)
            .join(Receita.granja)
            .filter(Granja.id == granja_id)
            .order_by(Receita.data.desc())
            .paginate(
                page=pagina,
                per_page=per_page,
                error_out=False
            )
        )
    

    @staticmethod
    def buscar_por_id(id):
        registro = (
            db.session.query(Receita)
            .filter(Receita.id == id)
            .first()
        )
        if not registro:
            raise NotFoundError("Registro não encontrado")

        return registro
    

    @staticmethod
    def card_receita_valor_total_receita_mes_graja(granja_id):
        hoje = datetime.now()
        
        total_vendido = (
            db.session.query(func.sum(Receita.valor))
            .filter(
                extract("month", Receita.data) == hoje.month,
                extract("year", Receita.data) == hoje.year,
                Receita.granja_id == granja_id
            )
            .scalar()
        )

        return float(total_vendido or 0)
    


    @staticmethod
    def card_receita_total_receitas_mes_granja(granja_id):
        hoje = datetime.now()

        total_vendas = (
            db.session.query(func.count(Receita.id))
            .filter(
                extract("month", Receita.data) == hoje.month,
                extract("year", Receita.data) == hoje.year,
                Receita.granja_id == granja_id
            )
            .scalar()
        )
        return total_vendas or 0
    


    @staticmethod
    def card_receita_maior_receita_mes(granja_id):
        hoje = datetime.now()

        maior_venda = (
            db.session.query(Receita)
            .filter(
                extract("month", Receita.data) == hoje.month,
                extract("year", Receita.data) == hoje.year,
                Receita.granja_id == granja_id
            )
            .order_by(Receita.valor.desc())
            .first()
        )
        return maior_venda


    @staticmethod
    def criar(data):
        novo_registro = Receita(**data)

        db.session.add(novo_registro)
        db.session.flush()

        return novo_registro
    

    @staticmethod
    def atualizar(registro, data):
        for k, v in data.items():
            setattr(registro, k, v)

        return registro
    

    @staticmethod
    def deletar(registro):
        db.session.delete(registro)