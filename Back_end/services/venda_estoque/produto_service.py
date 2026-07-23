from helpers.database import db
from helpers.errors.exceptions import NotFoundError
from models.estoque.produto import Produto
from models.granja.granja import Granja
from models.aviario.tipo_produto import TipoProduto

class ProdutoService:

    @staticmethod
    def listar_paginado(granja_id, pagina, per_page):
        resultados = (
            db.session.query(Produto)
            .join(Produto.tipo_produto)
            .filter(
                Produto.granja_id == granja_id
            )
            .order_by(
                TipoProduto.nome.asc()
            )
            .paginate(
                page=pagina,
                per_page=per_page,
                error_out=False
            )
        )

        return resultados
    

    @staticmethod
    def listar(granja_id):
        resultado = (
            db.session.query(Produto)
            .filter(
                Produto.granja_id == granja_id
            )
            .all()
        )
        return resultado


    @staticmethod
    def buscar_por_id(id):
        registro = db.session.get(Produto, id)

        if not registro:
            raise NotFoundError("Registro não encontrado")

        return registro


    @staticmethod
    def criar(data, granja_id):
        tipo_produto = data.get("tipo_produto_id")
        verificacao = (
            db.session.query(Produto)
            .filter(
                Produto.granja_id == granja_id,
                Produto.tipo_produto_id == tipo_produto
            )
            .first()
        )
        if verificacao is None:
            novo_registro = Produto(**data)

            db.session.add(novo_registro)
            db.session.flush()
            
            return novo_registro
        
        else:
            verificacao.quantidade_estoque += data.get("quantidade_estoque")
            db.session.flush()

            return verificacao


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