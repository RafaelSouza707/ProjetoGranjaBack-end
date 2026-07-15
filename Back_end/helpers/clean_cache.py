from helpers.cache import cache

class CacheService:

    @staticmethod
    def limpar_cache_despesa(granja_id):
        redis = cache.cache._write_client

        for key in redis.scan_iter(
            f"cache:granja:{granja_id}:despesa:*"
        ):
            redis.delete(key)

    @staticmethod
    def limpar_cache_receitas(granja_id):
        redis = cache.cache._write_client

        for key in redis.scan_iter(
            f"cache:granja:{granja_id}:receita:*"
        ):
            redis.delete(key)

    @staticmethod
    def limpar_cache_consumo_lote_diaria(granja_id, lote_frango_id):
        redis = cache.cache._write_client

        if lote_frango_id:
            pattern = (
                f"cache:granja:{granja_id}:lote_frango:{lote_frango_id}:consumos_lote_diaria"
            )
        else:
            pattern = (
                f"cache:granja:{granja_id}:lote_frango:consumos_lote_diaria"
            )

        for key in redis.scan_iter(pattern):
            redis.delete(key)
    

    @staticmethod
    def limpar_cache_cards_lote_frango(granja_id):
        cache.delete(f"cache:granja:{granja_id}:lote_frango:cards_lote_frango")


    @staticmethod
    def limpar_cache_card_lote_racao(granja_id):
        cache.delete(f"cache:granja:{granja_id}:lotes_racoes:cards")

    @staticmethod
    def limpar_cache_lote_frango(granja_id):
        cache.delete(f"cache:granja:{granja_id}:lote_frango")

    @staticmethod
    def limpar_cache_mortalidade(granja_id, lote_frango_id):
        redis = cache.cache._write_client

        if lote_frango_id:
            pattern = (
                f"cache:granja:{granja_id}:lote_frango:{lote_frango_id}:mortalidade"
            )
        else:
            pattern = (
                f"cache:granja:{granja_id}:lote_frango:mortalidade"
            )

        for key in redis.scan_iter(pattern):
            redis.delete(key)

    @staticmethod
    def limpar_cache_lote_racao(granja_id):
        cache.delete(f"cache:granja:{granja_id}:lote_racao")

    @staticmethod
    def limpar_cache_status_lote_frango(granja_id):
        cache.delete(f"cache:granja:{granja_id}:status_lote_frango")
    
    @staticmethod
    def limpar_cache_tipo_produto(granja_id):
        cache.delete(f"cache:granja:{granja_id}:tipo_produto")

    @staticmethod
    def limpar_cache_tipo_racao(granja_id):
        cache.delete(f"cache:granja:{granja_id}:tipo_racao")

    @staticmethod
    def limpar_cache_cards_gastos_granja(granja_id):
        cache.delete(f"cache:granja:{granja_id}:despesa:cards_gastos")
    
    @staticmethod
    def limpar_cache_despesa_granja(granja_id):
        redis = cache.cache._write_client

        for key in redis.scan_iter(
            f"cache:granja:{granja_id}:despesa:pagina:*"
        ):
            redis.delete(key)

    @staticmethod
    def limpar_cache_cards_financas(granja_id):
        cache.delete(f"cache:granja:{granja_id}:despesa:cards_financas")
    
    @staticmethod
    def limpar_cache_cards_receita_granja(granja_id):
        cache.delete(f"cache:granja:{granja_id}:receita:cards_receitas")
    
    @staticmethod
    def limpar_cache_receita(granja_id):
        redis = cache.cache._write_client

        for key in redis.scan_iter(
            f"cache:granja:{granja_id}:receita:pagina:*"
        ):
            redis.delete(key)
    
    @staticmethod
    def limpar_cache_status_financas(granja_id):
        cache.delete(f"cache:granja:{granja_id}:status_financas")

    @staticmethod
    def limpar_cache_tipo_despesa(granja_id):
        cache.delete(f"cache:granja:{granja_id}:tipo_despesa")

    @staticmethod
    def limpar_cache_tipo_receita(granja_id):
        cache.delete(f"cache:granja:{granja_id}:tipo_receita")

    @staticmethod
    def limpar_cache_cards_granja(granja_id):
        cache.delete(f"cache:granja:{granja_id}:cards")

    @staticmethod
    def deletar_cache_granja(user_id):
        cache.delete(f"cache:user:{user_id}")

    @staticmethod
    def deletar_cache_cliente(granja_id):
        cache.delete(f"cache:user:granja:{granja_id}:cliente")
    
    @staticmethod
    def deletar_cache_sexo():
        cache.delete(f"cache:sexo")

    @staticmethod
    def deletar_cache_item_venda(granja_id):
        cache.delete(f"cache:granja:{granja_id}:item_venda")

    @staticmethod
    def deletar_cache_movimentacao_estoque(granja_id):
        cache.delete(f"cache:granja:{granja_id}:movimentacao_estoque")

    @staticmethod
    def deletar_cache_producao(granja_id, lote_frango_id):
        redis = cache.cache._write_client

        if lote_frango_id:
            pattern = (
                f"cache:granja:{granja_id}:lote_frango:{lote_frango_id}:producao"
            )
        else:
            pattern = (
                f"cache:granja:{granja_id}:producao"
            )

        for key in redis.scan_iter(pattern):
            redis.delete(key)
    

    @staticmethod
    def deletar_cache_produto(granja_id):
        cache.delete(f"cache:granja:{granja_id}:produto")

    @staticmethod
    def deletar_cache_tipo_movimentacao(granja_id):
        cache.delete(f"cache:granja:{granja_id}:tipo_movimentacao")
    
    @staticmethod
    def deletar_cache_tipo_unidade_medida(granja_id):
        cache.delete(f"cache:granja:{granja_id}:tipo_unidade_medida")
    
    @staticmethod
    def deletar_cache_tipo_venda(granja_id):
        cache.delete(f"cache:granja:{granja_id}:tipo_venda")

    @staticmethod
    def deletar_cache_venda(granja_id):
        cache.delete(f"cache:granja:{granja_id}:venda")