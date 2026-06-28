from helpers.database import db
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
    def listar_de_lote_frango(lote_frango_id, granja_id):
        resultados = (
            db.session.query(ConsumoLoteDiaria)
            .join(ConsumoLoteDiaria.lote_frango)
            .join(LoteFrango.granja)
            .filter(
                ConsumoLoteDiaria.lote_frango_id == lote_frango_id,
                Granja.id == granja_id
            )
            .all()
        )

        return resultados


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