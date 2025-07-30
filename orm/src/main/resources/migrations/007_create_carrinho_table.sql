
CREATE TABLE IF NOT EXISTS carrinho (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    total DECIMAL(10,2) NOT NULL DEFAULT 0.00 CHECK (total >= 0),
    status VARCHAR(20) NOT NULL DEFAULT 'Ativo' CHECK (status IN ('Ativo', 'Finalizado', 'Abandonado')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE carrinho
ADD CONSTRAINT fk_carrinho_cliente 
FOREIGN KEY (cliente_id) REFERENCES cliente_crm(id) ON DELETE CASCADE;



CREATE INDEX IF NOT EXISTS idx_carrinho_cliente ON carrinho(cliente_id);
CREATE INDEX IF NOT EXISTS idx_carrinho_status ON carrinho(status);
CREATE INDEX IF NOT EXISTS idx_carrinho_total ON carrinho(total);
CREATE INDEX IF NOT EXISTS idx_carrinho_cliente_status ON carrinho(cliente_id, status);

CREATE TRIGGER update_carrinho_updated_at
    BEFORE UPDATE ON carrinho 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column(); 