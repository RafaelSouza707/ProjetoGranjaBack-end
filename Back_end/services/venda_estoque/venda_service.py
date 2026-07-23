from helpers.database import db
from sqlalchemy import func
from helpers.errors.exceptions import NotFoundError
from models.venda.venda import Venda
from models.granja.granja import Granja
from services.financas.receita_service import ReceitaService
from models.financas.tipo_receita import TipoReceita


class VendaService:

    @staticmethod
    def listar(granja_id, pagina, per_page):
        return (
            db.session.query(Venda)
            .join(Venda.granja)
            .filter(Granja.id == granja_id)
            .order_by(Venda.data_venda.desc())
            .paginate(
                page=pagina,
                per_page=per_page,
                error_out=False
            ) 
        )
    

    @staticmethod
    def buscar_por_id(id):
        registro = db.session.get(Venda, id)

        if not registro:
            raise NotFoundError("Registro não encontrado")

        return registro
    

    @staticmethod
    def criar(data):
        novo_registro = Venda(**data)

        tipo_receita = TipoReceita.query.filter(func.lower(TipoReceita.nome) == "venda produto").first()


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
    def atualizar(registro, data):
        for k, v in data.items():
            setattr(registro, k, v)

        return registro
    

    @staticmethod
    def deletar(registro):
        db.session.delete(registro)