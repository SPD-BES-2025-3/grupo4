
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

BEGIN;

SET session_replication_role = replica;

DROP TRIGGER IF EXISTS trigger_registrar_mudanca_preco ON produto_crm;
DROP TRIGGER IF EXISTS update_auditoria_updated_at ON auditoria;
DROP TRIGGER IF EXISTS update_historico_preco_updated_at ON historico_preco;
DROP TRIGGER IF EXISTS update_categoria_updated_at ON categoria;
DROP TRIGGER IF EXISTS update_item_carrinho_updated_at ON item_carrinho;
DROP TRIGGER IF EXISTS calculate_item_carrinho_subtotal ON item_carrinho;
DROP TRIGGER IF EXISTS update_carrinho_updated_at ON carrinho;
DROP TRIGGER IF EXISTS update_item_pedido_updated_at ON item_pedido;
DROP TRIGGER IF EXISTS calculate_item_pedido_subtotal ON item_pedido;
DROP TRIGGER IF EXISTS update_pedido_crm_updated_at ON pedido_crm;
DROP TRIGGER IF EXISTS update_produto_crm_updated_at ON produto_crm;
DROP TRIGGER IF EXISTS update_administrador_updated_at ON administrador;
DROP TRIGGER IF EXISTS update_cliente_crm_updated_at ON cliente_crm;

DROP FUNCTION IF EXISTS registrar_mudanca_preco() CASCADE;
DROP FUNCTION IF EXISTS registrar_auditoria(INTEGER, VARCHAR, VARCHAR, VARCHAR, INTEGER, JSONB, JSONB, INET, TEXT) CASCADE;
DROP FUNCTION IF EXISTS calculate_item_subtotal() CASCADE;
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;

DROP TABLE IF EXISTS auditoria CASCADE;
DROP TABLE IF EXISTS historico_preco CASCADE;
DROP TABLE IF EXISTS item_carrinho CASCADE;
DROP TABLE IF EXISTS carrinho CASCADE;
DROP TABLE IF EXISTS item_pedido CASCADE;
DROP TABLE IF EXISTS pedido_crm CASCADE;
DROP TABLE IF EXISTS produto_crm CASCADE;
DROP TABLE IF EXISTS categoria CASCADE;
DROP TABLE IF EXISTS administrador CASCADE;
DROP TABLE IF EXISTS cliente_crm CASCADE;
DROP TABLE IF EXISTS endereco CASCADE;

SET session_replication_role = DEFAULT;

COMMIT;

DO $$
BEGIN
    RAISE NOTICE 'Todas as migrations foram revertidas com sucesso!';
    RAISE NOTICE 'Todas as tabelas foram removidas.';
END $$; 