CREATE TABLE pedido_crm (
    id SERIAL PRIMARY KEY,
    data TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL DEFAULT 'Pendente' CHECK (status IN ('Pendente', 'Aprovado', 'Em Processamento', 'Enviado', 'Entregue', 'Cancelado')),
    total DECIMAL(10,2) NOT NULL DEFAULT 0.00 CHECK (total >= 0),
    cliente_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE pedido_crm
ADD CONSTRAINT fk_pedido_cliente 
FOREIGN KEY (cliente_id) REFERENCES cliente_crm(id) ON DELETE RESTRICT;



CREATE INDEX IF NOT EXISTS idx_pedido_cliente ON pedido_crm(cliente_id);
CREATE INDEX IF NOT EXISTS idx_pedido_data ON pedido_crm(data);
CREATE INDEX IF NOT EXISTS idx_pedido_status ON pedido_crm(status);
CREATE INDEX IF NOT EXISTS idx_pedido_total ON pedido_crm(total);
CREATE INDEX IF NOT EXISTS idx_pedido_cliente_data ON pedido_crm(cliente_id, data);
CREATE INDEX IF NOT EXISTS idx_pedido_status_data ON pedido_crm(status, data);

CREATE TRIGGER update_pedido_crm_updated_at
    BEFORE UPDATE ON pedido_crm 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column(); 