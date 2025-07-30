package com.exemplo.hello.model;

import java.util.ArrayList;
import java.util.List;

public class Carrinho {
    private List<ProdutoCRM> produtos = new ArrayList<>();
    private double total = 0.0;

    public void adicionarProduto(ProdutoCRM produto) {
        produtos.add(produto);
        total += produto.getPreco();
    }

    public void removerProduto(ProdutoCRM produto) {
        produtos.remove(produto);
        total -= produto.getPreco();
    }

    public void limpar() {
        produtos.clear();
        total = 0.0;
    }

    public List<ProdutoCRM> getProdutos() {
        return produtos;
    }

    public double getTotal() {
        return total;
    }
}
