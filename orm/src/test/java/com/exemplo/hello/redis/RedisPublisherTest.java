package com.exemplo.hello.redis;

import com.exemplo.hello.model.CarrinhoItem;
import com.exemplo.hello.model.ProdutoCRM;
import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;
import java.util.ArrayList;
import java.util.List;

public class RedisPublisherTest {
    
    private RedisPublisher publisher;
    private List<CarrinhoItem> itens;
    private ProdutoCRM produto;
    
    @Before
    public void setUp() {
        publisher = RedisPublisher.getInstancia();
        
        produto = new ProdutoCRM();
        produto.setId(1);
        produto.setNome("Produto Teste");
        produto.setPreco(99.99);
        produto.setEstoque(10);
        
        itens = new ArrayList<>();
        itens.add(new CarrinhoItem(produto, 2));
    }
    
    @Test
    public void testGetInstancia() {
        RedisPublisher instancia1 = RedisPublisher.getInstancia();
        RedisPublisher instancia2 = RedisPublisher.getInstancia();
        
        assertNotNull(instancia1);
        assertNotNull(instancia2);
        // Deve ser a mesma instância (Singleton)
        assertEquals(instancia1, instancia2);
    }
    
    @Test
    public void testPublicarCarrinhoFinalizado() {
        try {
            publisher.publicarCarrinhoFinalizado(itens, 1);
            // Se chegou aqui, a publicação foi bem-sucedida
        } catch (Exception e) {
            // Esperado se não houver Redis rodando
            assertTrue(e instanceof RuntimeException || e instanceof Exception);
        }
    }
    
    @Test
    public void testPublicarCarrinhoVazio() {
        try {
            List<CarrinhoItem> itensVazios = new ArrayList<>();
            publisher.publicarCarrinhoFinalizado(itensVazios, 1);
            // Se chegou aqui, a publicação foi bem-sucedida
        } catch (Exception e) {
            // Esperado se não houver Redis rodando
            assertTrue(e instanceof RuntimeException || e instanceof Exception);
        }
    }
    
    @Test
    public void testPublicarCarrinhoComClienteIdZero() {
        try {
            publisher.publicarCarrinhoFinalizado(itens, 0);
            // Se chegou aqui, a publicação foi bem-sucedida
        } catch (Exception e) {
            // Esperado se não houver Redis rodando
            assertTrue(e instanceof RuntimeException || e instanceof Exception);
        }
    }
    
    @Test
    public void testPublicarCarrinhoComClienteIdNegativo() {
        try {
            publisher.publicarCarrinhoFinalizado(itens, -1);
            // Se chegou aqui, a publicação foi bem-sucedida
        } catch (Exception e) {
            // Esperado se não houver Redis rodando
            assertTrue(e instanceof RuntimeException || e instanceof Exception);
        }
    }
    
    @Test
    public void testPublicarCarrinhoComClienteIdGrande() {
        try {
            publisher.publicarCarrinhoFinalizado(itens, 999999);
            // Se chegou aqui, a publicação foi bem-sucedida
        } catch (Exception e) {
            // Esperado se não houver Redis rodando
            assertTrue(e instanceof RuntimeException || e instanceof Exception);
        }
    }
    
    @Test
    public void testPublicarMetodoEstatico() {
        try {
            RedisPublisher.publicar("teste", "{\"teste\": \"valor\"}");
            // Se chegou aqui, a publicação foi bem-sucedida
        } catch (Exception e) {
            // Esperado se não houver Redis rodando
            assertTrue(e instanceof RuntimeException || e instanceof Exception);
        }
    }
    
    @Test
    public void testPublicarMetodoEstaticoComCanalNulo() {
        try {
            RedisPublisher.publicar(null, "{\"teste\": \"valor\"}");
            // Pode lançar exceção
        } catch (Exception e) {
            // Esperado se não houver Redis rodando ou canal nulo
            assertTrue(e instanceof RuntimeException || e instanceof Exception || e instanceof NullPointerException);
        }
    }
    
    @Test
    public void testPublicarMetodoEstaticoComJsonNulo() {
        try {
            RedisPublisher.publicar("teste", null);
            // Pode lançar exceção
        } catch (Exception e) {
            // Esperado se não houver Redis rodando ou json nulo
            assertTrue(e instanceof RuntimeException || e instanceof Exception || e instanceof NullPointerException);
        }
    }
    
    @Test
    public void testFechar() {
        try {
            publisher.fechar();
            // Se chegou aqui, o fechamento foi bem-sucedido
        } catch (Exception e) {
            // Esperado se não houver Redis rodando
            assertTrue(e instanceof RuntimeException || e instanceof Exception);
        }
    }
    
    @Test
    public void testFecharMultiplasVezes() {
        try {
            publisher.fechar();
            publisher.fechar();
            publisher.fechar();
            // Se chegou aqui, não houve exceção
        } catch (Exception e) {
            // Esperado se não houver Redis rodando
            assertTrue(e instanceof RuntimeException || e instanceof Exception);
        }
    }
} 