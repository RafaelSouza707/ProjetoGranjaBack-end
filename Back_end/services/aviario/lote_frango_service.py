from helpers.database import db
from helpers.exceptions import NotFoundError
from models.aviario.lote_frangos import LoteFrango
from datetime import datetime
from models.aviario.mortalidade import Mortalidade
from models.aviario.status_lote_frango import StatusLoteFrango
from sqlalchemy import extract, func
from models.aviario.lote_frangos import LoteFrango
from helpers.exceptions import NotFoundError
from models.aviario.consumo_lote_diaria import ConsumoLoteDiaria

def normalizar(data):
    if "identificacao" in data and isinstance(data["identificacao"], str):
        data["identificacao"] = data["identificacao"].strip().lower()

class LoteFrangoService:

    @staticmethod
    def listar(granja_id):
        resultado = (
            db.session.query(LoteFrango)
            .filter(
                LoteFrango.granja_id == granja_id
            )
            .order_by(LoteFrango.identificacao.desc())
            .all()
        )

        return resultado

    
    @staticmethod
    def buscar_por_id(id):
        registro = (db.session.get(LoteFrango, id))

        if not registro:
            raise NotFoundError("Registro não encontrado")
        
        return registro
    

    @staticmethod
    def mortalidade_granja_mes(granja_id):
        hoje = datetime.now()
        
        total = (
            db.session.query(
                func.sum(Mortalidade.quantidade_mortes)
            )
            .join(Mortalidade.lote_frango)
            .filter(
                extract("month", Mortalidade.data) == hoje.month,
                extract("year", Mortalidade.data) == hoje.year,
                LoteFrango.granja_id == granja_id
            )
            .scalar()
        )
        return total or 0
    

    @staticmethod
    def mortalidade_lote_mes(lote_frango_id):
        hoje = datetime.now()

        total = (
            db.session.query(
                func.sum(Mortalidade.quantidade_mortes)
            )
            .filter(
                extract("month", Mortalidade.data) == hoje.month,
                extract("year", Mortalidade.data) == hoje.year,
                Mortalidade.lote_frango_id == lote_frango_id
            )
            .scalar()
        )
        return total or 0


    @staticmethod
    def total_aves_granja(granja_id):
        total_vivos = (
            db.session.query(func.sum(LoteFrango.quantidade_atual))
            .join(LoteFrango.status_lote_frango)
            .filter(
                LoteFrango.granja_id == granja_id,
                StatusLoteFrango.nome == "ativo"
            )
            .scalar()
        )
        return total_vivos or 0
    

    @staticmethod
    def total_aves_lote_frango(lote_frango_id):
        total_vivos = (
            db.session.query(LoteFrango.quantidade_atual)
            .filter(
                LoteFrango.id == lote_frango_id,
            )
            .scalar()
        )
        return total_vivos or 0


    @staticmethod
    def baixa_quantidade_aves_granja(granja_id):
        return (
            db.session.query(LoteFrango)
            .filter(
                LoteFrango.granja_id == granja_id,
                LoteFrango.quantidade_inicial > 0,
                (LoteFrango.quantidade_atual / LoteFrango.quantidade_inicial) <= 0.4
            )
            .count()
        )
    

    @staticmethod
    def consumo_total_granja(granja_id):
        return (
            db.session.query(
                func.sum(ConsumoLoteDiaria.quilos)
            )
            .join(ConsumoLoteDiaria.lote_frango)
            .filter(
                LoteFrango.granja_id == granja_id
            )
            .scalar() or None
        )
    

    @staticmethod
    def criar(data):
        normalizar(data)

        if data.get("status"):
            data["status_lote_frango_id"] = data["status"]["id"]

        data.pop("status", None)

        novo_registro = LoteFrango(**data)
        
        db.session.add(novo_registro)
        db.session.flush()

        return novo_registro
    

    @staticmethod
    def atualizar(registro, data):
        data.pop("status_lote_frango", None)
        for k, v in data.items():
            setattr(registro, k, v)

        return registro
    

    @staticmethod
    def deletar(registro):
        db.session.delete(registro)
        