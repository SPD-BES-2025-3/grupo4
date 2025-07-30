package com.exemplo.hello.model;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class EnderecoTest {
    
    private Endereco endereco;
    
    @Before
    public void setUp() {
        endereco = new Endereco();
    }
    
    @Test
    public void testSetAndGetId() {
        endereco.setId(1);
        assertEquals(1, endereco.getId());
    }
    
    @Test
    public void testSetAndGetRua() {
        endereco.setRua("Rua das Flores");
        assertEquals("Rua das Flores", endereco.getRua());
    }
    
    @Test
    public void testSetAndGetNumero() {
        endereco.setNumero("456");
        assertEquals("456", endereco.getNumero());
    }
    
    @Test
    public void testSetAndGetBairro() {
        endereco.setBairro("Setor Bueno");
        assertEquals("Setor Bueno", endereco.getBairro());
    }
    
    @Test
    public void testSetAndGetCidade() {
        endereco.setCidade("Goiânia");
        assertEquals("Goiânia", endereco.getCidade());
    }
    
    @Test
    public void testSetAndGetEstado() {
        endereco.setEstado("GO");
        assertEquals("GO", endereco.getEstado());
    }
    
    @Test
    public void testSetAndGetCep() {
        endereco.setCep("74230-120");
        assertEquals("74230-120", endereco.getCep());
    }
    
    @Test
    public void testSetAndGetComplemento() {
        endereco.setComplemento("Apto 101");
        assertEquals("Apto 101", endereco.getComplemento());
    }
    
    @Test
    public void testEnderecoCompleto() {
        endereco.setId(1);
        endereco.setRua("Avenida Principal");
        endereco.setNumero("789");
        endereco.setBairro("Centro");
        endereco.setCidade("Goiânia");
        endereco.setEstado("GO");
        endereco.setCep("74000-000");
        endereco.setComplemento("Sala 205");
        
        assertEquals(1, endereco.getId());
        assertEquals("Avenida Principal", endereco.getRua());
        assertEquals("789", endereco.getNumero());
        assertEquals("Centro", endereco.getBairro());
        assertEquals("Goiânia", endereco.getCidade());
        assertEquals("GO", endereco.getEstado());
        assertEquals("74000-000", endereco.getCep());
        assertEquals("Sala 205", endereco.getComplemento());
    }
    
    @Test
    public void testEnderecoSemComplemento() {
        endereco.setId(2);
        endereco.setRua("Rua Secundária");
        endereco.setNumero("321");
        endereco.setBairro("Setor Sul");
        endereco.setCidade("Goiânia");
        endereco.setEstado("GO");
        endereco.setCep("74100-000");
        
        assertEquals(2, endereco.getId());
        assertEquals("Rua Secundária", endereco.getRua());
        assertEquals("321", endereco.getNumero());
        assertEquals("Setor Sul", endereco.getBairro());
        assertEquals("Goiânia", endereco.getCidade());
        assertEquals("GO", endereco.getEstado());
        assertEquals("74100-000", endereco.getCep());
        assertNull(endereco.getComplemento());
    }
} 