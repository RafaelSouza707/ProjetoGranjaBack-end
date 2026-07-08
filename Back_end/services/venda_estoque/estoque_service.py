from helpers.database import db
from helpers.exceptions import NotFoundError
from models.estoque.estoque import Estoque
from models.estoque.produto import Produto
from models.granja.granja import Granja
from models.granja.usuario_granja import UsuarioGranja

class EstoqueService:

    @staticmethod
    def listar(user_id):
        resultado = (
            db.session.query(Estoque)
            .join(Estoque.produto)
            .join(Produto.granja)
            .join(Granja.usuarios)
            .filter(
                UsuarioGranja.usuario_id == user_id
            )
            .all()
        )
        return resultado
    
    
    @staticmethod
    def buscar_por_id(id, user_id):
        registro = (
            db.session.query(Estoque)
            .join(Estoque.produto)
            .join(Produto.granja)
            .join(Granja.usuarios)
            .filter(
                UsuarioGranja.usuario_id == user_id,
                Estoque.id == id
            )
            .first()
        )

        if not registro:
            raise NotFoundError("Registro não encontrado")
        
        return registro
    

    @staticmethod
    def criar(data):
        novo_registro = Estoque(**data)
        
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