
ALTER TABLE produto_crm 
ADD COLUMN categoria_id INTEGER;

ALTER TABLE produto_crm
ADD CONSTRAINT fk_produto_categoria 
FOREIGN KEY (categoria_id) REFERENCES categoria(id) ON DELETE SET NULL;

COMMENT ON COLUMN produto_crm.categoria_id IS 'Referência à categoria do produto';

CREATE INDEX IF NOT EXISTS idx_produto_categoria ON produto_crm(categoria_id);

UPDATE produto_crm
SET categoria_id = (SELECT id FROM categoria WHERE nome = 'Outros' LIMIT 1)
WHERE categoria_id IS NULL; 