from helpers.database import db
from sqlalchemy import extract, func
from helpers.exceptions import NotFoundError
from models.aviario.lote_racao import LoteRacao
from models.granja.granja import Granja


class LoteRacaoService:

    @staticmethod
    def listar(granja_id):
        resultado = (
            db.session.query(LoteRacao)
            .join(LoteRacao.granja)
            .filter(Granja.id == granja_id)
            .all()
        )
        return resultado

    @staticmethod
    def buscar_por_id(id):
        registro = (
            db.session.query(LoteRacao)
            .filter(LoteRacao.id == id)
            .first()
        )

        if not registro:
            raise NotFoundError("Registro não encontrado")

        return registro


    @staticmethod
    def quantidade_total_racao_granja(granja_id):
        resultado = (
            db.session.query(func.sum(LoteRacao.quilos))
            .filter(
                LoteRacao.granja_id == granja_id
            )
            .scalar()
        )

        return resultado
    

    @staticmethod
    def quantidade_lotes_racao(granja_id):
        resultado = (
            db.session.query(func.count(LoteRacao.id))
            .filter(
                LoteRacao.granja_id == granja_id
            )
            .scalar()
        )

        return resultado
    

    @staticmethod
    def lote_menor_quantidade(granja_id):
        resultado = (
            db.session.query(LoteRacao)
            .filter(
                LoteRacao.granja_id == granja_id,
                LoteRacao.quilos > 0,
            )
            .order_by(LoteRacao.quilos.asc())
            .first()
        )
        return resultado


    @staticmethod
    def previsao_acabar(qtd_total_granja, consumo_diario):
        if qtd_total_granja > 0 and consumo_diario > 0:
            resultado = qtd_total_granja / consumo_diario
        else:
            return 0
        
        return int(resultado)

    
    @staticmethod
    def criar(data):
        novo_registro = LoteRacao(**data)

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