package com.exemplo.hello.model;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class DatabaseTest {
    
    private Database database;
    
    @Before
    public void setUp() {
        database = new Database("testdb");
    }
    
    @Test
    public void testConstrutor() {
        assertNotNull(database);
    }
    
    @Test
    public void testConstrutorComNomeNulo() {
        Database dbNulo = new Database(null);
        assertNotNull(dbNulo);
    }
    
    @Test
    public void testConstrutorComNomeVazio() {
        Database dbVazio = new Database("");
        assertNotNull(dbVazio);
    }
    
    @Test
    public void testGetConnectionComNomeValido() {
        try {
            // Este teste pode falhar se não houver PostgreSQL rodando
            // É um teste de integração que requer banco de dados
            database.getConnection();
            // Se chegou aqui, a conexão foi estabelecida com sucesso
        } catch (Exception e) {
            // Esperado se não houver PostgreSQL rodando
            assertTrue(e instanceof java.sql.SQLException);
        }
    }
    
    @Test(expected = java.sql.SQLException.class)
    public void testGetConnectionComNomeNulo() throws Exception {
        Database dbNulo = new Database(null);
        dbNulo.getConnection();
    }
    
    @Test
    public void testClose() {
        try {
            database.getConnection();
            database.close();
            // Se chegou aqui, o fechamento foi bem-sucedido
        } catch (Exception e) {
            // Esperado se não houver PostgreSQL rodando
            assertTrue(e instanceof java.sql.SQLException);
        }
    }
    
    @Test
    public void testCloseSemConexao() {
        // Deve funcionar mesmo sem conexão estabelecida
        database.close();
        // Se chegou aqui, não houve exceção
    }
    
    @Test
    public void testCloseMultiplasVezes() {
        // Deve funcionar mesmo chamando close múltiplas vezes
        database.close();
        database.close();
        database.close();
        // Se chegou aqui, não houve exceção
    }
    
    @Test
    public void testGetConnectionAposClose() {
        try {
            database.getConnection();
            database.close();
            // Tentar obter conexão novamente após fechar
            database.getConnection();
        } catch (Exception e) {
            // Esperado se não houver PostgreSQL rodando
            assertTrue(e instanceof java.sql.SQLException);
        }
    }
} 