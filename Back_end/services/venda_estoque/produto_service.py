from helpers.database import db
from helpers.exceptions import NotFoundError
from models.estoque.produto import Produto
from models.granja.granja import Granja


class ProdutoService:

    @staticmethod
    def listar(granja_id):
        resultados = (
            db.session.query(Produto)
            .filter(Produto.granja_id == granja_id)
            .all()
        )

        return resultados


    @staticmethod
    def buscar_por_id(id):
        registro = db.session.get(Produto, id)

        if not registro:
            raise NotFoundError("Registro não encontrado")

        return registro


    @staticmethod
    def criar(data):
        novo_registro = Produto(**data)

        db.session.add(novo_registro)
        db.session.flush()

        return novo_registro


    @staticmethod
    def atualizar(registro, data):
        
        data.pop("tipo_produto", None)
        data.pop("tipo_unidade_medida", None)
        for k, v in data.items():
            setattr(registro, k, v)

        return registro


    @staticmethod
    def deletar(registro):
        db.session.delete(registro)