package com.exemplo.hello.model;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class CarrinhoItemTest {
    
    private CarrinhoItem carrinhoItem;
    private ProdutoCRM produto;
    
    @Before
    public void setUp() {
        produto = new ProdutoCRM();
        produto.setId(1);
        produto.setNome("Notebook Dell");
        produto.setPreco(2999.99);
        produto.setEstoque(10);
        
        carrinhoItem = new CarrinhoItem(produto, 2);
    }
    
    @Test
    public void testConstrutor() {
        assertNotNull(carrinhoItem);
        assertEquals(produto, carrinhoItem.getProduto());
        assertEquals(2, carrinhoItem.getQuantidade());
    }
    
    @Test
    public void testGetProduto() {
        assertEquals(produto, carrinhoItem.getProduto());
        assertEquals("Notebook Dell", carrinhoItem.getProduto().getNome());
        assertEquals(2999.99, carrinhoItem.getProduto().getPreco(), 0.01);
    }
    
    @Test
    public void testGetQuantidade() {
        assertEquals(2, carrinhoItem.getQuantidade());
    }
    
    @Test
    public void testSetQuantidade() {
        carrinhoItem.setQuantidade(5);
        assertEquals(5, carrinhoItem.getQuantidade());
    }
    
    @Test
    public void testGetSubtotal() {
        assertEquals(5999.98, carrinhoItem.getSubtotal(), 0.01);
    }
    
    @Test
    public void testGetSubtotalComQuantidadeUm() {
        CarrinhoItem item = new CarrinhoItem(produto, 1);
        assertEquals(2999.99, item.getSubtotal(), 0.01);
    }
    
    @Test
    public void testGetSubtotalComQuantidadeZero() {
        CarrinhoItem item = new CarrinhoItem(produto, 0);
        assertEquals(0.0, item.getSubtotal(), 0.01);
    }
    
    @Test
    public void testGetSubtotalComQuantidadeAlterada() {
        carrinhoItem.setQuantidade(3);
        assertEquals(8999.97, carrinhoItem.getSubtotal(), 0.01);
    }
    
    @Test
    public void testCarrinhoItemComProdutoBarato() {
        ProdutoCRM produtoBarato = new ProdutoCRM();
        produtoBarato.setId(2);
        produtoBarato.setNome("Mouse USB");
        produtoBarato.setPreco(29.99);
        produtoBarato.setEstoque(50);
        
        CarrinhoItem item = new CarrinhoItem(produtoBarato, 10);
        
        assertEquals(produtoBarato, item.getProduto());
        assertEquals(10, item.getQuantidade());
        assertEquals(299.90, item.getSubtotal(), 0.01);
    }
    
    @Test
    public void testCarrinhoItemComQuantidadeNegativa() {
        CarrinhoItem item = new CarrinhoItem(produto, -1);
        assertEquals(-1, item.getQuantidade());
        assertEquals(-2999.99, item.getSubtotal(), 0.01);
    }
} 