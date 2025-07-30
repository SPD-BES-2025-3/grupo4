
CREATE TABLE IF NOT EXISTS produto_crm (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10,2) NOT NULL CHECK (preco >= 0),
    estoque INTEGER NOT NULL DEFAULT 0 CHECK (estoque >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



CREATE INDEX IF NOT EXISTS idx_produto_nome ON produto_crm(nome);
CREATE INDEX IF NOT EXISTS idx_produto_preco ON produto_crm(preco);
CREATE INDEX IF NOT EXISTS idx_produto_estoque ON produto_crm(estoque);
CREATE INDEX IF NOT EXISTS idx_produto_preco_estoque ON produto_crm(preco, estoque);

CREATE TRIGGER update_produto_crm_updated_at
    BEFORE UPDATE ON produto_crm 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE INDEX IF NOT EXISTS idx_produto_busca ON produto_crm USING gin(to_tsvector('portuguese', nome || ' ' || COALESCE(descricao, '')));