from helpers.database import db
from helpers.exceptions import NotFoundError
from models.estoque.producao import Producao
from models.aviario.lote_frangos import LoteFrango


class ProducaoService:

    @staticmethod
    def listar(granja_id):
        resultados = (
            db.session.query(Producao)
            .join(Producao.lote_frango)
            .filter(LoteFrango.granja_id == granja_id)
            .all()
        )

        return resultados
    
    
    @staticmethod
    def listar_do_lote_frango(lote_frango_id):
        resultados = (
            db.session.query(Producao)
            .filter(Producao.lote_frango_id == lote_frango_id)
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
        data.pop("lote_frango", None)
        data.pop("produto", None)
        for k, v in data.items():
            setattr(registro, k, v)

        return registro
    

    @staticmethod
    def deletar(registro):
        db.session.delete(registro)