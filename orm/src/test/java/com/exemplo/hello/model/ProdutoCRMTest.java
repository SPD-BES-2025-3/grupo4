package com.exemplo.hello.model;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class ProdutoCRMTest {
    
    private ProdutoCRM produto;
    
    @Before
    public void setUp() {
        produto = new ProdutoCRM();
    }
    
    @Test
    public void testSetAndGetId() {
        produto.setId(1);
        assertEquals(1, produto.getId());
    }
    
    @Test
    public void testSetAndGetNome() {
        produto.setNome("Notebook Dell");
        assertEquals("Notebook Dell", produto.getNome());
    }
    
    @Test
    public void testSetAndGetDescricao() {
        produto.setDescricao("Notebook Dell Inspiron 15 polegadas");
        assertEquals("Notebook Dell Inspiron 15 polegadas", produto.getDescricao());
    }
    
    @Test
    public void testSetAndGetPreco() {
        produto.setPreco(2999.99);
        assertEquals(2999.99, produto.getPreco(), 0.01);
    }
    
    @Test
    public void testSetAndGetEstoque() {
        produto.setEstoque(10);
        assertEquals(10, produto.getEstoque());
    }
    
    @Test
    public void testProdutoCompleto() {
        produto.setId(1);
        produto.setNome("Smartphone Samsung");
        produto.setDescricao("Smartphone Samsung Galaxy S21");
        produto.setPreco(3999.99);
        produto.setEstoque(25);
        
        assertEquals(1, produto.getId());
        assertEquals("Smartphone Samsung", produto.getNome());
        assertEquals("Smartphone Samsung Galaxy S21", produto.getDescricao());
        assertEquals(3999.99, produto.getPreco(), 0.01);
        assertEquals(25, produto.getEstoque());
    }
    
    @Test
    public void testProdutoSemDescricao() {
        produto.setId(2);
        produto.setNome("Mouse USB");
        produto.setPreco(29.99);
        produto.setEstoque(50);
        
        assertEquals(2, produto.getId());
        assertEquals("Mouse USB", produto.getNome());
        assertNull(produto.getDescricao());
        assertEquals(29.99, produto.getPreco(), 0.01);
        assertEquals(50, produto.getEstoque());
    }
    
    @Test
    public void testProdutoComPrecoZero() {
        produto.setId(3);
        produto.setNome("Produto Gratuito");
        produto.setDescricao("Produto de demonstração");
        produto.setPreco(0.0);
        produto.setEstoque(100);
        
        assertEquals(3, produto.getId());
        assertEquals("Produto Gratuito", produto.getNome());
        assertEquals("Produto de demonstração", produto.getDescricao());
        assertEquals(0.0, produto.getPreco(), 0.01);
        assertEquals(100, produto.getEstoque());
    }
    
    @Test
    public void testProdutoComEstoqueZero() {
        produto.setId(4);
        produto.setNome("Produto Esgotado");
        produto.setDescricao("Produto temporariamente indisponível");
        produto.setPreco(99.99);
        produto.setEstoque(0);
        
        assertEquals(4, produto.getId());
        assertEquals("Produto Esgotado", produto.getNome());
        assertEquals("Produto temporariamente indisponível", produto.getDescricao());
        assertEquals(99.99, produto.getPreco(), 0.01);
        assertEquals(0, produto.getEstoque());
    }
} 