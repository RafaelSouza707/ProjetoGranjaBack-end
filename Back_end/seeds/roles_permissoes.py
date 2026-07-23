ROLES = [
    "OPERADOR",
    "ADMINISTRADOR",
    "MASTER"
]

PERMISSOES = [
    "AVIARIO",
    "ESTOQUE",
    "FINANCAS",
    "VENDA",
    "GRANJA",
    "MOVER_USUARIOS",
    "GERENCIAR_CARGOS",
    "MINHA_CONTA"
]

ROLE_PERMISSOES = {
    "OPERADOR": [
        "AVIARIO",
        "ESTOQUE",
        "MINHA_CONTA",
        "VENDA"
    ],

    "ADMINISTRADOR": [
        "AVIARIO",
        "ESTOQUE",
        "FINANCAS",
        "VENDA",
        "MOVER_USUARIOS",
        "GERENCIAR_CARGOS",
        "MINHA_CONTA"
    ],

    "MASTER": [
        "AVIARIO",
        "ESTOQUE",
        "FINANCAS",
        "VENDA",
        "GRANJA",
        "MOVER_USUARIOS",
        "GERENCIAR_CARGOS",
        "MINHA_CONTA"
    ]
}