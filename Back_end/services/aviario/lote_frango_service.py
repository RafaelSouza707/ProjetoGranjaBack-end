from helpers.database import db
from helpers.exceptions import NotFoundError
from models.aviario.lote_frangos import LoteFrango
from datetime import datetime
from models.aviario.mortalidade import Mortalidade
from models.aviario.status_lote_frango import StatusLoteFrango
from models.granja.usuario_granja import UsuarioGranja
from sqlalchemy import extract, func
from models.aviario.lote_frangos import LoteFrango
from models.granja.granja import Granja
from helpers.exceptions import NotFoundError

def normalizar(data):
    if "identificacao" in data and isinstance(data["identificacao"], str):
        data["identificacao"] = data["identificacao"].strip().lower()

class LoteFrangoService:

    @staticmethod
    def listar(granja_id):
        granjas = (
            db.session.query(LoteFrango)
            .join(LoteFrango.granja)
            .filter(
                Granja.id == granja_id
            )
            .all()
        )

        return granjas

    
    @staticmethod
    def buscar_por_id(id):
        registro = (db.session.get(LoteFrango, id))

        if not registro:
            raise NotFoundError("Registro não encontrado")
        
        return registro
    

    @staticmethod
    def mortalidade_lote_frango(granja_id):
        hoje = datetime.now()
        
        total = (
            db.session.query(
                func.sum(Mortalidade.quantidade_mortes)
            )
            .join(Mortalidade.lote_frango)
            .join(LoteFrango.granja)
            .filter(Granja.id == granja_id)
            .filter(
                extract("month", Mortalidade.data) == hoje.month,
                extract("year", Mortalidade.data) == hoje.year,
            )
            .scalar()
        )
        return int(total or 0)


    @staticmethod
    def total_aves_lote_frango(granja_id):
        total_vivos = (
            db.session.query(func.sum(LoteFrango.quantidade_atual))
            .join(LoteFrango.granja)
            .join(LoteFrango.status_lote_frango)
            .filter(
                Granja.id == granja_id,
                StatusLoteFrango.nome == "ativo"
            )
            .scalar()
        )

        return total_vivos or 0


    @staticmethod
    def baixa_quantidade_aves_lote_frango(granja_id):
        return (
            db.session.query(LoteFrango)
            .join(LoteFrango.granja)
            .filter(
                Granja.id == granja_id,
                LoteFrango.quantidade_inicial > 0,
                (LoteFrango.quantidade_atual / LoteFrango.quantidade_inicial) <= 0.4
            )
            .count()
        )
        

    @staticmethod
    def criar(data):
        normalizar(data)

        novo_registro = LoteFrango(**data)
        
        db.session.add(novo_registro)
        db.session.flush()

        return novo_registro
    

    @staticmethod
    def atualizar(registro, data):
        print(data, registro)
        for k, v in data.items():
            setattr(registro, k, v)

        return registro
    

    @staticmethod
    def deletar(registro):
        db.session.delete(registro)
        