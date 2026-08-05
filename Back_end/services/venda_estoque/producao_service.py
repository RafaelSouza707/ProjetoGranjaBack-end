from helpers.database import db
from helpers.errors.exceptions import NotFoundError
from models.estoque.producao import Producao
from models.aviario.lote_frangos import LoteFrango
from helpers.database.query_builder import QueryBuilder


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
    def listar_do_lote_frango(lote_frango_id, pagina, per_page):
        query = (
            db.session.query(Producao)
            .filter(Producao.lote_frango_id == lote_frango_id)
        )

        query = QueryBuilder(
            Producao,
            query
        ).build().order_by(Producao.data.desc())

        return query.paginate(
            page=pagina,
            per_page=per_page,
            error_out=False
        )
    

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