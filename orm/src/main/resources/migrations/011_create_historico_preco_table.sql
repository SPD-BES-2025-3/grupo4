
CREATE TABLE IF NOT EXISTS historico_preco (
    id SERIAL PRIMARY KEY,
    produto_id INTEGER NOT NULL,
    preco_anterior DECIMAL(10,2) NOT NULL CHECK (preco_anterior >= 0),
    preco_novo DECIMAL(10,2) NOT NULL CHECK (preco_novo >= 0),
    data_mudanca TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    motivo VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE historico_preco
ADD CONSTRAINT fk_historico_preco_produto 
FOREIGN KEY (produto_id) REFERENCES produto_crm(id) ON DELETE CASCADE;

COMMENT ON TABLE historico_preco IS 'Tabela para armazenar histórico de mudanças de preço dos produtos';
COMMENT ON COLUMN historico_preco.id IS 'Identificador único do registro de histórico';
COMMENT ON COLUMN historico_preco.produto_id IS 'Referência ao produto';
COMMENT ON COLUMN historico_preco.preco_anterior IS 'Preço anterior do produto';
COMMENT ON COLUMN historico_preco.preco_novo IS 'Novo preço do produto';
COMMENT ON COLUMN historico_preco.data_mudanca IS 'Data e hora da mudança de preço';
COMMENT ON COLUMN historico_preco.motivo IS 'Motivo da mudança de preço';
COMMENT ON COLUMN historico_preco.created_at IS 'Data de criação do registro';

CREATE INDEX IF NOT EXISTS idx_historico_preco_produto ON historico_preco(produto_id);
CREATE INDEX IF NOT EXISTS idx_historico_preco_data ON historico_preco(data_mudanca);
CREATE INDEX IF NOT EXISTS idx_historico_preco_produto_data ON historico_preco(produto_id, data_mudanca);

CREATE OR REPLACE FUNCTION registrar_mudanca_preco()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.preco != NEW.preco THEN
        INSERT INTO historico_preco (produto_id, preco_anterior, preco_novo, motivo)
        VALUES (NEW.id, OLD.preco, NEW.preco, 'Atualização automática');
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER trigger_registrar_mudanca_preco 
    AFTER UPDATE ON produto_crm 
    FOR EACH ROW 
    EXECUTE FUNCTION registrar_mudanca_preco(); 