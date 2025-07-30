
CREATE TABLE IF NOT EXISTS item_pedido (
    id SERIAL PRIMARY KEY,
    pedido_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario DECIMAL(10,2) NOT NULL CHECK (preco_unitario >= 0),
    subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE item_pedido
ADD CONSTRAINT fk_item_pedido_pedido 
FOREIGN KEY (pedido_id) REFERENCES pedido_crm(id) ON DELETE CASCADE;

ALTER TABLE item_pedido 
ADD CONSTRAINT fk_item_pedido_produto 
FOREIGN KEY (produto_id) REFERENCES produto_crm(id) ON DELETE RESTRICT;

COMMENT ON TABLE item_pedido IS 'Tabela para armazenar itens de cada pedido';
COMMENT ON COLUMN item_pedido.id IS 'Identificador único do item do pedido';
COMMENT ON COLUMN item_pedido.pedido_id IS 'Referência ao pedido';
COMMENT ON COLUMN item_pedido.produto_id IS 'Referência ao produto';
COMMENT ON COLUMN item_pedido.quantidade IS 'Quantidade do produto no pedido';
COMMENT ON COLUMN item_pedido.preco_unitario IS 'Preço unitário do produto no momento do pedido';
COMMENT ON COLUMN item_pedido.subtotal IS 'Subtotal do item (quantidade * preço_unitario)';
COMMENT ON COLUMN item_pedido.created_at IS 'Data de criação do registro';
COMMENT ON COLUMN item_pedido.updated_at IS 'Data da última atualização';

CREATE INDEX IF NOT EXISTS idx_item_pedido_pedido ON item_pedido(pedido_id);
CREATE INDEX IF NOT EXISTS idx_item_pedido_produto ON item_pedido(produto_id);
CREATE INDEX IF NOT EXISTS idx_item_pedido_quantidade ON item_pedido(quantidade);
CREATE INDEX IF NOT EXISTS idx_item_pedido_subtotal ON item_pedido(subtotal);

CREATE TRIGGER update_item_pedido_updated_at
    BEFORE UPDATE ON item_pedido 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE OR REPLACE FUNCTION calculate_item_subtotal()
RETURNS TRIGGER AS $$
BEGIN
    NEW.subtotal = NEW.quantidade * NEW.preco_unitario;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER calculate_item_pedido_subtotal 
    BEFORE INSERT OR UPDATE ON item_pedido 
    FOR EACH ROW 
    EXECUTE FUNCTION calculate_item_subtotal(); 