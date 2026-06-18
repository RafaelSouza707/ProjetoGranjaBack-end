-- ==========================================
-- TIPO RAÇÃO
-- ==========================================

INSERT INTO tipo_racao (nome, descricao) VALUES
('inicial', 'Ração utilizada nas primeiras semanas'),
('crescimento', 'Ração para fase de crescimento'),
('terminação', 'Ração para fase final de engorda');

-- ==========================================
-- TIPO PRODUTO
-- ==========================================

INSERT INTO tipo_produto (nome) VALUES
('ovos'),
('frango vivo'),
('esterco'),
('pinto de um dia'),
('frango abatido');

-- ==========================================
-- STATUS LOTE FRANGO
-- ==========================================

INSERT INTO status_lote_frango (nome) VALUES
('ativo'),
('finalizado'),
('cancelado');

-- ==========================================
-- LOTE RAÇÃO
-- ==========================================

INSERT INTO lote_racao (
    tipo_racao_id,
    fornecedor,
    data_compra,
    quilos,
    valor
) VALUES
(
    1,
    'NutriRacao LTDA',
    '2026-01-05',
    5000.000,
    12500.00
),
(
    2,
    'AgroFeed LTDA',
    '2026-02-01',
    6000.000,
    15600.00
),
(
    3,
    'NutriRacao LTDA',
    '2026-03-01',
    7000.000,
    18900.00
);

-- ==========================================
-- LOTE FRANGO
-- ==========================================

INSERT INTO lote_frango (
    status_lote_frango_id,
    identificacao,
    quantidade_inicial,
    data_alojamento,
    fornecedor,
    quantidade_atual,
    observacao
) VALUES
(
    1,
    'A1',
    500,
    '2026-01-10',
    'Agi Ota',
    500,
    'Primeiro lote do ano'
),
(
    1,
    'A2',
    500,
    '2026-02-10',
    'Agi Ota',
    500,
    'Primeiro lote do ano'
),
(
    1,
    'A3',
    500,
    '2026-03-10',
    'Agi Ota',
    500,
    'Primeiro lote do ano'
),
(
    1,
    'LF-2026-001',
    600,
    '2026-04-10',
    'Agi Ota',
    500,
    'Primeiro lote do ano'
),
(
    1,
    'LF-2026-002',
    1000,
    '2026-04-11',
    'Agi Ota',
    500,
    'Lote em fase de crescimento'
);

-- ==========================================
-- MORTALIDADE
-- ==========================================

INSERT INTO mortalidade (
    lote_frango_id,
    data,
    quantidade_mortes
) VALUES
(
    1,
    '2026-01-10',
    5
),
(
    1,
    '2026-01-11',
    5
),
(
    1,
    '2026-01-12',
    5
),
(
    1,
    '2026-01-13',
    5
),
(
    1,
    '2026-01-14',
    5
),
(
    1,
    '2026-01-15',
    5
),
(
    1,
    '2026-01-16',
    5
),
(
    1,
    '2026-01-17',
    10
),
(
    2,
    '2026-02-10',
    8
),
(
    2,
    '2026-02-11',
    8
),
(
    2,
    '2026-02-12',
    8
),
(
    2,
    '2026-02-13',
    8
),
(
    2,
    '2026-02-14',
    8
),
(
    2,
    '2026-02-14',
    8
);

-- ==========================================
-- CONSUMO LOTE DIÁRIA
-- ==========================================

INSERT INTO consumo_lote_diaria (
    lote_frango_id,
    lote_racao_id,
    data,
    quilos
) VALUES
(
    1,
    1,
    '2026-01-11',
    120.500
),
(
    1,
    1,
    '2026-01-12',
    118.750
),
(
    1,
    1,
    '2026-01-13',
    118.750
),
(
    1,
    1,
    '2026-01-14',
    118.750
),
(
    1,
    1,
    '2026-01-14',
    118.750
),
(
    1,
    1,
    '2026-01-15',
    118.750
),
(
    1,
    2,
    '2026-02-01',
    135.200
),
(
    2,
    2,
    '2026-02-16',
    140.000
),
(
    2,
    3,
    '2026-03-01',
    155.800
);
