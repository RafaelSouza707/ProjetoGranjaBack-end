from helpers.database import db
from datetime import datetime
from sqlalchemy import extract, func
from helpers.exceptions import NotFoundError
from models.aviario.consumo_lote_diaria import ConsumoLoteDiaria
from models.aviario.lote_frangos import LoteFrango
from models.granja.granja import Granja

class ConsumoLoteDiariaService:

    @staticmethod
    def listar(granja_id):
        resultados = (
            db.session.query(ConsumoLoteDiaria)
            .join(ConsumoLoteDiaria.lote_frango)
            .join(LoteFrango.granja)
            .filter(
                Granja.id == granja_id
            )
            .all()
        )
        return resultados
    

    @staticmethod
    def listar_de_lote_frango(lote_frango_id):
        resultados = (
            db.session.query(ConsumoLoteDiaria)
            .filter(
                ConsumoLoteDiaria.lote_frango_id == lote_frango_id,
            )
            .all()
        )
        print(resultados)

        return resultados


    @staticmethod
    def consumo_mensal(granja_id):
        hoje = datetime.now()

        resultado = (
            db.session.query(func.sum(ConsumoLoteDiaria.quilos))
            .join(ConsumoLoteDiaria.lote_frango)
            .filter(
                extract("month", ConsumoLoteDiaria.data) == hoje.month,
                extract("year", ConsumoLoteDiaria.data) == hoje.year,
                LoteFrango.granja_id == granja_id
            )
            .scalar()
        )

        return float(resultado or 0)
    

    @staticmethod
    def consumo_mensal_diaria(consumo_mensal):
        hoje = datetime.now()
        consumo_diario_medio = consumo_mensal / hoje.day

        return float(consumo_diario_medio)


    @staticmethod
    def buscar_por_id(id):
        registro = db.session.get(ConsumoLoteDiaria, id)

        if not registro:
            raise NotFoundError("Registro não encontrado")
        
        return registro
    

    @staticmethod
    def criar(data):
        novo_registro = ConsumoLoteDiaria(**data)
        
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