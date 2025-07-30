package com.exemplo.hello.model;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class UsuarioTest {
    
    private Usuario usuario;
    private Endereco endereco;
    
    @Before
    public void setUp() {
        usuario = new Usuario();
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
        usuario.setId(1);
        assertEquals(1, usuario.getId());
    }
    
    @Test
    public void testSetAndGetNome() {
        usuario.setNome("João Silva");
        assertEquals("João Silva", usuario.getNome());
    }
    
    @Test
    public void testSetAndGetEmail() {
        usuario.setEmail("joao@teste.com");
        assertEquals("joao@teste.com", usuario.getEmail());
    }
    
    @Test
    public void testSetAndGetSenha() {
        usuario.setSenha("senha123");
        assertEquals("senha123", usuario.getSenha());
    }
    
    @Test
    public void testSetAndGetEndereco() {
        usuario.setEndereco(endereco);
        assertNotNull(usuario.getEndereco());
        assertEquals("Rua Teste", usuario.getEndereco().getRua());
    }
    
    @Test
    public void testUsuarioCompleto() {
        usuario.setId(1);
        usuario.setNome("Maria Santos");
        usuario.setEmail("maria@teste.com");
        usuario.setSenha("senha456");
        usuario.setEndereco(endereco);
        
        assertEquals(1, usuario.getId());
        assertEquals("Maria Santos", usuario.getNome());
        assertEquals("maria@teste.com", usuario.getEmail());
        assertEquals("senha456", usuario.getSenha());
        assertNotNull(usuario.getEndereco());
    }
} 