
CREATE TABLE IF NOT EXISTS cliente_crm (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    endereco_id INTEGER NOT NULL,
    numero_telefone VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE cliente_crm
ADD CONSTRAINT fk_cliente_endereco 
FOREIGN KEY (endereco_id) REFERENCES endereco(id) ON DELETE RESTRICT;

CREATE INDEX IF NOT EXISTS idx_cliente_email ON cliente_crm(email);
CREATE INDEX IF NOT EXISTS idx_cliente_nome ON cliente_crm(nome);
CREATE INDEX IF NOT EXISTS idx_cliente_endereco ON cliente_crm(endereco_id);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_cliente_crm_updated_at 
    BEFORE UPDATE ON cliente_crm 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column(); 