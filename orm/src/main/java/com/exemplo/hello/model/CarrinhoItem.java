package com.exemplo.hello.model;

public class CarrinhoItem {
    private ProdutoCRM produto;
    private int quantidade;

    public CarrinhoItem(ProdutoCRM produto, int quantidade) {
        this.produto = produto;
        this.quantidade = quantidade;
    }

    public ProdutoCRM getProduto() {
        return produto;
    }

    public int getQuantidade() {
        return quantidade;
    }

    public void setQuantidade(int quantidade) {
        this.quantidade = quantidade;
    }

    public double getSubtotal() {
        return produto.getPreco() * quantidade;
    }
}