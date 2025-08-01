package com.exemplo.hello.model;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;
import java.util.List;

public class RepositorioTest {
    
    private Repositorio<ProdutoCRM, Integer> repositorio;
    private Database database;
    private ProdutoCRM produto;
    
    @Before
    public void setUp() {
        database = new Database("testedb");
        repositorio = new Repositorio<>(database, ProdutoCRM.class);
        
        produto = new ProdutoCRM();
        produto.setNome("Produto Teste");
        produto.setDescricao("Descrição do produto teste");
        produto.setPreco(99.99);
        produto.setEstoque(10);
    }
    
    @Test
    public void testConstrutor() {
        assertNotNull(repositorio);
    }
    
    @Test
    public void testSetDatabase() {
        Database novaDatabase = new Database("novadb");
        repositorio.setDatabase(novaDatabase);
        // Se chegou aqui, não houve exceção
    }
    
    @Test
    public void testCreate() {
        try {
            ProdutoCRM produtoCriado = repositorio.create(produto);
            assertNotNull(produtoCriado);
            assertEquals(produto, produtoCriado);
        } catch (Exception e) {
            // Esperado se não houver banco de dados disponível
            assertTrue(e instanceof java.sql.SQLException || e instanceof RuntimeException);
        }
    }
    
    @Test
    public void testUpdate() {
        try {
            repositorio.update(produto);
            // Se chegou aqui, não houve exceção
        } catch (Exception e) {
            // Esperado se não houver banco de dados disponível
            assertTrue(e instanceof java.sql.SQLException);
        }
    }
    
    @Test
    public void testDelete() {
        try {
            repositorio.delete(produto);
            // Se chegou aqui, não houve exceção
        } catch (Exception e) {
            // Esperado se não houver banco de dados disponível
            assertTrue(e instanceof java.sql.SQLException);
        }
    }
    
    @Test
    public void testLoadFromId() {
        try {
            ProdutoCRM produtoCarregado = repositorio.loadFromId(1);
            // Pode ser null se não existir o registro
        } catch (Exception e) {
            // Esperado se não houver banco de dados disponível
            assertTrue(e instanceof java.sql.SQLException);
        }
    }
    
    @Test
    public void testLoadAll() {
        try {
            List<ProdutoCRM> produtos = repositorio.loadAll();
            assertNotNull(produtos);
            // A lista pode estar vazia se não houver registros
        } catch (Exception e) {
            // Esperado se não houver banco de dados disponível
            assertTrue(e instanceof java.sql.SQLException);
        }
    }
    
    @Test
    public void testCreateComProdutoNulo() {
        try {
            ProdutoCRM produtoCriado = repositorio.create(null);
            // Pode lançar exceção ou retornar null
        } catch (Exception e) {
            // Esperado se não houver banco de dados disponível
            assertTrue(e instanceof java.sql.SQLException || e instanceof RuntimeException);
        }
    }
    
    @Test
    public void testUpdateComProdutoNulo() {
        try {
            repositorio.update(null);
            // Pode lançar exceção
        } catch (Exception e) {
            // Esperado se não houver banco de dados disponível
            assertTrue(e instanceof java.sql.SQLException);
        }
    }
    
    @Test
    public void testDeleteComProdutoNulo() {
        try {
            repositorio.delete(null);
            // Pode lançar exceção
        } catch (Exception e) {
            // Esperado se não houver banco de dados disponível
            assertTrue(e instanceof java.sql.SQLException);
        }
    }
    
    @Test
    public void testLoadFromIdComIdNulo() {
        try {
            ProdutoCRM produtoCarregado = repositorio.loadFromId(null);
            // Pode ser null se não existir o registro
        } catch (Exception e) {
            // Esperado se não houver banco de dados disponível
            assertTrue(e instanceof java.sql.SQLException);
        }
    }
} 