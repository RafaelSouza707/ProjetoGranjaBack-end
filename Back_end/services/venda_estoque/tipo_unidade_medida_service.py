from helpers.database import db
from helpers.exceptions import NotFoundError
from models.venda_estoque.tipo_unidade_medida import TipoUnidadeMedida
from models.granja.granja import Granja

def normalizar(data):
    if "sigla" in data and isinstance(data["sigla"], str):
        data["sigla"] = data["sigla"].strip().lower()

class TipoUnidadeMedidaService:


    @staticmethod
    def listar(granja_id):
        resultados = (
            db.session.query(TipoUnidadeMedida)
            .join(TipoUnidadeMedida.granja)
            .filter(
                Granja.id == granja_id
            )
            .all()
        )

        return resultados
    
    
    @staticmethod
    def buscar_por_id(id):
        registro = db.session.get(TipoUnidadeMedida, id)

        if not registro:
            raise NotFoundError("Registro não encontrado")
        
        return registro
    

    @staticmethod
    def criar(data):
        normalizar(data)
        
        novo_registro = TipoUnidadeMedida(**data)
        
        db.session.add(novo_registro)
        db.session.flush()

        return novo_registro
    

    @staticmethod
    def atualizar(registro, data):
        normalizar(data)

        for k, v in data.items():
            setattr(registro, k, v)

        return registro
    

    @staticmethod
    def deletar(registro):
        db.session.delete(registro)