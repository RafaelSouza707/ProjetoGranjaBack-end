from helpers.database import db
from helpers.exceptions import NotFoundError
from models.venda.item_venda import ItemVenda
from models.estoque.produto import Produto
from models.granja.granja import Granja


class ItemVendaService:

    @staticmethod
    def listar(granja_id):
        resultados = (
            db.session.query(ItemVenda)
            .join(ItemVenda.produto)
            .join(Produto.granja)
            .filter(
                Granja.id == granja_id
            )
            .all()
        )

        return resultados
    
    
    @staticmethod
    def buscar_por_id(id):
        registro = (
            db.session.query(ItemVenda)
            .join(ItemVenda.produto)
            .join(Produto.granja)
            .filter(
                ItemVenda.id == id
            )
            .first()
        )

        if not registro:
            raise NotFoundError("Registro não encontrado")
        
        return registro
    

    @staticmethod
    def criar(data):
        novo_registro = ItemVenda(**data)
        
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