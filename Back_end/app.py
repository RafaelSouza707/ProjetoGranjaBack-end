from flask import Flask
from flask_cors import CORS
from helpers.application import app, api
from helpers.database import db
from models import *
from seeds.seed import run_seed


# Resources
from resources.home_resource import HomeResources

## Controle_Banco_de_dados
from resources.controle_banco_de_dados.permissoes_resource import PermissaoResource
from resources.controle_banco_de_dados.role_permissao_resource import RolePermissaoResource
from resources.controle_banco_de_dados.role_resource import RoleResource

## Financas
from resources.financas.despesa_resource import DespesaResource
from resources.financas.status_financas_resource import StatusFinancasResource
from resources.financas.tipo_despesa_resource import TipoDespesaResource
from resources.financas.cards_gastos_resource import CardsFinancasResource
from resources.financas.cards_gastos_granja_resource import CardsGastosGranjaResource
from resources.financas.despesa_search import DespesaSearch
from resources.financas.tipo_receita_resource import TipoReceitaResource
from resources.financas.receita_resource import ReceitaResource
from resources.financas.cards_receitas_granja_resource import CardsReceitasResource

## Aviario
from resources.aviario.consumo_lote_diaria_resource import ConsumoLoteDiariaResource
from resources.aviario.lote_frango_resource import LoteFrangoResource
from resources.aviario.lote_racao_resource import LoteRacaoResource
from resources.aviario.mortalidade_resource import MortalidadeResource
from resources.aviario.status_lote_frango_resource import StatusLoteFrangoResource
from resources.aviario.tipo_produto_resource import TipoProdutoResource
from resources.aviario.tipo_racao_resource import TipoRacaoResource
from resources.aviario.cards_lote_frango import CardsLoteFrango
from resources.aviario.cards_racao_resource import CardsLoteRacao

## Usuarios
from resources.usuarios.cliente_resource import ClienteResource
from resources.usuarios.endereco_resource import EnderecoResource
from resources.usuarios.escolaridades_resource import EscolaridadesResource
from resources.usuarios.usuario_resource import UsuarioResource
from resources.usuarios.sexo_resource import SexoResource
from resources.usuarios.login_resource import LoginResource
from resources.usuarios.logout_resource import LogoutResource
from resources.usuarios.usuario_associacao_resource import UsuarioAssociacaoResource

## Granja
from resources.granja.granja_resource import GranjaResource
from resources.granja.usuario_resource import UsuarioGranjaResource

## Venda_Estoque
from resources.venda_estoque.estoque_resource import EstoqueResource
from resources.venda_estoque.item_venda_resource import ItemVendaResource
from resources.venda_estoque.movimentacao_estoque_resource import MovimentacaoEstoqueResource
from resources.venda_estoque.producao_resource import ProducaoResource
from resources.venda_estoque.produto_resource import ProdutoResource
from resources.venda_estoque.tipo_venda_resource import TipoVendaResource
from resources.venda_estoque.tipo_movimentacao_resource import TipoMovimentacaoResource
from resources.venda_estoque.tipo_unidade_medida_resource import TipoUnidadeMedidaResource
from resources.venda_estoque.venda_resource import VendaResource

CORS(
    app,
    supports_credentials=True,
    origins=["http://localhost:5001"]
)

from helpers.logging_config import setup_logging

setup_logging(app)

# end-point's
api.add_resource(HomeResources, '/')

## Controle_Banco_de_dados api.add_resource(, '/', '//<int:id>')
api.add_resource(PermissaoResource, '/controle_bd/permissao', '/controle_bd/permissao/<int:id>')
api.add_resource(RolePermissaoResource, '/controle_bd/role_permissao', '/controle_bd/role_permissao/<int:id>')
api.add_resource(RoleResource, '/controle_bd/role', '/controle_bd/role/<int:id>')
 
## Financas
api.add_resource(DespesaResource, '/financas/despesa', '/financas/despesa/<int:id>')
api.add_resource(StatusFinancasResource, '/financas/status_financas', '/financas/status_financas/<int:id>')
api.add_resource(TipoDespesaResource, '/financas/tipo_despesa', '/financas/tipo_despesa/<int:id>')
api.add_resource(CardsFinancasResource, '/financas/cards_financas')
api.add_resource(CardsGastosGranjaResource, '/financas/cards_gastos_granja')
api.add_resource(DespesaSearch, '/financas/despesa_search')
api.add_resource(TipoReceitaResource, '/financas/tipo_receita', '/financas/tipo_receita/<int:id>')
api.add_resource(ReceitaResource, '/financas/receita', '/financas/receita/<int:id>')
api.add_resource(CardsReceitasResource, '/financas/cards_receitas_granja')

## Aviario
api.add_resource(ConsumoLoteDiariaResource, '/granja/consumo_lote_diaria', '/granja/consumo_lote_diaria/<int:id>')
api.add_resource(LoteFrangoResource, '/granja/lote_frango', '/granja/lote_frango/<int:id>')
api.add_resource(LoteRacaoResource, '/granja/lote_racao', '/granja/lote_racao/<int:id>')
api.add_resource(CardsLoteRacao, '/granja/cards_lote_racao')
api.add_resource(MortalidadeResource, '/granja/mortalidade', '/granja/mortalidade/<int:id>')
api.add_resource(StatusLoteFrangoResource, '/granja/status_lote_frango', '/granja/status_lote_frango/<int:id>')
api.add_resource(TipoProdutoResource, '/granja/tipo_produto', '/granja/tipo_produto/<int:id>')
api.add_resource(TipoRacaoResource, '/granja/tipo_racao', '/granja/tipo_racao/<int:id>')
api.add_resource(CardsLoteFrango, '/granja/cards_lote_frango')

## Usuarios
api.add_resource(ClienteResource, '/usuarios/cliente', '/usuarios/cliente/<int:id>')
api.add_resource(EnderecoResource, '/usuarios/endereco', '/usuarios/endereco/<int:id>')
api.add_resource(EscolaridadesResource, '/usuarios/escolaridade', '/usuarios/escolaridade/<int:id>')
api.add_resource(UsuarioResource, '/usuarios/usuario', '/usuarios/usuario/<int:id>')
api.add_resource(SexoResource, '/usuarios/sexo', '/usuarios/sexo/<int:id>')
api.add_resource(LoginResource, '/usuarios/login')
api.add_resource(LogoutResource, '/usuarios/logout')
api.add_resource(UsuarioAssociacaoResource, '/usuarios/relacao')

## Granja
api.add_resource(GranjaResource, '/granja/granja', '/granja/granja/<int:id>')
api.add_resource(UsuarioGranjaResource, '/granja/usuario_granja', '/granja/usuario_granja/<int:id>')

# Venda_Estoque
api.add_resource(EstoqueResource, '/venda_estoque/estoque', '/venda_estoque/estoque/<int:id>')
api.add_resource(ItemVendaResource, '/venda_estoque/item_venda', '/venda_estoque/item_venda/<int:id>')
api.add_resource(MovimentacaoEstoqueResource, '/venda_estoque/movimentacao_estoque', '/venda_estoque/movimentacao_estoque/<int:id>')
api.add_resource(ProducaoResource, '/venda_estoque/producao', '/venda_estoque/producao/<int:id>')
api.add_resource(ProdutoResource, '/venda_estoque/produto', '/venda_estoque/produto/<int:id>')
api.add_resource(TipoVendaResource, '/venda_estoque/tipo_venda', '/venda_estoque/tipo_venda/<int:id>')
api.add_resource(TipoMovimentacaoResource, '/venda_estoque/tipo_movimentacao', '/venda_estoque/tipo_movimentacao/<int:id>')
api.add_resource(TipoUnidadeMedidaResource, '/venda_estoque/tipo_unidade_medida', '/venda_estoque/tipo_unidade_medida/<int:id>')
api.add_resource(VendaResource, '/venda_estoque/venda', '/venda_estoque/venda/<int:id>')


@app.cli.command("seed")
def seed():
    run_seed()



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, use_reloader=False)
