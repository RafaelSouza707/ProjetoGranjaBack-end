from decimal import Decimal
from helpers.database import db
from datetime import datetime
from sqlalchemy import extract, func
from helpers.errors.exceptions import NotFoundError, BusinessRuleError
from models.aviario.consumo_lote_diaria import ConsumoLoteDiaria
from models.aviario.lote_frangos import LoteFrango
from models.granja.granja import Granja
from helpers.database.query_builder import QueryBuilder
from services.aviario.lote_racao_service import LoteRacaoService

class ConsumoLoteDiariaService:

    @staticmethod
    def listar(granja_id, pagina, per_page):
        query = (
            db.session.query(ConsumoLoteDiaria)
            .join(ConsumoLoteDiaria.lote_frango)
            .filter(
                LoteFrango.granja_id == granja_id
            )
        )

        query = QueryBuilder(
            ConsumoLoteDiaria,
            query
        ).build().order_by(ConsumoLoteDiaria.data.desc())
        
        return query.paginate(
            page=pagina,
            per_page=per_page,
            error_out=False
        )
    

    @staticmethod
    def listar_de_lote_frango(lote_frango_id, pagina, per_page):
        query = (
            db.session.query(ConsumoLoteDiaria)
            .filter(
                ConsumoLoteDiaria.lote_frango_id == lote_frango_id
            )
        )

        query = QueryBuilder(
            ConsumoLoteDiaria,
            query
        ).build().order_by(ConsumoLoteDiaria.data.desc())

        return query.paginate(
            page=pagina,
            per_page=per_page,
            error_out=False
        )


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
    def _ajustar_quilos_lote_racao(lote_racao, quilos, operacao):
        if quilos is None:
            return

        valor = Decimal(str(quilos))

        if operacao == "subtrair":
            if lote_racao.quilos < valor:
                raise BusinessRuleError("A quantidade consumida excede o saldo disponível no lote de ração.")
            lote_racao.quilos -= valor
        elif operacao == "adicionar":
            lote_racao.quilos += valor


    @staticmethod
    def criar(data):
        novo_registro = ConsumoLoteDiaria(**data)
        lote_racao = LoteRacaoService.buscar_por_id(data["lote_racao_id"])
        ConsumoLoteDiariaService._ajustar_quilos_lote_racao(
            lote_racao,
            data["quilos"],
            "subtrair"
        )

        db.session.add(novo_registro)
        db.session.flush()

        return novo_registro
    

    @staticmethod
    def atualizar(registro, data):
        lote_racao_antigo = None
        lote_racao_novo = None

        lote_racao_id_antigo = registro.lote_racao_id
        quilos_antigos = registro.quilos
        lote_racao_id_novo = data.get("lote_racao_id", lote_racao_id_antigo)
        quilos_novos = data.get("quilos", quilos_antigos)

        if lote_racao_id_antigo != lote_racao_id_novo or quilos_antigos != quilos_novos:
            lote_racao_antigo = LoteRacaoService.buscar_por_id(lote_racao_id_antigo)
            ConsumoLoteDiariaService._ajustar_quilos_lote_racao(
                lote_racao_antigo,
                quilos_antigos,
                "adicionar"
            )

            lote_racao_novo = LoteRacaoService.buscar_por_id(lote_racao_id_novo)
            ConsumoLoteDiariaService._ajustar_quilos_lote_racao(
                lote_racao_novo,
                quilos_novos,
                "subtrair"
            )

        for k, v in data.items():
            setattr(registro, k, v)

        return registro
    

    @staticmethod
    def deletar(registro):
        lote_racao = LoteRacaoService.buscar_por_id(registro.lote_racao_id)
        ConsumoLoteDiariaService._ajustar_quilos_lote_racao(
            lote_racao,
            registro.quilos,
            "adicionar"
        )
        db.session.delete(registro)