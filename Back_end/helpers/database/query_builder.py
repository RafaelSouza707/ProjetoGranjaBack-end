from flask import request
from sqlalchemy import or_, cast, String


class QueryBuilder:

    IGNORAR = {
        "page",
        "per_page",
        "search",
        "sort",
        "order",
        "granjaId",
        "pagina"
    }

    def __init__(self, model, query):
        self.model = model
        self.query = query
        self.filters = getattr(model, "__filters__", {})

    def build(self):
        self._filters()
        self._search()
        self._order()
        return self.query

    ######################################################
    # FILTROS
    ######################################################

    def _filters(self):
        for parametro, valor in request.args.items():
            if parametro in self.IGNORAR or not valor:
                continue

            param_limpo = parametro
            operador = "exact"

            if "__" in parametro:
                param_limpo, operador = parametro.split("__", 1)

            # Verifica se o parâmetro está direto ou se é um alias mapeado
            nome_campo_real = None
            cfg_filtro = None

            if param_limpo in self.filters:
                nome_campo_real = param_limpo
                cfg_filtro = self.filters[param_limpo]
            else:
                # Procura se algum filtro possui esse parâmetro como alias
                for campo_model, cfg in self.filters.items():
                    aliases = cfg.get("alias", [])
                    if isinstance(aliases, str):
                        aliases = [aliases]
                    if param_limpo in aliases:
                        nome_campo_real = campo_model
                        cfg_filtro = cfg
                        break

            if not nome_campo_real or not hasattr(self.model, nome_campo_real):
                continue

            coluna = getattr(self.model, nome_campo_real)

            # Se for data_inicio / data_fim mapeado via range/alias especial ou operador customizado
            match operador:
                case "exact":
                    self.query = self.query.filter(coluna == valor)

                case "contains":
                    self.query = self.query.filter(
                        cast(coluna, String).ilike(f"%{valor}%")
                    )

                case "startswith":
                    self.query = self.query.filter(
                        cast(coluna, String).ilike(f"{valor}%")
                    )

                case "endswith":
                    self.query = self.query.filter(
                        cast(coluna, String).ilike(f"%{valor}")
                    )

                case "gt" | "gte" | "inicio":
                    # Suporte flexível para gte ou _inicio
                    op = ">=" if operador in ("gte", "inicio") else ">"
                    if op == ">=":
                        self.query = self.query.filter(coluna >= valor)
                    else:
                        self.query = self.query.filter(coluna > valor)

                case "lt" | "lte" | "fim":
                    # Suporte flexível para lte ou _fim
                    op = "<=" if operador in ("lte", "fim") else "<"
                    if op == "<=":
                        self.query = self.query.filter(coluna <= valor)
                    else:
                        self.query = self.query.filter(coluna < valor)

                case "between":
                    minimo, maximo = valor.split(",")
                    self.query = self.query.filter(
                        coluna.between(minimo, maximo)
                    )

                case "in":
                    valores = valor.split(",")
                    self.query = self.query.filter(
                        coluna.in_(valores)
                    )

    ######################################################
    # BUSCA GERAL
    ######################################################

    def _search(self):
        texto = request.args.get("search")
        if not texto:
            return

        campos = []
        for nome, cfg in self.filters.items():
            if not cfg.get("search", False):
                continue

            if not hasattr(self.model, nome):
                continue

            coluna = getattr(self.model, nome)
            campos.append(
                cast(coluna, String).ilike(f"%{texto}%")
            )

        if campos:
            self.query = self.query.filter(
                or_(*campos)
            )

    ######################################################
    # ORDENAÇÃO
    ######################################################

    def _order(self):
        campo = request.args.get("sort")
        if not campo:
            default = getattr(
                self.model,
                "__default_order__",
                None
            )
            if default:
                self.query = self.query.order_by(default.desc())
            return

        if campo not in self.filters or not hasattr(self.model, campo):
            return

        coluna = getattr(self.model, campo)
        ordem = request.args.get("order", "asc")

        if ordem.lower() == "desc":
            self.query = self.query.order_by(coluna.desc())
        else:
            self.query = self.query.order_by(coluna.asc())