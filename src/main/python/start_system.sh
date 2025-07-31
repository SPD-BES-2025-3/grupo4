#!/bin/bash

# 🚀 Script de Inicialização do Sistema Redis
# PostgreSQL (Java) → MongoDB (Python)

echo "============================================================"
echo "🚀 INICIANDO SISTEMA DE SINCRONIZAÇÃO REDIS"
echo "PostgreSQL (Java) → MongoDB (Python)"
echo "============================================================"

# Verificar se estamos no diretório correto
if [ ! -f "redis_receiver_final.py" ]; then
    echo "❌ Execute este script de dentro do diretório src/main/python"
    echo "Comando: cd src/main/python && ./start_system.sh"
    exit 1
fi

# Função para verificar se um comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar dependências
echo "🔍 Verificando dependências..."

# Verificar Redis
if command_exists redis-cli; then
    if redis-cli ping >/dev/null 2>&1; then
        echo "✅ Redis está rodando"
    else
        echo "⚠️ Redis não está rodando. Iniciando..."
        redis-server --daemonize yes
        sleep 2
        if redis-cli ping >/dev/null 2>&1; then
            echo "✅ Redis iniciado com sucesso"
        else
            echo "❌ Erro ao iniciar Redis"
            exit 1
        fi
    fi
else
    echo "❌ Redis não está instalado"
    echo "Instale com: sudo apt install redis-server redis-tools"
    exit 1
fi

# Verificar MongoDB
if command_exists mongosh; then
    if mongosh --eval "db.runCommand('ping')" >/dev/null 2>&1; then
        echo "✅ MongoDB está rodando"
    else
        echo "❌ MongoDB não está rodando"
        echo "Inicie com: sudo systemctl start mongod"
        exit 1
    fi
else
    echo "❌ MongoDB não está instalado"
    exit 1
fi

# Verificar ambiente Python
if [ ! -d "venv" ]; then
    echo "⚠️ Ambiente virtual não encontrado. Criando..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "🐍 Ativando ambiente Python..."
source venv/bin/activate

# Verificar dependências Python
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt não encontrado"
    exit 1
fi

echo "📦 Verificando dependências Python..."
pip install -r requirements.txt >/dev/null 2>&1

# Parar receptor anterior se estiver rodando
echo "🛑 Parando receptor anterior..."
pkill -f redis_receiver_final.py 2>/dev/null
sleep 2

# Iniciar receptor
echo "🚀 Iniciando receptor Python..."
echo "============================================================"
echo "📋 COMANDOS ÚTEIS:"
echo "• Parar receptor: pkill -f redis_receiver_final.py"
echo "• Verificar MongoDB: mongosh --eval 'use ecommerce; db.produtos.find().pretty()'"
echo "• Verificar status: ps aux | grep redis_receiver_final"
echo "============================================================"
echo ""

# Executar receptor
python redis_receiver_final.py 