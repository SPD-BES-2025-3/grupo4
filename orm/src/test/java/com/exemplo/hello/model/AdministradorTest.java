package com.exemplo.hello.model;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class AdministradorTest {
    
    private Administrador administrador;
    private Endereco endereco;
    
    @Before
    public void setUp() {
        administrador = new Administrador();
        endereco = new Endereco();
        endereco.setRua("Rua Admin");
        endereco.setNumero("456");
        endereco.setBairro("Setor Central");
        endereco.setCidade("Goiânia");
        endereco.setEstado("GO");
        endereco.setCep("74000-000");
    }
    
    @Test
    public void testSetAndGetId() {
        administrador.setId(1);
        assertEquals(1, administrador.getId());
    }
    
    @Test
    public void testSetAndGetNome() {
        administrador.setNome("Admin Silva");
        assertEquals("Admin Silva", administrador.getNome());
    }
    
    @Test
    public void testSetAndGetEmail() {
        administrador.setEmail("admin@teste.com");
        assertEquals("admin@teste.com", administrador.getEmail());
    }
    
    @Test
    public void testSetAndGetSenha() {
        administrador.setSenha("admin123");
        assertEquals("admin123", administrador.getSenha());
    }
    
    @Test
    public void testSetAndGetEndereco() {
        administrador.setEndereco(endereco);
        assertNotNull(administrador.getEndereco());
        assertEquals("Rua Admin", administrador.getEndereco().getRua());
    }
    
    @Test
    public void testAdministradorCompleto() {
        administrador.setId(1);
        administrador.setNome("Administrador Principal");
        administrador.setEmail("admin@empresa.com");
        administrador.setSenha("senhaAdmin456");
        administrador.setEndereco(endereco);
        
        assertEquals(1, administrador.getId());
        assertEquals("Administrador Principal", administrador.getNome());
        assertEquals("admin@empresa.com", administrador.getEmail());
        assertEquals("senhaAdmin456", administrador.getSenha());
        assertNotNull(administrador.getEndereco());
    }
    
    @Test
    public void testAdministradorSemEndereco() {
        administrador.setId(2);
        administrador.setNome("Admin Secundário");
        administrador.setEmail("admin2@empresa.com");
        administrador.setSenha("senhaAdmin789");
        
        assertEquals(2, administrador.getId());
        assertEquals("Admin Secundário", administrador.getNome());
        assertEquals("admin2@empresa.com", administrador.getEmail());
        assertEquals("senhaAdmin789", administrador.getSenha());
        assertNull(administrador.getEndereco());
    }
} 