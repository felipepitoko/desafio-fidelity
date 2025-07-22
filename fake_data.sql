-- This script populates the tables in an order that respects foreign key constraints.
-- NOTE: SERIAL primary keys (like cod_estado, cod_lote, etc.) start at 1 by default.
-- The INSERT statements below assume this behavior for foreign key references.
 
-- 1. Populate 'estado' table
-- We insert São Paulo first, so we know its cod_estado will be 1.
INSERT INTO estado (nome_estado, sigla_estado) VALUES
('São Paulo', 'SP'),       -- cod_estado = 1
('Rio de Janeiro', 'RJ'),  -- cod_estado = 2
('Minas Gerais', 'MG');     -- cod_estado = 3
 
-- 2. Populate 'lote_pesquisa' table
-- Create two batches for searches with different deadlines.
INSERT INTO lote_pesquisa (prazo_lote) VALUES
('2025-07-31 23:59:59'), -- cod_lote = 1
('2025-07-31 23:59:59'); -- cod_lote = 2
 
-- 3. Populate 'filtro_enriquecimento' table
-- Defines the types of search filters available and their corresponding HTML element IDs.
INSERT INTO filtro_enriquecimento (descricao_filtro, referencia_html_filtro) VALUES
('CPF', 'campo_DOCPARTE'),  -- cod_filtro = 1
('Nome', 'campo_NMPARTE'),  -- cod_filtro = 2
('RG', 'campo_DOCPARTE');   -- cod_filtro = 3
 
-- 4. Populate 'tipo_enriquecimento' table
-- Defines specific enrichment services, linking them to a state, URL, and filter type.
INSERT INTO tipo_enriquecimento (descricao_enriquecimento, uf_referencia, url_enriquecimento, cod_filtro) VALUES
('Consulta de processos TJSP por CPF', 1, 'https://esaj.tjsp.jus.br/cpopg/open.do', 1), -- cod_tipo_enriquecimento = 1
('Consulta de processos TJSP por Nome', 1, 'https://esaj.tjsp.jus.br/cpopg/open.do', 2), -- cod_tipo_enriquecimento = 2
('Consulta de processos TJSP por RG', 1, 'https://esaj.tjsp.jus.br/cpopg/open.do', 3);  -- cod_tipo_enriquecimento = 3
 
-- 5. Populate 'pesquisa' table
-- All searches are for São Paulo (uf_rg = 1, uf_pesquisa = 1). The new 'uf_pesquisa' column is added.
INSERT INTO pesquisa (cod_lote, cpf_consultado, nome_consultado, rg_consultado, uf_rg, uf_pesquisa, data_nascimento, data_pesquisa) VALUES
(1, '11122233344', 'Ana Silva', '123456789', 1, 1, '1990-05-15', '2023-10-26 10:00:00'), -- cod_pesquisa = 1
(1, '55566677788', 'Bruno Costa', '987654321', 1, 1, '1985-08-20', '2023-10-26 11:30:00'), -- cod_pesquisa = 2
(2, '99988877766', 'Carla Dias', '555444333', 1, 1, '1992-02-10', '2023-10-27 09:00:00'); -- cod_pesquisa = 3