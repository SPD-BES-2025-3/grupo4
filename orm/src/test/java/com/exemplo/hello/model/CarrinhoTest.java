package com.exemplo.hello.model;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;
import java.util.List;

public class CarrinhoTest {
    
    private Carrinho carrinho;
    private ProdutoCRM produto1;
    private ProdutoCRM produto2;
    
    @Before
    public void setUp() {
        carrinho = new Carrinho();
        
        produto1 = new ProdutoCRM();
        produto1.setId(1);
        produto1.setNome("Notebook Dell");
        produto1.setPreco(2999.99);
        produto1.setEstoque(10);
        
        produto2 = new ProdutoCRM();
        produto2.setId(2);
        produto2.setNome("Mouse USB");
        produto2.setPreco(29.99);
        produto2.setEstoque(50);
    }
    
    @Test
    public void testCarrinhoVazio() {
        assertTrue(carrinho.getProdutos().isEmpty());
        assertEquals(0.0, carrinho.getTotal(), 0.01);
    }
    
    @Test
    public void testAdicionarProduto() {
        carrinho.adicionarProduto(produto1);
        
        List<ProdutoCRM> produtos = carrinho.getProdutos();
        assertEquals(1, produtos.size());
        assertEquals(produto1, produtos.get(0));
        assertEquals(2999.99, carrinho.getTotal(), 0.01);
    }
    
    @Test
    public void testAdicionarMultiplosProdutos() {
        carrinho.adicionarProduto(produto1);
        carrinho.adicionarProduto(produto2);
        
        List<ProdutoCRM> produtos = carrinho.getProdutos();
        assertEquals(2, produtos.size());
        assertEquals(produto1, produtos.get(0));
        assertEquals(produto2, produtos.get(1));
        assertEquals(3029.98, carrinho.getTotal(), 0.01);
    }
    
    @Test
    public void testRemoverProduto() {
        carrinho.adicionarProduto(produto1);
        carrinho.adicionarProduto(produto2);
        
        carrinho.removerProduto(produto1);
        
        List<ProdutoCRM> produtos = carrinho.getProdutos();
        assertEquals(1, produtos.size());
        assertEquals(produto2, produtos.get(0));
        assertEquals(29.99, carrinho.getTotal(), 0.01);
    }
    
    @Test
    public void testRemoverProdutoInexistente() {
        carrinho.adicionarProduto(produto1);
        
        carrinho.removerProduto(produto2);
        
        List<ProdutoCRM> produtos = carrinho.getProdutos();
        assertEquals(1, produtos.size());
        assertEquals(produto1, produtos.get(0));
        // O total é subtraído mesmo que o produto não exista (comportamento atual da classe)
        assertEquals(2970.0, carrinho.getTotal(), 0.01);
    }
    
    @Test
    public void testLimparCarrinho() {
        carrinho.adicionarProduto(produto1);
        carrinho.adicionarProduto(produto2);
        
        carrinho.limpar();
        
        assertTrue(carrinho.getProdutos().isEmpty());
        assertEquals(0.0, carrinho.getTotal(), 0.01);
    }
    
    @Test
    public void testLimparCarrinhoVazio() {
        carrinho.limpar();
        
        assertTrue(carrinho.getProdutos().isEmpty());
        assertEquals(0.0, carrinho.getTotal(), 0.01);
    }
    
    @Test
    public void testGetProdutos() {
        carrinho.adicionarProduto(produto1);
        carrinho.adicionarProduto(produto2);
        
        List<ProdutoCRM> produtos = carrinho.getProdutos();
        assertNotNull(produtos);
        assertEquals(2, produtos.size());
    }
    
    @Test
    public void testGetTotal() {
        assertEquals(0.0, carrinho.getTotal(), 0.01);
        
        carrinho.adicionarProduto(produto1);
        assertEquals(2999.99, carrinho.getTotal(), 0.01);
        
        carrinho.adicionarProduto(produto2);
        assertEquals(3029.98, carrinho.getTotal(), 0.01);
    }
} 