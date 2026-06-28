from helpers.extensao_elasticsearch import es
from elastic.despesa_index import INDEX

def buscar_despesas(termo):
    resp = es.search(
        index=INDEX,
        query={
            "multi_match": {
                "query": termo,
                "fields": ["status", "identificacao", "quantidade_atual"],
                "fuzziness": "AUTO"
            }
        }
    )

    return [hit["_source"] for hit in resp["hits"]["hits"]]