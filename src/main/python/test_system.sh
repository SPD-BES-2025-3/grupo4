#!/bin/bash

# 🧪 Script de Teste do Sistema Redis
# Testa se o sistema está funcionando corretamente

echo "============================================================"
echo "TESTE DO SISTEMA DE SINCRONIZAÇÃO REDIS"
echo "============================================================"

# Verificar se estamos no diretório correto
if [ ! -f "redis_receiver_final.py" ]; then
    echo "Execute este script de dentro do diretório src/main/python"
    echo "Comando: cd src/main/python && ./test_system.sh"
    exit 1
fi

# Função para verificar status
check_status() {
    echo "Verificando status dos serviços..."
    
    # Verificar Redis
    if redis-cli ping >/dev/null 2>&1; then
        echo "Redis: Conectado"
    else
        echo "Redis: Não conectado"
        return 1
    fi
    
    # Verificar MongoDB
    if mongosh --eval "db.runCommand('ping')" >/dev/null 2>&1; then
        echo "MongoDB: Conectado"
    else
        echo "MongoDB: Não conectado"
        return 1
    fi
    
    # Verificar receptor Python
    if pgrep -f redis_receiver_final.py >/dev/null; then
        echo "Receptor Python: Rodando"
    else
        echo "Receptor Python: Não está rodando"
        return 1
    fi
    
    return 0
}

# Verificar produtos no MongoDB
check_products() {
    echo "📦 Verificando produtos no MongoDB..."
    count=$(mongosh --quiet --eval "use ecommerce; db.produtos.countDocuments()")
    echo "📊 Produtos encontrados: $count"
    
    if [ "$count" -gt 0 ]; then
        echo "📋 Últimos produtos:"
        mongosh --quiet --eval "use ecommerce; db.produtos.find().sort({_id: -1}).limit(3).pretty()"
    fi
}

# Teste de envio
test_send() {
    echo "📤 Testando envio de mensagem..."
    cd src/main/python
    source venv/bin/activate
    
    echo "Teste de envio concluído"
}

# Menu principal
echo ""
echo "📋 Escolha uma opção:"
echo "1. Verificar status dos serviços"
echo "2. Verificar produtos no MongoDB"
echo "3. Testar envio de mensagem"
echo "4. Teste completo"
echo "5. Sair"
echo ""

read -p "Digite sua opção (1-5): " choice

case $choice in
    1)
        check_status
        ;;
    2)
        check_products
        ;;
    3)
        test_send
        ;;
    4)
        echo "🧪 Executando teste completo..."
        check_status
        if [ $? -eq 0 ]; then
            check_products
            test_send
            echo ""
            echo "Teste completo executado!"
        else
            echo "Alguns serviços não estão funcionando"
        fi
        ;;
    5)
        echo "👋 Saindo..."
        exit 0
        ;;
    *)
        echo "Opção inválida"
        exit 1
        ;;
esac

echo ""
echo "Teste concluído!" 