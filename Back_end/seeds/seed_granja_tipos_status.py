from datetime import date

from helpers.database import db

from models.aviario.tipo_racao import TipoRacao
from models.aviario.tipo_produto import TipoProduto
from models.aviario.status_lote_frango import StatusLoteFrango
from models.financas.status_financas import StatusFinancas
from models.financas.tipo_despesa import TipoDespesa
from models.financas.tipo_receita import TipoReceita
from models.estoque.tipo_movimentacao import TipoMovimentacao
from models.estoque.tipo_unidade_medida import TipoUnidadeMedida
from models.venda.tipo_venda import TipoVenda
from models.usuarios.sexo import Sexo


def criar_dados_padrao_granja(granja_id):

    # STATUS FINANCEIRO
    db.session.add_all([
        StatusFinancas(nome="Pago", granja_id=granja_id),
        StatusFinancas(nome="Atrasado", granja_id=granja_id),
        StatusFinancas(nome="Em Espera", granja_id=granja_id),
    ])

    # TIPO DESPESA
    db.session.add_all([
        TipoDespesa(nome="Ração Frangos", granja_id=granja_id),
        TipoDespesa(nome="Produtos Limpeza", granja_id=granja_id),
        TipoDespesa(nome="Salário", granja_id=granja_id),
        TipoDespesa(nome="Serviço Externo", granja_id=granja_id),
        TipoDespesa(nome="Transporte", granja_id=granja_id),
        TipoDespesa(nome="Aluguel", granja_id=granja_id),
    ])

    # TIPO RECEITA
    db.session.add_all([
        TipoReceita(nome="Venda Produto", granja_id=granja_id),
        TipoReceita(nome="Venda Excedente", granja_id=granja_id),
        TipoReceita(nome="Aluguel", granja_id=granja_id),
    ])

    # STATUS LOTE
    db.session.add_all([
        StatusLoteFrango(nome="ativo", granja_id=granja_id),
        StatusLoteFrango(nome="desativado", granja_id=granja_id),
        StatusLoteFrango(nome="vazio", granja_id=granja_id),
        StatusLoteFrango(nome="paralisado", granja_id=granja_id),
    ])

    # TIPO PRODUTO
    db.session.add_all([
        TipoProduto(nome="Ovo", granja_id=granja_id),
        TipoProduto(nome="Frango Vivo", granja_id=granja_id),
        TipoProduto(nome="Frango Abatido", granja_id=granja_id),
        TipoProduto(nome="Pinto de Um Dia", granja_id=granja_id),
        TipoProduto(nome="Esterco", granja_id=granja_id),
        TipoProduto(nome="Ração", granja_id=granja_id),
    ])

    # TIPO RAÇÃO
    db.session.add_all([
        TipoRacao(
            nome="Inicial",
            descricao="Ração para frangos até 2 dias de vida",
            granja_id=granja_id
        ),
        TipoRacao(
            nome="Concentrado",
            descricao="Frangos de 2 até 15 dias de vida",
            granja_id=granja_id
        ),
        TipoRacao(
            nome="Engorda",
            descricao="Para frangos de corte a partir de 10 dias de vida",
            granja_id=granja_id
        ),
    ])

    # TIPO MOVIMENTAÇÃO
    db.session.add_all([
        TipoMovimentacao(
            nome="Troca de Armazém",
            granja_id=granja_id
        ),
        TipoMovimentacao(
            nome="Retirada para Venda",
            granja_id=granja_id
        ),
    ])

    # TIPO VENDA
    db.session.add_all([
        TipoVenda(
            nome="Venda Direta",
            granja_id=granja_id
        ),
        TipoVenda(
            nome="Venda Indireta",
            granja_id=granja_id
        ),
    ])

    # UNIDADES
    db.session.add_all([
        TipoUnidadeMedida(
            sigla="KG",
            descricao="Quilograma",
            granja_id=granja_id
        ),
        TipoUnidadeMedida(
            sigla="DZ",
            descricao="12 unidades",
            granja_id=granja_id
        ),
        TipoUnidadeMedida(
            sigla="CENT",
            descricao="100 unidades",
            granja_id=granja_id
        ),
        TipoUnidadeMedida(
            sigla="UN",
            descricao="1 unidade",
            granja_id=granja_id
        ),
    ])

    db.session.flush()