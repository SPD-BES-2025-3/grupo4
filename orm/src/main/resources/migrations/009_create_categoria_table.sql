

CREATE TABLE IF NOT EXISTS categoria (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao TEXT,
    ativo BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE categoria IS 'Tabela para armazenar categorias de produtos';
COMMENT ON COLUMN categoria.id IS 'Identificador único da categoria';
COMMENT ON COLUMN categoria.nome IS 'Nome da categoria (único)';
COMMENT ON COLUMN categoria.descricao IS 'Descrição da categoria';
COMMENT ON COLUMN categoria.ativo IS 'Indica se a categoria está ativa';
COMMENT ON COLUMN categoria.created_at IS 'Data de criação do registro';
COMMENT ON COLUMN categoria.updated_at IS 'Data da última atualização';

CREATE INDEX IF NOT EXISTS idx_categoria_nome ON categoria(nome);
CREATE INDEX IF NOT EXISTS idx_categoria_ativo ON categoria(ativo);

CREATE TRIGGER update_categoria_updated_at
    BEFORE UPDATE ON categoria 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

INSERT INTO categoria (nome, descricao) VALUES
('Eletrônicos', 'Produtos eletrônicos e tecnológicos'),
('Informática', 'Computadores, notebooks e acessórios'),
('Smartphones', 'Telefones celulares e acessórios'),
('Livros', 'Livros físicos e digitais'),
('Casa e Jardim', 'Produtos para casa e jardim'),
('Esportes', 'Produtos esportivos e fitness'),
('Moda', 'Roupas, calçados e acessórios'),
('Beleza', 'Produtos de beleza e cosméticos'),
('Brinquedos', 'Brinquedos e jogos'),
('Outros', 'Outras categorias de produtos')
ON CONFLICT (nome) DO NOTHING; 