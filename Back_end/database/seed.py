from datetime import date

from helpers.database import db

from models.granja.tipo_racao import TipoRacao
from models.granja.tipo_produto import TipoProduto
from models.granja.status_lote_frango import StatusLoteFrango
from models.granja.lote_racao import LoteRacao
from models.granja.lote_frangos import LoteFrango
from models.granja.mortalidade import Mortalidade
from models.granja.consumo_lote_diaria import ConsumoLoteDiaria


def run_seed():
    if TipoRacao.query.first():
        print("Seed já executado.")
        return

    # ==========================================
    # TIPO RAÇÃO
    # ==========================================

    tipo_inicial = TipoRacao(
        nome="inicial",
        descricao="Ração utilizada nas primeiras semanas"
    )

    tipo_crescimento = TipoRacao(
        nome="crescimento",
        descricao="Ração para fase de crescimento"
    )

    tipo_terminacao = TipoRacao(
        nome="terminação",
        descricao="Ração para fase final de engorda"
    )

    db.session.add_all([
        tipo_inicial,
        tipo_crescimento,
        tipo_terminacao
    ])

    # ==========================================
    # TIPO PRODUTO
    # ==========================================

    db.session.add_all([
        TipoProduto(nome="ovos"),
        TipoProduto(nome="frango vivo"),
        TipoProduto(nome="esterco"),
        TipoProduto(nome="pinto de um dia"),
        TipoProduto(nome="frango abatido")
    ])

    # ==========================================
    # STATUS LOTE FRANGO
    # ==========================================

    status_ativo = StatusLoteFrango(nome="ativo")
    status_finalizado = StatusLoteFrango(nome="finalizado")
    status_cancelado = StatusLoteFrango(nome="cancelado")

    db.session.add_all([
        status_ativo,
        status_finalizado,
        status_cancelado
    ])

    db.session.flush()

    # ==========================================
    # LOTE RAÇÃO
    # ==========================================

    lote_racao_1 = LoteRacao(
        tipo_racao_id=tipo_inicial.id,
        fornecedor="NutriRacao LTDA",
        data_compra=date(2026, 1, 5),
        quilos=5000,
        valor=12500.00
    )

    lote_racao_2 = LoteRacao(
        tipo_racao_id=tipo_crescimento.id,
        fornecedor="AgroFeed LTDA",
        data_compra=date(2026, 2, 1),
        quilos=6000,
        valor=15600.00
    )

    lote_racao_3 = LoteRacao(
        tipo_racao_id=tipo_terminacao.id,
        fornecedor="NutriRacao LTDA",
        data_compra=date(2026, 3, 1),
        quilos=7000,
        valor=18900.00
    )

    db.session.add_all([
        lote_racao_1,
        lote_racao_2,
        lote_racao_3
    ])

    db.session.flush()

    # ==========================================
    # LOTE FRANGO
    # ==========================================

    lote1 = LoteFrango(
        status_lote_frango_id=status_ativo.id,
        identificacao="A1",
        quantidade_inicial=500,
        data_alojamento=date(2026, 1, 10),
        fornecedor="Agi Ota",
        quantidade_atual=500,
        observacao="Primeiro lote do ano"
    )

    lote2 = LoteFrango(
        status_lote_frango_id=status_ativo.id,
        identificacao="A2",
        quantidade_inicial=500,
        data_alojamento=date(2026, 2, 10),
        fornecedor="Agi Ota",
        quantidade_atual=500,
        observacao="Primeiro lote do ano"
    )

    lote3 = LoteFrango(
        status_lote_frango_id=status_ativo.id,
        identificacao="A3",
        quantidade_inicial=500,
        data_alojamento=date(2026, 3, 10),
        fornecedor="Agi Ota",
        quantidade_atual=500,
        observacao="Primeiro lote do ano"
    )

    db.session.add_all([
        lote1,
        lote2,
        lote3
    ])

    db.session.flush()

    # ==========================================
    # MORTALIDADE
    # ==========================================

    db.session.add_all([
        Mortalidade(
            lote_frango_id=lote1.id,
            data=date(2026, 1, 10),
            quantidade_mortes=5
        ),
        Mortalidade(
            lote_frango_id=lote1.id,
            data=date(2026, 1, 11),
            quantidade_mortes=5
        ),
        Mortalidade(
            lote_frango_id=lote1.id,
            data=date(2026, 1, 12),
            quantidade_mortes=5
        ),
        Mortalidade(
            lote_frango_id=lote1.id,
            data=date(2026, 1, 17),
            quantidade_mortes=10
        )
    ])

    # ==========================================
    # CONSUMO LOTE DIÁRIA
    # ==========================================

    db.session.add_all([
        ConsumoLoteDiaria(
            lote_frango_id=lote1.id,
            lote_racao_id=lote_racao_1.id,
            data=date(2026, 1, 11),
            quilos=120.500
        ),
        ConsumoLoteDiaria(
            lote_frango_id=lote1.id,
            lote_racao_id=lote_racao_1.id,
            data=date(2026, 1, 12),
            quilos=118.750
        ),
        ConsumoLoteDiaria(
            lote_frango_id=lote2.id,
            lote_racao_id=lote_racao_2.id,
            data=date(2026, 2, 16),
            quilos=140.000
        )
    ])

    db.session.commit()

    print("Seed executado com sucesso.")
