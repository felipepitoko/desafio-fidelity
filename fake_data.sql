INSERT INTO estado (UF, Cod_Fornecedor, Nome) VALUES
('AC', 101, 'Acre'),
('AL', 102, 'Alagoas'),
('AP', 103, 'Amapá'),
('AM', 104, 'Amazonas'),
('BA', 105, 'Bahia'),
('CE', 106, 'Ceará'),
('DF', 107, 'Distrito Federal'),
('ES', 108, 'Espírito Santo'),
('GO', 109, 'Goiás'),
('MA', 110, 'Maranhão'),
('MT', 111, 'Mato Grosso'),
('MS', 112, 'Mato Grosso do Sul'),
('MG', 113, 'Minas Gerais'),
('PA', 114, 'Pará'),
('PB', 115, 'Paraíba'),
('PR', 116, 'Paraná'),
('PE', 117, 'Pernambuco'),
('PI', 118, 'Piauí'),
('RJ', 119, 'Rio de Janeiro'),
('RN', 120, 'Rio Grande do Norte'),
('RS', 121, 'Rio Grande do Sul'),
('RO', 122, 'Rondônia'),
('RR', 123, 'Roraima'),
('SC', 124, 'Santa Catarina'),
('SP', 125, 'São Paulo'),
('SE', 126, 'Sergipe'),
('TO', 127, 'Tocantins');

INSERT INTO lote (Cod_Lote_Prazo, Data_Criacao, Cod_Funcionario, Tipo, Prioridade) VALUES
(202301, '2023-10-01', 10, 'Background Check', 'Alta'),
(202302, '2023-10-05', 12, 'Verificação de Crédito', 'Média'),
(202303, '2023-10-10', 10, 'Consulta Simples', 'Baixa'),
(202304, '2023-10-12', 15, 'Background Check', 'Crítica'),
(202305, '2023-10-15', 12, 'Consulta Urgente', 'Alta'),
(202306, '2023-10-20', 18, 'Verificação de Crédito', 'Média'),
(202307, '2023-10-22', 10, 'Consulta Simples', 'Baixa'),
(202308, '2023-10-25', 19, 'Background Check', 'Alta'),
(202309, '2023-10-28', 15, 'Consulta Urgente', 'Crítica'),
(202310, '2023-11-01', 12, 'Verificação de Crédito', 'Média');

-- Mock data for the 'fornecedor' table
-- Note: Cod_Fornecedor is explicitly set to match the foreign keys in the 'estado' table.
INSERT INTO fornecedor (Cod_Fornecedor, Nome, Cnpj, Telefone, Email) VALUES
(101, 'Provedor de Dados Alpha', '11.111.111/0001-11', '(11) 91111-1111', 'contato@alpha.com'),
(102, 'Beta Informações Ltda', '22.222.222/0001-22', '(21) 92222-2222', 'suporte@beta.com.br'),
(103, 'Gamma Soluções de Checagem', '33.333.333/0001-33', '(31) 93333-3333', 'vendas@gamma-solucoes.com'),
(104, 'Delta Pesquisas S.A.', '44.444.444/0001-44', '(41) 94444-4444', 'comercial@delta.com'),
(105, 'Epsilon Consultoria', '55.555.555/0001-55', '(51) 95555-5555', 'atendimento@epsilon.net'),
(106, 'Zeta Data Services', '66.666.666/0001-66', '(61) 96666-6666', 'contato@zetaservicos.com.br'),
(107, 'Omega Analytics', '77.777.777/0001-77', '(71) 97777-7777', 'suporte@omegaanalytics.com');

-- Mock data for the 'funcionario' table
-- Note: Cod_Funcionario is explicitly set to match the foreign keys in the 'lote' table.
INSERT INTO funcionario (Cod_Funcionario, Nome, Cpf_funcionario) VALUES
(10, 'Ana Carolina Silva', '111.222.333-44'),
(12, 'Bruno Costa Santos', '222.333.444-55'),
(15, 'Carlos Dias Almeida', '333.444.555-66'),
(18, 'Daniela Souza Pereira', '444.555.666-77'),
(19, 'Eduardo Lima Ferreira', '555.666.777-88');

-- Mock data for the 'servico' table
INSERT INTO servico (cod_servico, civil, criminal) VALUES
(1, 'Busca de Processos Cíveis', 'Busca de Antecedentes Criminais Estaduais'),
(2, 'Verificação de Protestos', 'Busca de Antecedentes Criminais Federais'),
(3, 'Consulta de Bens e Imóveis', 'Verificação de Mandados de Prisão'),
(4, 'Análise de Participação Societária', 'Consulta a Processos Criminais (Todas as Instâncias)');

-- Mock data for the 'pesquisa' table
-- Assumes cod_pesquisa will be generated from 1 to 10
INSERT INTO pesquisa (cod_cliente, cod_uf, cod_servico, tipo, cpf, cod_uf_nascimento, cod_uf_rg, data_entrada, data_conclusao, nome, nome_corrigido, rg, rg_corrigido, mae, mae_corrigido, anexo) VALUES
(501, 25, 1, 'Pessoa Física', '029.890.902-23', 25, 25, '2023-10-01 09:00:00', NULL, 'Felipe Sousa da Costa', 'Felipe Sousa da Costa', '5329371', '5329371', NULL, NULL, 'anexo_felipe.pdf');
-- (502, 19, 2, 'Pessoa Física', '987.654.321-09', 19, 19, '2023-10-05 10:00:00', '2023-10-06 11:30:00', 'Mariana Oliveira', 'Mariana de Oliveira', '98.765.432-1', '98.765.432-1', 'Ana Oliveira', 'Ana de Oliveira', 'anexo_mariana.pdf'),
-- (501, 13, 4, 'Pessoa Física', '111.222.333-44', 13, 13, '2023-10-10 11:00:00', NULL, 'Pedro Souza', 'Pedro de Souza', '11.223.344-5', '11.223.344-5', 'Beatriz Souza', 'Beatriz de Souza', NULL),
-- (503, 5, 1, 'Pessoa Física', '444.555.666-77', 5, 5, '2023-10-12 14:00:00', '2023-10-13 15:00:00', 'Lucas Costa', 'Lucas da Costa', '44.556.677-8', '44.556.677-8', 'Fernanda Costa', 'Fernanda da Costa', 'anexo_lucas.pdf'),
-- (504, 21, 3, 'Pessoa Física', '777.888.999-00', 1, 21, '2023-10-15 15:30:00', NULL, 'Juliana Pereira', 'Juliana Alves Pereira', '77.889.900-1', '77.889.900-1', 'Sandra Pereira', 'Sandra Alves Pereira', NULL),
-- (502, 24, 2, 'Pessoa Física', '234.567.890-12', 24, 24, '2023-10-20 08:45:00', '2023-10-21 17:00:00', 'Gabriel Martins', 'Gabriel Martins Junior', '23.456.789-0', '23.456.789-0', 'Carla Martins', 'Carla Martins', 'anexo_gabriel.pdf'),
-- (505, 11, 1, 'Pessoa Física', '345.678.901-23', 11, 11, '2023-10-22 13:00:00', NULL, 'Larissa Almeida', 'Larissa de Almeida', '34.567.890-1', '34.567.890-1', 'Sonia Almeida', 'Sonia de Almeida', NULL),
-- (501, 7, 4, 'Pessoa Física', '456.789.012-34', 7, 7, '2023-10-25 16:20:00', '2023-10-26 18:00:00', 'Rafael Rodrigues', 'Rafael Rodrigues Filho', '45.678.901-2', '45.678.901-2', 'Teresa Rodrigues', 'Teresa Rodrigues', 'anexo_rafael.pdf'),
-- (503, 16, 3, 'Pessoa Física', '567.890.123-45', 16, 16, '2023-10-28 10:10:00', NULL, 'Fernanda Lima', 'Fernanda Lima e Silva', '56.789.012-3', '56.789.012-3', 'Vera Lima', 'Vera Lima e Silva', NULL),
-- (504, 27, 1, 'Pessoa Física', '678.901.234-56', 27, 27, '2023-11-01 11:00:00', '2023-11-02 14:00:00', 'Thiago Barbosa', 'Thiago Barbosa', '67.890.123-4', '67.890.123-4', 'Eliane Barbosa', 'Eliane Barbosa', 'anexo_thiago.pdf');

-- Mock data for the 'lote_pesquisa' table
-- This table links each 'lote' with its corresponding 'pesquisa'
INSERT INTO lote_pesquisa (Cod_Lote, Cod_Pesquisa, Cod_Funcionario, Cod_Funcionario_Conclusao, Cod_Fornecedor, Data_Entrada, Data_Conclusao, Cod_UF, Obs) VALUES
(1, 1, 10, 10, 104, '2025-07-01 09:05:00', NULL, 25, NULL);
-- (2, 2, 12, 12, 105, '2023-10-05 10:05:00', '2023-10-06 11:25:00', 19, 'Verificação de crédito no RJ finalizada.'),
-- (3, 3, 10, NULL, 106, '2023-10-10 11:05:00', NULL, 13, 'Pesquisa em MG em andamento.'),
-- (4, 4, 15, 15, 105, '2023-10-12 14:05:00', '2023-10-13 14:50:00', 5, 'Background check na BA concluído com urgência.'),
-- (5, 5, 12, NULL, 107, '2023-10-15 15:35:00', NULL, 21, 'Pesquisa no RS aguardando documentos.'),
-- (6, 6, 18, 18, 103, '2023-10-20 08:50:00', '2023-10-21 16:50:00', 24, 'Verificação de crédito em SC finalizada.'),
-- (7, 7, 10, NULL, 104, '2023-10-22 13:05:00', NULL, 11, 'Pesquisa em MT em andamento.'),
-- (8, 8, 19, 19, 107, '2023-10-25 16:25:00', '2023-10-26 17:45:00', 7, 'Background check no DF concluído.'),
-- (9, 9, 15, NULL, 102, '2023-10-28 10:15:00', NULL, 16, 'Pesquisa urgente no PR em andamento.'),
-- (10, 10, 12, 12, 106, '2023-11-01 11:05:00', '2023-11-02 13:55:00', 27, 'Pesquisa em TO concluída.');

-- Mock data for the 'pesquisa_spv' table
-- Each row represents a specific, logged search action for a given 'pesquisa'.
INSERT INTO pesquisa_spv (Cod_Pesquisa, cod_spv, cod_spv_computador, cod_spv_tipo, cod_funcionario, filtro, website_id, resultado) VALUES
(1, 'SPV001', 'BOT_SP_01', 'AUTOMATICA', 10, 'CPF,NOME_COMPLETO', 'tjsp.jus.br', NULL);
-- (2, 'SPV002', 'BOT_CREDITO_03', 'AUTOMATICA', 12, 'CPF', 'serasa.com.br', 'Score: 750. Nenhuma pendência encontrada.'),
-- (4, 'SPV003', 'ANALISTA_DESK_05', 'MANUAL', 15, 'NOME_COMPLETO,NOME_MAE', 'tjba.jus.br', 'Verificado manualmente. Sem registros correspondentes.'),
-- (6, 'SPV004', 'BOT_SC_02', 'AUTOMATICA', 18, 'CPF', 'protestosc.com.br', 'Nenhum protesto localizado para o CPF informado.'),
-- (8, 'SPV005', 'BOT_DF_01', 'AUTOMATICA', 19, 'CPF', 'tjdft.jus.br', '1 processo cível encontrado. Status: Baixado/Arquivado.'),
-- (10, 'SPV006', 'ANALISTA_DESK_02', 'MANUAL', 12, 'NOME_COMPLETO', 'tjto.jus.br', 'Pesquisa manual realizada. Nenhum registro encontrado.');
