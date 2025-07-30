

CREATE TABLE IF NOT EXISTS auditoria (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER,
    tipo_usuario VARCHAR(20) NOT NULL CHECK (tipo_usuario IN ('Cliente', 'Administrador')),
    acao VARCHAR(50) NOT NULL,
    tabela_afetada VARCHAR(50),
    registro_id INTEGER,
    dados_anteriores JSONB,
    dados_novos JSONB,
    ip_address INET,
    user_agent TEXT,
    data_acao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);



CREATE INDEX IF NOT EXISTS idx_auditoria_usuario ON auditoria(usuario_id);
CREATE INDEX IF NOT EXISTS idx_auditoria_tipo_usuario ON auditoria(tipo_usuario);
CREATE INDEX IF NOT EXISTS idx_auditoria_acao ON auditoria(acao);
CREATE INDEX IF NOT EXISTS idx_auditoria_data ON auditoria(data_acao);
CREATE INDEX IF NOT EXISTS idx_auditoria_tabela ON auditoria(tabela_afetada);
CREATE INDEX IF NOT EXISTS idx_auditoria_usuario_data ON auditoria(usuario_id, data_acao);

CREATE OR REPLACE FUNCTION registrar_auditoria(
    p_usuario_id INTEGER,
    p_tipo_usuario VARCHAR(20),
    p_acao VARCHAR(50),
    p_tabela_afetada VARCHAR(50),
    p_registro_id INTEGER,
    p_dados_anteriores JSONB DEFAULT NULL,
    p_dados_novos JSONB DEFAULT NULL,
    p_ip_address INET DEFAULT NULL,
    p_user_agent TEXT DEFAULT NULL
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO auditoria (
        usuario_id, tipo_usuario, acao, tabela_afetada, registro_id,
        dados_anteriores, dados_novos, ip_address, user_agent
    ) VALUES (
        p_usuario_id, p_tipo_usuario, p_acao, p_tabela_afetada, p_registro_id,
        p_dados_anteriores, p_dados_novos, p_ip_address, p_user_agent
    );
END;
$$ LANGUAGE plpgsql; 