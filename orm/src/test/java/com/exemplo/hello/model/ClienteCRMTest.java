package com.exemplo.hello.model;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class ClienteCRMTest {
    
    private ClienteCRM cliente;
    private Endereco endereco;
    
    @Before
    public void setUp() {
        cliente = new ClienteCRM();
        endereco = new Endereco();
        endereco.setRua("Rua Teste");
        endereco.setNumero("123");
        endereco.setBairro("Centro");
        endereco.setCidade("Goiânia");
        endereco.setEstado("GO");
        endereco.setCep("74000-000");
    }
    
    @Test
    public void testSetAndGetId() {
        cliente.setId(1);
        assertEquals(1, cliente.getId());
    }
    
    @Test
    public void testSetAndGetNome() {
        cliente.setNome("João Silva");
        assertEquals("João Silva", cliente.getNome());
    }
    
    @Test
    public void testSetAndGetEmail() {
        cliente.setEmail("joao@teste.com");
        assertEquals("joao@teste.com", cliente.getEmail());
    }
    
    @Test
    public void testSetAndGetSenha() {
        cliente.setSenha("senha123");
        assertEquals("senha123", cliente.getSenha());
    }
    
    @Test
    public void testSetAndGetEndereco() {
        cliente.setEndereco(endereco);
        assertNotNull(cliente.getEndereco());
        assertEquals("Rua Teste", cliente.getEndereco().getRua());
    }
    
    @Test
    public void testSetAndGetNumeroTelefone() {
        cliente.setNumeroTelefone("(62) 99999-9999");
        assertEquals("(62) 99999-9999", cliente.getNumeroTelefone());
    }
    
    @Test
    public void testClienteCompleto() {
        cliente.setId(1);
        cliente.setNome("Maria Santos");
        cliente.setEmail("maria@teste.com");
        cliente.setSenha("senha456");
        cliente.setEndereco(endereco);
        cliente.setNumeroTelefone("(62) 88888-8888");
        
        assertEquals(1, cliente.getId());
        assertEquals("Maria Santos", cliente.getNome());
        assertEquals("maria@teste.com", cliente.getEmail());
        assertEquals("senha456", cliente.getSenha());
        assertNotNull(cliente.getEndereco());
        assertEquals("(62) 88888-8888", cliente.getNumeroTelefone());
    }
    
    @Test
    public void testClienteSemEndereco() {
        cliente.setId(2);
        cliente.setNome("Pedro Costa");
        cliente.setEmail("pedro@teste.com");
        cliente.setSenha("senha789");
        cliente.setNumeroTelefone("(62) 77777-7777");
        
        assertEquals(2, cliente.getId());
        assertEquals("Pedro Costa", cliente.getNome());
        assertEquals("pedro@teste.com", cliente.getEmail());
        assertEquals("senha789", cliente.getSenha());
        assertNull(cliente.getEndereco());
        assertEquals("(62) 77777-7777", cliente.getNumeroTelefone());
    }
} 