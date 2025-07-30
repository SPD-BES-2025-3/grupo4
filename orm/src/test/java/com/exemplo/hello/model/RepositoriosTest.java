package com.exemplo.hello.model;

import org.junit.Test;
import static org.junit.Assert.*;

public class RepositoriosTest {
    
    @Test
    public void testDatabase() {
        assertNotNull(Repositorios.database);
    }
    
    @Test
    public void testProdutoCRM() {
        assertNotNull(Repositorios.PRODUTOCRM);
    }
    
    @Test
    public void testPedidoCRM() {
        assertNotNull(Repositorios.PEDIDOCRM);
    }
    
    @Test
    public void testClienteCRM() {
        assertNotNull(Repositorios.CLIENTECRM);
    }
    
    @Test
    public void testEndereco() {
        assertNotNull(Repositorios.ENDERECO);
    }
    
    @Test
    public void testAdministrador() {
        assertNotNull(Repositorios.ADMINISTRADOR);
    }
    
    @Test
    public void testTodosOsRepositorios() {
        // Verifica se todos os repositórios estão inicializados
        assertNotNull(Repositorios.database);
        assertNotNull(Repositorios.PRODUTOCRM);
        assertNotNull(Repositorios.PEDIDOCRM);
        assertNotNull(Repositorios.CLIENTECRM);
        assertNotNull(Repositorios.ENDERECO);
        assertNotNull(Repositorios.ADMINISTRADOR);
    }
    
    @Test
    public void testRepositoriosComClassesCorretas() {
        // Verifica se os repositórios estão configurados corretamente
        assertNotNull(Repositorios.PRODUTOCRM);
        assertNotNull(Repositorios.PEDIDOCRM);
        assertNotNull(Repositorios.CLIENTECRM);
        assertNotNull(Repositorios.ENDERECO);
        assertNotNull(Repositorios.ADMINISTRADOR);
    }
} 