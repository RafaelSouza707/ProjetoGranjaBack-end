from helpers.database import db
from helpers.exceptions import NotFoundError
from models.aviario.mortalidade import Mortalidade
from models.aviario.lote_frangos import LoteFrango
from models.granja.granja import Granja
from models.granja.usuario_granja import UsuarioGranja
from services.aviario.lote_frango_service import LoteFrangoService

class MortalidadeService:

    @staticmethod
    def listar(granja_id):
        resultado = (
            db.session.query(Mortalidade)
            .join(Mortalidade.lote_frango)
            .join(LoteFrango.granja)
            .filter(Granja.id == granja_id)
            .all()
        )
        return resultado

    @staticmethod
    def listar_de_lote_frango(lote_frango_id, granja_id):
        resultado = (
            db.session.query(Mortalidade)
            .join(Mortalidade.lote_frango)
            .join(LoteFrango.granja)
            .filter(Granja.id == granja_id, LoteFrango.id == lote_frango_id)
            .all()
        )

        return resultado

    @staticmethod
    def buscar_por_id(id, granja_id=None):
        query = (
            db.session.query(Mortalidade)
            .join(Mortalidade.lote_frango)
            .join(LoteFrango.granja)
        )

        if granja_id is not None:
            query = query.filter(Granja.id == granja_id)

        resultado = query.filter(Mortalidade.id == id).first()

        if not resultado:
            raise NotFoundError("Registro não encontrado")

        return resultado

    @staticmethod
    def criar(data, granja_id):
        lote_frango = LoteFrangoService.buscar_por_id(data["lote_frango_id"])

        novo_registro = Mortalidade(**data)

        lote_frango.quantidade_atual -= data["quantidade_mortes"]

        db.session.add(novo_registro)
        db.session.flush()

        return novo_registro

    @staticmethod
    def atualizar(registro, data, granja_id):
        lote_frango = LoteFrangoService.buscar_por_id(registro.lote_frango_id)

        mortes_antigas = registro.quantidade_mortes
        mortes_novas = data["quantidade_mortes"]

        diferenca = mortes_novas - mortes_antigas

        lote_frango.quantidade_atual -= diferenca

        for k, v in data.items():
            setattr(registro, k, v)

        return registro

    @staticmethod
    def deletar(registro, granja_id):
        lote_frango = LoteFrangoService.buscar_por_id(registro.lote_frango_id)

        lote_frango.quantidade_atual -= registro.quantidade_mortes

        db.session.delete(registro)