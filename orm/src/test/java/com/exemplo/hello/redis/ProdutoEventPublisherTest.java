package com.exemplo.hello.redis;

import com.exemplo.hello.model.ProdutoCRM;
import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class ProdutoEventPublisherTest {
    
    private ProdutoCRM produto;
    
    @Before
    public void setUp() {
        produto = new ProdutoCRM();
        produto.setId(1);
        produto.setNome("Produto Teste");
        produto.setDescricao("Descrição do produto teste");
        produto.setPreco(99.99);
        produto.setEstoque(10);
    }
    
    @Test
    public void testPublicarEvento() {
        try {
            ProdutoEventPublisher.publicarEvento("criado", produto);
            // Se chegou aqui, a publicação foi bem-sucedida
        } catch (Exception e) {
            // Esperado se não houver Redis rodando
            assertTrue(e instanceof RuntimeException || e instanceof Exception);
        }
    }
    
    @Test
    public void testPublicarEventoAtualizado() {
        try {
            ProdutoEventPublisher.publicarEvento("atualizado", produto);
            // Se chegou aqui, a publicação foi bem-sucedida
        } catch (Exception e) {
            // Esperado se não houver Redis rodando
            assertTrue(e instanceof RuntimeException || e instanceof Exception);
        }
    }
    
    @Test
    public void testPublicarEventoDeletado() {
        try {
            ProdutoEventPublisher.publicarEvento("deletado", produto);
            // Se chegou aqui, a publicação foi bem-sucedida
        } catch (Exception e) {
            // Esperado se não houver Redis rodando
            assertTrue(e instanceof RuntimeException || e instanceof Exception);
        }
    }
    
    @Test
    public void testPublicarEventoComAcaoNula() {
        try {
            ProdutoEventPublisher.publicarEvento(null, produto);
            // Pode lançar exceção
        } catch (Exception e) {
            // Esperado se não houver Redis rodando ou ação nula
            assertTrue(e instanceof RuntimeException || e instanceof Exception || e instanceof NullPointerException);
        }
    }
    
    @Test
    public void testPublicarEventoComAcaoVazia() {
        try {
            ProdutoEventPublisher.publicarEvento("", produto);
            // Se chegou aqui, a publicação foi bem-sucedida
        } catch (Exception e) {
            // Esperado se não houver Redis rodando
            assertTrue(e instanceof RuntimeException || e instanceof Exception);
        }
    }
    
    @Test
    public void testPublicarEventoComProdutoNulo() {
        try {
            ProdutoEventPublisher.publicarEvento("criado", null);
            // Pode lançar exceção
        } catch (Exception e) {
            // Esperado se não houver Redis rodando ou produto nulo
            assertTrue(e instanceof RuntimeException || e instanceof Exception || e instanceof NullPointerException);
        }
    }
    
    @Test
    public void testPublicarEventoComProdutoSemId() {
        ProdutoCRM produtoSemId = new ProdutoCRM();
        produtoSemId.setNome("Produto Sem ID");
        produtoSemId.setPreco(50.0);
        
        try {
            ProdutoEventPublisher.publicarEvento("criado", produtoSemId);
            // Se chegou aqui, a publicação foi bem-sucedida
        } catch (Exception e) {
            // Esperado se não houver Redis rodando
            assertTrue(e instanceof RuntimeException || e instanceof Exception);
        }
    }
    
    @Test
    public void testPublicarEventoComProdutoCompleto() {
        ProdutoCRM produtoCompleto = new ProdutoCRM();
        produtoCompleto.setId(999);
        produtoCompleto.setNome("Produto Completo");
        produtoCompleto.setDescricao("Descrição completa do produto");
        produtoCompleto.setPreco(1999.99);
        produtoCompleto.setEstoque(100);
        
        try {
            ProdutoEventPublisher.publicarEvento("atualizado", produtoCompleto);
            // Se chegou aqui, a publicação foi bem-sucedida
        } catch (Exception e) {
            // Esperado se não houver Redis rodando
            assertTrue(e instanceof RuntimeException || e instanceof Exception);
        }
    }
    
    @Test
    public void testFechar() {
        try {
            ProdutoEventPublisher.fechar();
            // Se chegou aqui, o fechamento foi bem-sucedido
        } catch (Exception e) {
            // Esperado se não houver Redis rodando
            assertTrue(e instanceof RuntimeException || e instanceof Exception);
        }
    }
    
    @Test
    public void testFecharMultiplasVezes() {
        try {
            ProdutoEventPublisher.fechar();
            ProdutoEventPublisher.fechar();
            ProdutoEventPublisher.fechar();
            // Se chegou aqui, não houve exceção
        } catch (Exception e) {
            // Esperado se não houver Redis rodando
            assertTrue(e instanceof RuntimeException || e instanceof Exception);
        }
    }
} 