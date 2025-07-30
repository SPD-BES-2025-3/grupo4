
CREATE TABLE IF NOT EXISTS item_carrinho (
    id SERIAL PRIMARY KEY,
    carrinho_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario DECIMAL(10,2) NOT NULL CHECK (preco_unitario >= 0),
    subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE item_carrinho
ADD CONSTRAINT fk_item_carrinho_carrinho 
FOREIGN KEY (carrinho_id) REFERENCES carrinho(id) ON DELETE CASCADE;

ALTER TABLE item_carrinho 
ADD CONSTRAINT fk_item_carrinho_produto 
FOREIGN KEY (produto_id) REFERENCES produto_crm(id) ON DELETE RESTRICT;

CREATE INDEX IF NOT EXISTS idx_item_carrinho_carrinho ON item_carrinho(carrinho_id);
CREATE INDEX IF NOT EXISTS idx_item_carrinho_produto ON item_carrinho(produto_id);
CREATE INDEX IF NOT EXISTS idx_item_carrinho_quantidade ON item_carrinho(quantidade);
CREATE INDEX IF NOT EXISTS idx_item_carrinho_subtotal ON item_carrinho(subtotal);

CREATE TRIGGER update_item_carrinho_updated_at
    BEFORE UPDATE ON item_carrinho 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER calculate_item_carrinho_subtotal
    BEFORE INSERT OR UPDATE ON item_carrinho 
    FOR EACH ROW 
    EXECUTE FUNCTION calculate_item_subtotal(); 