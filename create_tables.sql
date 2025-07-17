-- Table: estado
CREATE TABLE estado (
    Cod_UF SERIAL PRIMARY KEY,
    UF VARCHAR(50),
    Cod_Fornecedor INT,
    Nome VARCHAR(255)
);

-- Table: lote
CREATE TABLE lote (
    Cod_Lote SERIAL PRIMARY KEY,
    Cod_Lote_Prazo INT,
    Data_Criacao DATE,
    Cod_Funcionario INT, -- This is likely a FK to a 'funcionario' table not shown
    Tipo VARCHAR(100),
    Prioridade VARCHAR(50)
);

-- Table: servico
CREATE TABLE servico (
    cod_servico SERIAL PRIMARY KEY,
    civil VARCHAR(255),
    criminal VARCHAR(255)
);

-- Table: pesquisa
CREATE TABLE pesquisa (
    cod_pesquisa SERIAL PRIMARY KEY,
    cod_cliente INT, -- This is likely a FK to a 'cliente' table not shown
    cod_uf INT, -- FK to estado
    cod_servico INT, -- FK to servico
    tipo VARCHAR(100),
    cpf VARCHAR(14), -- Assuming standard CPF format 'XXX.XXX.XXX-XX'
    cod_uf_nascimento INT, -- FK to estado for birthplace UF
    cod_uf_rg INT, -- FK to estado for RG issuing UF
    data_entrada TIMESTAMP,
    data_conclusao TIMESTAMP,
    nome VARCHAR(255),
    nome_corrigido VARCHAR(255),
    rg VARCHAR(20),
    rg_corrigido VARCHAR(20),
    mae VARCHAR(255),
    mae_corrigido VARCHAR(255),
    anexo TEXT, -- Assuming anexo can be a path or a description
    FOREIGN KEY (cod_uf) REFERENCES estado(Cod_UF),
    FOREIGN KEY (cod_servico) REFERENCES servico(cod_servico),
    FOREIGN KEY (cod_uf_nascimento) REFERENCES estado(Cod_UF),
    FOREIGN KEY (cod_uf_rg) REFERENCES estado(Cod_UF)
);

-- Table: lote_pesquisa
CREATE TABLE lote_pesquisa (
    Cod_Lote_Pesquisa SERIAL PRIMARY KEY,
    Cod_Lote INT, -- FK to lote
    Cod_Pesquisa INT, -- FK to pesquisa
    Cod_Funcionario INT, -- This is likely a FK to a 'funcionario' table not shown
    Cod_Funcionario_Conclusao INT, -- This is likely a FK to a 'funcionario' table not shown
    Cod_Fornecedor INT, -- FK to estado (assuming Cod_Fornecedor in estado is a master list of suppliers)
    Data_Entrada TIMESTAMP,
    Data_Conclusao TIMESTAMP,
    Cod_UF INT, -- FK to estado
    Obs TEXT,
    FOREIGN KEY (Cod_Lote) REFERENCES lote(Cod_Lote),
    FOREIGN KEY (Cod_Pesquisa) REFERENCES pesquisa(cod_pesquisa),
    FOREIGN KEY (Cod_UF) REFERENCES estado(Cod_UF)
    -- FOREIGN KEY (Cod_Fornecedor) REFERENCES estado(Cod_Fornecedor) -- This FK might be tricky as Cod_Fornecedor in estado is not a PK
);

-- Table: pesquisa_spv
CREATE TABLE pesquisa_spv (
    Cod_pesquisa SERIAL PRIMARY KEY, -- This might be a FK to pesquisa or a separate PK
    cod_spv VARCHAR(100),
    cod_spv_computador VARCHAR(100),
    cod_spv_tipo VARCHAR(100),
    cod_funcionario INT, -- This is likely a FK to a 'funcionario' table not shown
    filtro TEXT,
    website_id VARCHAR(255),
    resultado TEXT
    -- FOREIGN KEY (Cod_pesquisa) REFERENCES pesquisa(cod_pesquisa) -- If it's a FK
);