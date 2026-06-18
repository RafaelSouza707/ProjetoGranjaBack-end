# Para fazer uso do projeto siga as instruções:
## Clone e entre no projeto
`git clone https://github.com/RafaelSouza707/ProjetoGranjaBack-end`
`cd Back_end/`

## Copiar o exemplo de .env (já vem configurado)
`cp .env.example .env`

## Inicializar containers, fique atento ao fato da máquina possuir docker
`docker compose up -d --build`

## Verifique se os containers estão ativos
`docker ps`

## Execuar o migrate do projeto para fazer o banco de dados ficar adequado
`docker compose exec api flask db upgrade`

## Após isso acessar os end-points para teste.
#
#
## Fique informado que para a atividade "Atividade 4 - Cache e serviços" foram escolhidos as entidades contidas no diretorio "granja": 
* consumo_lote_diaria - /consumo_lote_diaria;
* lote_frangos - /lote_frango;
* lote_racao - /lote_racao;
* mortalidade - /mortalidade;
* status_lote_frango - /status_lote_frango;
* tipo_produto - /tipo_produto; e
* tipo_racao /tipo_racao.
