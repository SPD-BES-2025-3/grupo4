package com.exemplo.hello.model;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class SessaoTest {
    
    private ClienteCRM cliente;
    
    @Before
    public void setUp() {
        cliente = new ClienteCRM();
        cliente.setId(1);
        cliente.setNome("João Silva");
        cliente.setEmail("joao@teste.com");
        cliente.setSenha("senha123");
    }
    
    @Test
    public void testSetCliente() {
        Sessao.setCliente(cliente);
        ClienteCRM clienteSessao = Sessao.getCliente();
        assertNotNull(clienteSessao);
        assertEquals(cliente, clienteSessao);
    }
    
    @Test
    public void testGetCliente() {
        Sessao.setCliente(cliente);
        ClienteCRM clienteSessao = Sessao.getCliente();
        
        assertNotNull(clienteSessao);
        assertEquals(1, clienteSessao.getId());
        assertEquals("João Silva", clienteSessao.getNome());
        assertEquals("joao@teste.com", clienteSessao.getEmail());
        assertEquals("senha123", clienteSessao.getSenha());
    }
    
    @Test
    public void testGetClienteSemClienteDefinido() {
        // Limpar a sessão antes do teste
        Sessao.setCliente(null);
        
        ClienteCRM clienteSessao = Sessao.getCliente();
        assertNull(clienteSessao);
    }
    
    @Test
    public void testAlterarClienteNaSessao() {
        Sessao.setCliente(cliente);
        
        ClienteCRM novoCliente = new ClienteCRM();
        novoCliente.setId(2);
        novoCliente.setNome("Maria Santos");
        novoCliente.setEmail("maria@teste.com");
        novoCliente.setSenha("senha456");
        
        Sessao.setCliente(novoCliente);
        
        ClienteCRM clienteSessao = Sessao.getCliente();
        assertNotNull(clienteSessao);
        assertEquals(novoCliente, clienteSessao);
        assertEquals(2, clienteSessao.getId());
        assertEquals("Maria Santos", clienteSessao.getNome());
        assertEquals("maria@teste.com", clienteSessao.getEmail());
    }
    
    @Test
    public void testSessaoComClienteCompleto() {
        Endereco endereco = new Endereco();
        endereco.setRua("Rua Teste");
        endereco.setNumero("123");
        endereco.setBairro("Centro");
        endereco.setCidade("Goiânia");
        endereco.setEstado("GO");
        endereco.setCep("74000-000");
        
        cliente.setEndereco(endereco);
        cliente.setNumeroTelefone("(62) 99999-9999");
        
        Sessao.setCliente(cliente);
        ClienteCRM clienteSessao = Sessao.getCliente();
        
        assertNotNull(clienteSessao);
        assertEquals(1, clienteSessao.getId());
        assertEquals("João Silva", clienteSessao.getNome());
        assertEquals("joao@teste.com", clienteSessao.getEmail());
        assertEquals("senha123", clienteSessao.getSenha());
        assertNotNull(clienteSessao.getEndereco());
        assertEquals("Rua Teste", clienteSessao.getEndereco().getRua());
        assertEquals("(62) 99999-9999", clienteSessao.getNumeroTelefone());
    }
} 