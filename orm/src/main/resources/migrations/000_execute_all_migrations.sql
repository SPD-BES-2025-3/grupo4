SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

BEGIN;
\i 001_create_endereco_table.sql
\i 002_create_cliente_crm_table.sql
\i 003_create_administrador_table.sql
\i 004_create_produto_crm_table.sql
\i 005_create_pedido_crm_table.sql
\i 006_create_item_pedido_table.sql
\i 007_create_carrinho_table.sql
\i 008_create_item_carrinho_table.sql
\i 009_create_categoria_table.sql
\i 010_add_categoria_to_produto.sql
\i 011_create_historico_preco_table.sql
\i 012_create_auditoria_table.sql
\i 013_insert_sample_data.sql
COMMIT;

DO $$
BEGIN
    RAISE NOTICE 'Todas as migrations foram executadas com sucesso!';
    RAISE NOTICE 'Tabelas criadas: endereco, cliente_crm, administrador, produto_crm, pedido_crm, item_pedido, carrinho, item_carrinho, categoria, historico_preco, auditoria';
END $$; 