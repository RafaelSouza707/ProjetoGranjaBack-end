from helpers.database import db
from helpers.errors.exceptions import NotFoundError
from models.aviario.mortalidade import Mortalidade
from models.aviario.lote_frangos import LoteFrango
from models.granja.granja import Granja
from models.aviario.lote_frangos import LoteFrango
from services.aviario.lote_frango_service import LoteFrangoService
from sqlalchemy import extract, func

class MortalidadeService:

    @staticmethod
    def listar(granja_id, pagina, per_page):
        resultado = (
            db.session.query(Mortalidade)
            .join(Mortalidade.lote_frango)
            .join(LoteFrango.granja)
            .filter(Granja.id == granja_id)
            .order_by(Mortalidade.data.desc())
            .paginate(
                page=pagina,
                per_page=per_page,
                error_out=False
            )
        )
        return resultado


    @staticmethod
    def grafico_mortalidade_granja(granja_id):
        resultados = (
            db.session.query(
                extract('year', Mortalidade.data).label('ano'),
                extract('month', Mortalidade.data).label('mes'),
                func.sum(Mortalidade.quantidade_mortes).label('quantidade')
            )
            .join(Mortalidade.lote_frango)
            .filter(LoteFrango.granja_id == granja_id)
            .group_by('ano', 'mes')
            .order_by('ano', 'mes')
            .all()
        )

        dados_formatados = []
        for ano, mes, quantidade in resultados:
            nome_mes = f"{int(mes):02d}/{int(ano)}"
            dados_formatados.append({
                "mes": nome_mes,
                "quantidade": int(quantidade or 0)
            })

        return dados_formatados
    

    @staticmethod
    def listar_de_lote_frango(lote_frango_id, pagina, per_page):
        resultado = (
            db.session.query(Mortalidade)
            .join(Mortalidade.lote_frango)
            .join(LoteFrango.granja)
            .filter(LoteFrango.id == lote_frango_id)
            .order_by(Mortalidade.data.desc())
            .paginate(
                page=pagina,
                per_page=per_page,
                error_out=False
            )
        )

        if not resultado:
            raise NotFoundError("Registros de mortalidade não encotrados")

        return resultado

    @staticmethod
    def buscar_por_id(id):
        resultado = (
            db.session.query(Mortalidade)
            .filter(Mortalidade.id == id)
            .first()
        )
        return resultado

    @staticmethod
    def criar(data):
        lote_frango = LoteFrangoService.buscar_por_id(data["lote_frango_id"])

        novo_registro = Mortalidade(**data)

        lote_frango.quantidade_atual -= data["quantidade_mortes"]

        db.session.add(novo_registro)
        db.session.flush()

        return novo_registro

    @staticmethod
    def atualizar(registro, data):
        lote_frango = LoteFrangoService.buscar_por_id(registro.lote_frango_id)

        mortes_antigas = registro.quantidade_mortes
        mortes_novas = data["quantidade_mortes"]

        diferenca = mortes_novas - mortes_antigas

        lote_frango.quantidade_atual -= diferenca

        for k, v in data.items():
            setattr(registro, k, v)

        return registro

    @staticmethod
    def deletar(registro):
        lote_frango = LoteFrangoService.buscar_por_id(registro.lote_frango_id)

        lote_frango.quantidade_atual += registro.quantidade_mortes

        db.session.delete(registro)