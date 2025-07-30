
INSERT INTO endereco (rua, numero, bairro, cidade, estado, cep, complemento) VALUES
('Rua das Flores', '123', 'Centro', 'Goiânia', 'GO', '74000-000', 'Apto 101'),
('Avenida Principal', '456', 'Setor Bueno', 'Goiânia', 'GO', '74230-120', 'Sala 205'),
('Rua do Comércio', '789', 'Setor Central', 'Goiânia', 'GO', '74000-100', 'Loja 10'),
('Avenida Universitária', '321', 'Setor Universitário', 'Goiânia', 'GO', '74605-010', 'Casa 5'),
('Rua da Paz', '654', 'Setor Marista', 'Goiânia', 'GO', '74120-030', 'Apto 302')
ON CONFLICT DO NOTHING;

INSERT INTO cliente_crm (nome, email, senha, endereco_id, numero_telefone) VALUES
('João Silva', 'joao@email.com', 'senha123', 1, '(62) 99999-9999'),
('Maria Santos', 'maria@email.com', 'senha456', 2, '(62) 88888-8888'),
('Pedro Costa', 'pedro@email.com', 'senha789', 3, '(62) 77777-7777'),
('Ana Oliveira', 'ana@email.com', 'senha012', 4, '(62) 66666-6666'),
('Carlos Lima', 'carlos@email.com', 'senha345', 5, '(62) 55555-5555')
ON CONFLICT (email) DO NOTHING;

INSERT INTO administrador (nome, email, senha, endereco_id) VALUES
('Admin Principal', 'admin@empresa.com', 'admin123', 1),
('Gerente Vendas', 'gerente@empresa.com', 'gerente456', 2)
ON CONFLICT (email) DO NOTHING;

INSERT INTO produto_crm (nome, descricao, preco, estoque, categoria_id) VALUES
('Notebook Dell Inspiron', 'Notebook Dell Inspiron 15 polegadas, 8GB RAM, 256GB SSD', 2999.99, 10, 2),
('Smartphone Samsung Galaxy', 'Smartphone Samsung Galaxy S21, 128GB, Preto', 3999.99, 25, 3),
('Mouse USB Logitech', 'Mouse USB Logitech M185, Sem Fio, Preto', 29.99, 50, 2),
('Livro Java Programming', 'Livro sobre programação Java, 500 páginas', 89.90, 15, 4),
('Tênis Nike Air Max', 'Tênis Nike Air Max 270, Tamanho 42', 599.99, 8, 7),
('Fone de Ouvido Bluetooth', 'Fone de ouvido Bluetooth JBL, Cancelamento de Ruído', 299.99, 20, 1),
('Câmera Digital Canon', 'Câmera Digital Canon EOS Rebel T7, 24.1MP', 2499.99, 5, 1),
('Tablet Samsung Galaxy Tab', 'Tablet Samsung Galaxy Tab A7, 10.4 polegadas', 1299.99, 12, 1),
('Teclado Mecânico RGB', 'Teclado mecânico RGB com switches Cherry MX', 399.99, 30, 2),
('Monitor LG 24 polegadas', 'Monitor LG 24 polegadas, Full HD, IPS', 899.99, 18, 2)
ON CONFLICT DO NOTHING;

INSERT INTO carrinho (cliente_id, total, status) VALUES
(1, 0.00, 'Ativo'),
(2, 0.00, 'Ativo'),
(3, 0.00, 'Ativo')
ON CONFLICT DO NOTHING;

INSERT INTO item_carrinho (carrinho_id, produto_id, quantidade, preco_unitario, subtotal) VALUES
(1, 1, 1, 2999.99, 2999.99),
(1, 3, 2, 29.99, 59.98),
(2, 2, 1, 3999.99, 3999.99),
(2, 6, 1, 299.99, 299.99),
(3, 5, 1, 599.99, 599.99)
ON CONFLICT DO NOTHING;

UPDATE carrinho SET total = (
    SELECT COALESCE(SUM(subtotal), 0.00) 
    FROM item_carrinho 
    WHERE carrinho_id = carrinho.id
);

INSERT INTO pedido_crm (data, status, total, cliente_id) VALUES
(CURRENT_TIMESTAMP - INTERVAL '5 days', 'Entregue', 3059.97, 1),
(CURRENT_TIMESTAMP - INTERVAL '3 days', 'Enviado', 4299.98, 2),
(CURRENT_TIMESTAMP - INTERVAL '1 day', 'Em Processamento', 599.99, 3),
(CURRENT_TIMESTAMP, 'Pendente', 0.00, 4)
ON CONFLICT DO NOTHING;

INSERT INTO item_pedido (pedido_id, produto_id, quantidade, preco_unitario, subtotal) VALUES
(1, 1, 1, 2999.99, 2999.99),
(1, 3, 2, 29.99, 59.98),
(2, 2, 1, 3999.99, 3999.98),
(2, 6, 1, 299.99, 299.99),
(3, 5, 1, 599.99, 599.99)
ON CONFLICT DO NOTHING;

UPDATE pedido_crm SET total = (
    SELECT COALESCE(SUM(subtotal), 0.00) 
    FROM item_pedido 
    WHERE pedido_id = pedido_crm.id
);

INSERT INTO historico_preco (produto_id, preco_anterior, preco_novo, motivo) VALUES
(1, 2799.99, 2999.99, 'Ajuste de preço'),
(2, 3799.99, 3999.99, 'Aumento de custos'),
(3, 24.99, 29.99, 'Atualização de preço'),
(4, 79.90, 89.90, 'Reajuste de preço')
ON CONFLICT DO NOTHING;

INSERT INTO auditoria (usuario_id, tipo_usuario, acao, tabela_afetada, registro_id, dados_anteriores, dados_novos, ip_address, user_agent) VALUES
(1, 'Cliente', 'LOGIN', 'cliente_crm', 1, NULL, '{"email": "joao@email.com"}', '192.168.1.100', 'Mozilla/5.0'),
(2, 'Cliente', 'CREATE', 'carrinho', 2, NULL, '{"cliente_id": 2, "total": 0.00}', '192.168.1.101', 'Mozilla/5.0'),
(1, 'Administrador', 'UPDATE', 'produto_crm', 1, '{"preco": 2799.99}', '{"preco": 2999.99}', '192.168.1.102', 'Mozilla/5.0'),
(2, 'Cliente', 'CREATE', 'pedido_crm', 2, NULL, '{"cliente_id": 2, "total": 4299.98}', '192.168.1.103', 'Mozilla/5.0')
ON CONFLICT DO NOTHING;

DO $$
BEGIN
    RAISE NOTICE 'Dados de exemplo inseridos com sucesso!';
    RAISE NOTICE 'Endereços: 5 registros';
    RAISE NOTICE 'Clientes: 5 registros';
    RAISE NOTICE 'Administradores: 2 registros';
    RAISE NOTICE 'Produtos: 10 registros';
    RAISE NOTICE 'Carrinhos: 3 registros';
    RAISE NOTICE 'Itens de carrinho: 5 registros';
    RAISE NOTICE 'Pedidos: 4 registros';
    RAISE NOTICE 'Itens de pedido: 5 registros';
    RAISE NOTICE 'Histórico de preços: 4 registros';
    RAISE NOTICE 'Auditoria: 4 registros';
END $$; 