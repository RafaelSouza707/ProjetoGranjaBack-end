from flask import Flask
from flask_cors import CORS
from helpers.application import app, api
from helpers.database import db
from models import * 
from resources.HomeResources import HomeResources
from resources.lote_racao_resource import LoteRacaoResource
from resources.corte_resource import CorteResource
from resources.postura_resource import PosturaResource
from resources.lote_frango_resource import LoteFrangoResource
from resources.despesa_resource import DespesaResource
from resources.tipo_despesa_resource import TipoDespesaResource
from resources.venda_ovos_resource import VendaOvosResource
from resources.venda_corte_resource import VendaCorteResource
from resources.mortalidade_resource import MortalidadeResource
from resources.controle_vacina_resource import ControleVacinasResource
from resources.consumo_lote_diaria_resource import ConsumoLoteDiariaResource

CORS(app)

from helpers.logging_config import setup_logging

setup_logging(app)

# adiciona recurso
api.add_resource(HomeResources, '/')
api.add_resource(LoteRacaoResource, '/lote_racao', '/lote_racao/<int:id>')
api.add_resource(CorteResource, '/corte', '/corte/<int:id>')
api.add_resource(PosturaResource, '/postura', '/postura/<int:id>')
api.add_resource(LoteFrangoResource, '/lote_frango', '/lote_frango/<int:id>')
api.add_resource(DespesaResource, '/despesa', '/despesa/<int:id>')
api.add_resource(TipoDespesaResource, '/tipo_despesa', '/tipo_despesa/<int:id>')
api.add_resource(VendaOvosResource, '/venda_ovos', '/venda_ovos/<int:id>')
api.add_resource(VendaCorteResource, '/venda_corte', '/venda_corte/<int:id>')
api.add_resource(MortalidadeResource, '/mortalidade', '/mortalidade/<int:id>')
api.add_resource(ControleVacinasResource, '/controle_vacinas', '/controle_vacinas/<int:id>')
api.add_resource(ConsumoLoteDiariaResource, '/consumo_lote_diaria', '/consumo_lote_diaria/<int:id>')


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)