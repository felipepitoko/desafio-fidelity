-- Tables are created in an order that respects foreign key dependencies.

-- Table: lote_pesquisa
-- Stores batch information for searches.
CREATE TABLE lote_pesquisa (
    cod_lote SERIAL PRIMARY KEY,
    prazo_lote TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Table: estado
-- Stores state information.
CREATE TABLE estado (
    cod_estado SERIAL PRIMARY KEY,
    nome_estado VARCHAR(100) NOT NULL,
    sigla_estado VARCHAR(2) NOT NULL
);

-- Table: filtro_enriquecimento
-- Defines the types of search filters available.
CREATE TABLE filtro_enriquecimento(
    cod_filtro SERIAL PRIMARY KEY,
    descricao_filtro VARCHAR(100) NOT NULL,
    referencia_html_filtro VARCHAR(500) NOT NULL, -- e.g., 'campo_DOCPARTE', 'campo_NMPARTE'
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Table: tipo_enriquecimento
-- Defines different types of data enrichment that can be performed.
-- Depends on 'estado' and 'filtro_enriquecimento'.
CREATE TABLE tipo_enriquecimento (
    cod_tipo_enriquecimento SERIAL PRIMARY KEY,
    descricao_enriquecimento VARCHAR(100) NOT NULL,
    uf_referencia INTEGER NOT NULL,
    url_enriquecimento VARCHAR(500) NOT NULL,
    cod_filtro INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (cod_filtro) REFERENCES filtro_enriquecimento(cod_filtro),
    FOREIGN KEY (uf_referencia) REFERENCES estado(cod_estado)
);

-- Table: pesquisa
-- The core table for search requests. Depends on 'lote_pesquisa' and 'estado'.
CREATE TABLE pesquisa (
    cod_pesquisa SERIAL PRIMARY KEY,
    cod_lote INTEGER NOT NULL,
    cpf_consultado VARCHAR(11) NOT NULL,
    nome_consultado VARCHAR(100) NOT NULL,
    rg_consultado VARCHAR(11) NOT NULL,
    uf_rg INTEGER NOT NULL, --FK estado
    uf_pesquisa INTEGER NOT NULL, --FK estado
    data_nascimento DATE NOT NULL,
    data_pesquisa TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (cod_lote) REFERENCES lote_pesquisa(cod_lote),
    FOREIGN KEY (uf_rg) REFERENCES estado(cod_estado),
    FOREIGN KEY (uf_pesquisa) REFERENCES estado(cod_estado)
);

-- Table: log_enriquecimento
-- Logs the enrichment attempts for each search. Depends on 'pesquisa' and 'tipo_enriquecimento'.
CREATE TABLE log_enriquecimento (
    cod_log_enriquecimento SERIAL PRIMARY KEY,
    cod_pesquisa INTEGER NOT NULL,
    cod_tipo_enriquecimento INTEGER NOT NULL,
    status_enriquecimento VARCHAR(100) NOT NULL,
    enriquecimento_concluido BOOLEAN NOT NULL DEFAULT FALSE,
    resultado_enriquecimento VARCHAR(500) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (cod_pesquisa) REFERENCES pesquisa(cod_pesquisa),
    FOREIGN KEY (cod_tipo_enriquecimento) REFERENCES tipo_enriquecimento(cod_tipo_enriquecimento)
);