from helpers.extensao_elasticsearch import es

INDEX = "despesas"

def despesa_criar_index():
    if not es.indices.exists(index=INDEX):
        es.indices.create(
            index=INDEX,
            mappings={
                "properties": {
                    "tipo": {"type": "text"},
                    "status": {"type": "text"},
                    "lote_frango": {"type": "text"},
                    "data": {"type": "date"},
                    "valor": {"type": "float"},
                    "descricao": {"type": "text"},
                }
            }
        )