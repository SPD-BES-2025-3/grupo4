""" Temporariamente quebrado """

import sys, os 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from models.produto import Produto

@pytest.fixture
def produto_base():
    return Produto(
        nome="Camiseta Básica",
        descricao="Camiseta de algodão",
        preco=100.0,
        estoque=10,
        categoria="Vestuário"
    )

def test_str_representation(produto_base):
    texto = str(produto_base)
    assert "Camiseta Básica" in texto
    assert "R$" in texto
    assert "(Estoque:" in texto

def test_aplicar_desconto_valido(produto_base):
    produto_base.aplicar_desconto(20)
    assert produto_base.preco == 80.0

def test_aplicar_desconto_limites(produto_base):
    produto_base.aplicar_desconto(0)
    assert produto_base.preco == 100.0
    produto_base.aplicar_desconto(100)
    assert produto_base.preco == 0.0

def test_aplicar_desconto_invalido(produto_base):
    produto_base.aplicar_desconto(-10)  # Não deve aplicar
    assert produto_base.preco == 100.0
    produto_base.aplicar_desconto(150)  # Também não deve aplicar
    assert produto_base.preco == 100.0

def test_atualizar_estoque_incremento(produto_base):
    produto_base.atualizar_estoque(5)
    assert produto_base.estoque == 15

def test_atualizar_estoque_decremento(produto_base):
    produto_base.atualizar_estoque(-3)
    assert produto_base.estoque == 7

def test_atualizar_estoque_nao_negativo(produto_base):
    produto_base.atualizar_estoque(-20)
    assert produto_base.estoque == 0
