from flask import Flask
from flask_cors import CORS
from helpers.application import app, api
from helpers.database import db
from models import *
from database.seed import run_seed

# Resources
from resources.home_resource import HomeResources

## Controle_Banco_de_dados
from resources.controle_banco_de_dados.cargos_resource import CargoResource
from resources.controle_banco_de_dados.permissoes_resource import PermissaoResource
from resources.controle_banco_de_dados.role_permissao_resource import RolePermissaoResource
from resources.controle_banco_de_dados.role_resource import RoleResource

## Financas
from resources.financas.despesa_resource import DespesaResource
from resources.financas.status_financas_resource import StatusFinancasResource
from resources.financas.tipo_despesa_resource import TipoDespesaResource
from resources.financas.cards_gastos_resource import CardsGastosResource

## Granja
from resources.granja.consumo_lote_diaria_resource import ConsumoLoteDiariaResource
from resources.granja.lote_frango_resource import LoteFrangoResource
from resources.granja.lote_racao_resource import LoteRacaoResource
from resources.granja.mortalidade_resource import MortalidadeResource
from resources.granja.status_lote_frango_resource import StatusLoteFrangoResource
from resources.granja.tipo_produto_resource import TipoProdutoResource
from resources.granja.tipo_racao_resource import TipoRacaoResource

## Usuarios
from resources.usuarios.cliente_resource import ClienteResource
from resources.usuarios.conta_adm_resource import ContaADMResource
from resources.usuarios.endereco_resource import EnderecoResource
from resources.usuarios.escolaridades_resource import EscolaridadesResource
from resources.usuarios.funcionario_resource import FuncionarioResource
from resources.usuarios.sexo_service import SexoResource

## Venda_Estoque
from resources.venda_estoque.estoque_resource import EstoqueResource
from resources.venda_estoque.item_venda_resource import ItemVendaResource
from resources.venda_estoque.movimentacao_estoque_resource import MovimentacaoEstoqueResource
from resources.venda_estoque.producao_resource import ProducaoResource
from resources.venda_estoque.produto_resource import ProdutoResource
from resources.venda_estoque.status_venda_resource import StatusVendaResource
from resources.venda_estoque.tipo_movimentacao_resource import TipoMovimentacaoResource
from resources.venda_estoque.tipo_unidade_medida_resource import TipoUnidadeMediaResource
from resources.venda_estoque.venda_resource import VendaResource


CORS(app)

from helpers.logging_config import setup_logging

setup_logging(app)

# end-point's
api.add_resource(HomeResources, '/')

## Controle_Banco_de_dados api.add_resource(, '/', '//<int:id>')
api.add_resource(CargoResource, '/cargo', '/cargo/<int:id>')
api.add_resource(PermissaoResource, '/permissao', '/permissao/<int:id>')
api.add_resource(RolePermissaoResource, '/role_permissao', '/role_permissao/<int:id>')
api.add_resource(RoleResource, '/role', '/role/<int:id>')

## Financas
api.add_resource(DespesaResource, '/despesa', '/despesa/<int:id>')
api.add_resource(StatusFinancasResource, '/status_financas', '/status_financas/<int:id>')
api.add_resource(TipoDespesaResource, '/tipo_despesa', '/tipo_despesa/<int:id>')
api.add_resource(CardsGastosResource, '/cards_gastos')

## Granja
api.add_resource(ConsumoLoteDiariaResource, '/consumo_lote_diaria', '/consumo_lote_diaria/<int:id>')
api.add_resource(LoteFrangoResource, '/lote_frango', '/lote_frango/<int:id>')
api.add_resource(LoteRacaoResource, '/lote_racao', '/lote_racao/<int:id>')
api.add_resource(MortalidadeResource, '/mortalidade', '/mortalidade/<int:id>')
api.add_resource(StatusLoteFrangoResource, '/status_lote_frango', '/status_lote_frango/<int:id>')
api.add_resource(TipoProdutoResource, '/tipo_produto', '/tipo_produto/<int:id>')
api.add_resource(TipoRacaoResource, '/tipo_racao', '/tipo_racao/<int:id>')

## Usuarios
api.add_resource(ClienteResource, '/cliente', '/cliente/<int:id>')
api.add_resource(ContaADMResource, '/conta_adm', '/conta_adm/<int:id>')
api.add_resource(EnderecoResource, '/endereco', '/endereco/<int:id>')
api.add_resource(EscolaridadesResource, '/escolaridade', '/escolaridade/<int:id>')
api.add_resource(FuncionarioResource, '/funcionario', '/funcionario/<int:id>')
api.add_resource(SexoResource, '/sexo', '/sexo/<int:id>')


api.add_resource(EstoqueResource, '/estoque', '/estoque/<int:id>')
api.add_resource(ItemVendaResource, '/item_venda', '/item_venda/<int:id>')
api.add_resource(MovimentacaoEstoqueResource, '/movimentacao_estoque', '/movimentacao_estoque/<int:id>')
api.add_resource(ProducaoResource, '/producao', '/producao/<int:id>')
api.add_resource(ProdutoResource, '/produto', '/produto/<int:id>')
api.add_resource(StatusVendaResource, '/status_venda', '/status_venda/<int:id>')
api.add_resource(TipoMovimentacaoResource, '/tipo_movimentacao', '/tipo_movimentacao/<int:id>')
api.add_resource(TipoUnidadeMediaResource, '/tipo_unidade_media', '/tipo_unidade_media/<int:id>')
api.add_resource(VendaResource, '/venda', '/venda/<int:id>')


@app.cli.command("seed")
def seed():
    run_seed()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, use_reloader=False)
