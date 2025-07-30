

CREATE TABLE IF NOT EXISTS endereco (
    id SERIAL PRIMARY KEY,
    rua VARCHAR(255) NOT NULL,
    numero VARCHAR(20) NOT NULL,
    bairro VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(2) NOT NULL,
    cep VARCHAR(10) NOT NULL,
    complemento VARCHAR(255)
);

COMMENT ON TABLE endereco IS 'Tabela para armazenar endereços dos clientes e administradores';
COMMENT ON COLUMN endereco.id IS 'Identificador único do endereço';
COMMENT ON COLUMN endereco.rua IS 'Nome da rua';
COMMENT ON COLUMN endereco.numero IS 'Número do endereço';
COMMENT ON COLUMN endereco.bairro IS 'Nome do bairro';
COMMENT ON COLUMN endereco.cidade IS 'Nome da cidade';
COMMENT ON COLUMN endereco.estado IS 'Sigla do estado (UF)';
COMMENT ON COLUMN endereco.cep IS 'Código de Endereçamento Postal';
COMMENT ON COLUMN endereco.complemento IS 'Complemento do endereço (opcional)';

CREATE INDEX IF NOT EXISTS idx_endereco_cep ON endereco(cep);
CREATE INDEX IF NOT EXISTS idx_endereco_cidade ON endereco(cidade);
CREATE INDEX IF NOT EXISTS idx_endereco_estado ON endereco(estado); 