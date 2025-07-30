
CREATE TABLE IF NOT EXISTS administrador (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    endereco_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE administrador
ADD CONSTRAINT fk_administrador_endereco 
FOREIGN KEY (endereco_id) REFERENCES endereco(id) ON DELETE RESTRICT;

CREATE INDEX IF NOT EXISTS idx_administrador_email ON administrador(email);
CREATE INDEX IF NOT EXISTS idx_administrador_nome ON administrador(nome);
CREATE INDEX IF NOT EXISTS idx_administrador_endereco ON administrador(endereco_id);

CREATE TRIGGER update_administrador_updated_at
    BEFORE UPDATE ON administrador 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column(); 