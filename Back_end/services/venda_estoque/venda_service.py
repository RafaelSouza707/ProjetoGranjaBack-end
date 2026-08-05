from helpers.database import db
from sqlalchemy import func

from helpers.errors.exceptions import NotFoundError
from helpers.database.query_builder import QueryBuilder

from models.venda.venda import Venda
from models.granja.granja import Granja

from services.financas.receita_service import ReceitaService
from services.venda_estoque.item_venda_service import ItemVendaService

from models.financas.tipo_receita import TipoReceita


class VendaService:

    @staticmethod
    def listar(granja_id, pagina, per_page):
        query = (
            db.session.query(Venda)
            .join(Venda.granja)
            .filter(Granja.id == granja_id)
        )

        query = QueryBuilder(
            Venda,
            query
        ).build().order_by(
            Venda.data_venda.desc()
        )

        return query.paginate(
            page=pagina,
            per_page=per_page,
            error_out=False
        )

    @staticmethod
    def buscar_por_id(id):
        registro = db.session.get(Venda, id)

        if not registro:
            raise NotFoundError(
                "Registro não encontrado"
            )

        return registro

    @staticmethod
    def criar(data):
        novo_registro = Venda(**data)

        tipo_receita = TipoReceita.query.filter(
            func.lower(TipoReceita.nome) == "venda produto"
        ).first()

        db.session.add(novo_registro)

        db.session.flush()

        ReceitaService.criar({
            "tipo_receita_id": tipo_receita.id,
            "status_financas_id": novo_registro.status_financas_id,
            "venda_id": novo_registro.id,
            "granja_id": novo_registro.granja_id,
            "data": novo_registro.data_venda,
            "valor": novo_registro.valor_total,
            "descricao": None
        })

        return novo_registro

    @staticmethod
    def atualizar(registro, data, itens):
        for k, v in data.items():
            setattr(registro, k, v)

        db.session.flush()

        itens_existentes = ItemVendaService.listar(
            registro.id
        )

        ids_itens_recebidos = set()

        for item_novo in itens:

            item_id = item_novo.get("id")

            if item_id:

                item_existente = next(
                    (
                        item
                        for item in itens_existentes
                        if item.id == item_id
                    ),
                    None
                )

                if item_existente:

                    item_existente.produto_id = item_novo[
                        "produto_id"
                    ]

                    item_existente.quantidade = item_novo[
                        "quantidade"
                    ]

                    item_existente.subtotal = item_novo[
                        "subtotal"
                    ]

                    ids_itens_recebidos.add(item_id)

            else:

                ItemVendaService.criar({
                    "venda_id": registro.id,
                    "produto_id": item_novo["produto_id"],
                    "quantidade": item_novo["quantidade"],
                    "subtotal": item_novo["subtotal"]
                })


        for item_existente in itens_existentes:

            if item_existente.id not in ids_itens_recebidos:
                ItemVendaService.deletar(
                    item_existente
                )

        receita = ReceitaService.buscar_por_id(
            registro.id
        )

        if receita:

            receita.valor = registro.valor_total

            receita.status_financas_id = (
                registro.status_financas_id
            )

            receita.data = registro.data_venda

        return registro

    @staticmethod
    def deletar(registro):
        db.session.delete(registro)