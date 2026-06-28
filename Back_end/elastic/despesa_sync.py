from helpers.extensao_elasticsearch import es
from elastic.despesa_index import INDEX

def indexar_despesa(despesa):
    es.index(
        index=INDEX,
        id=despesa.id,
        document={
            "tipo": despesa.tipo_despesa.nome,
            "status": despesa.status_financas.nome,
            "lote_frango": getattr(despesa.lote_frango, "identificacao", None),
            "data": despesa.data.isoformat(),
            "valor": float(despesa.valor),
            "descricao": despesa.descricao if despesa.descricao else None,
        }
    )

def deletar_index_despesa(id):
    es.delete(index=INDEX, id=id, ignore=[404])