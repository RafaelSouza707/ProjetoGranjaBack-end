from helpers.database import db
from helpers.exceptions import NotFoundError
from models.estoque.movimentacao_estoque import MovimentacaoEstoque
from models.estoque.produto import Produto
from models.granja.granja import Granja


class MovimentacaoEstoqueService:

    @staticmethod
    def listar(granja_id):
        resultado = (
            db.session.query(MovimentacaoEstoque)
            .join(MovimentacaoEstoque.produto)
            .join(Produto.granja)
            .filter(Granja.id == granja_id)
            .all()
        )
        return resultado

    @staticmethod
    def buscar_por_id(id):
        registro = db.session.get(MovimentacaoEstoque, id)
        if not registro:
            raise NotFoundError("Registro não encontrado")

        return registro

    @staticmethod
    def criar(data):
        novo_registro = MovimentacaoEstoque(**data)

        db.session.add(novo_registro)
        db.session.flush()

        return novo_registro

    @staticmethod
    def atualizar(registro, data):
        for k, v in data.items():
            setattr(registro, k, v)

        return registro

    @staticmethod
    def deletar(registro):
        db.session.delete(registro)