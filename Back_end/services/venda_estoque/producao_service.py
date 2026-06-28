from helpers.database import db
from helpers.exceptions import NotFoundError
from models.venda_estoque.producao import Producao
from models.aviario.lote_frangos import LoteFrango
from models.granja.granja import Granja


class ProducaoService:

    @staticmethod
    def listar(granja_id):
        resultados = (
            db.session.query(Producao)
            .join(Producao.lote_frango)
            .join(LoteFrango.granja)
            .filter(Granja.id == granja_id)
            .all()
        )

        return resultados

    @staticmethod
    def buscar_por_id(id):
        registro = db.session.get(Producao, id)

        if not registro:
            raise NotFoundError("Registro não encontrado")

        return registro

    @staticmethod
    def criar(data):
        novo_registro = Producao(**data)

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