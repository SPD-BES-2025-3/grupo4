package com.exemplo.hello.model;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;
import java.util.Date;

public class PedidoCRMTest {
    
    private PedidoCRM pedido;
    private ClienteCRM cliente;
    private Date data;
    
    @Before
    public void setUp() {
        pedido = new PedidoCRM();
        cliente = new ClienteCRM();
        cliente.setId(1);
        cliente.setNome("João Silva");
        cliente.setEmail("joao@teste.com");
        data = new Date();
    }
    
    @Test
    public void testSetAndGetId() {
        pedido.setId(1);
        assertEquals(1, pedido.getId());
    }
    
    @Test
    public void testSetAndGetData() {
        pedido.setData(data);
        assertEquals(data, pedido.getData());
    }
    
    @Test
    public void testSetAndGetStatus() {
        pedido.setStatus("Pendente");
        assertEquals("Pendente", pedido.getStatus());
    }
    
    @Test
    public void testSetAndGetTotal() {
        pedido.setTotal(299.99);
        assertEquals(299.99, pedido.getTotal(), 0.01);
    }
    
    @Test
    public void testSetAndGetCliente() {
        pedido.setCliente(cliente);
        assertNotNull(pedido.getCliente());
        assertEquals(1, pedido.getCliente().getId());
        assertEquals("João Silva", pedido.getCliente().getNome());
    }
    
    @Test
    public void testPedidoCompleto() {
        pedido.setId(1);
        pedido.setData(data);
        pedido.setStatus("Aprovado");
        pedido.setTotal(599.99);
        pedido.setCliente(cliente);
        
        assertEquals(1, pedido.getId());
        assertEquals(data, pedido.getData());
        assertEquals("Aprovado", pedido.getStatus());
        assertEquals(599.99, pedido.getTotal(), 0.01);
        assertNotNull(pedido.getCliente());
        assertEquals("João Silva", pedido.getCliente().getNome());
    }
    
    @Test
    public void testPedidoComStatusCancelado() {
        pedido.setId(2);
        pedido.setData(data);
        pedido.setStatus("Cancelado");
        pedido.setTotal(0.0);
        pedido.setCliente(cliente);
        
        assertEquals(2, pedido.getId());
        assertEquals(data, pedido.getData());
        assertEquals("Cancelado", pedido.getStatus());
        assertEquals(0.0, pedido.getTotal(), 0.01);
        assertNotNull(pedido.getCliente());
    }
    
    @Test
    public void testPedidoComStatusEmProcessamento() {
        pedido.setId(3);
        pedido.setData(data);
        pedido.setStatus("Em Processamento");
        pedido.setTotal(899.99);
        pedido.setCliente(cliente);
        
        assertEquals(3, pedido.getId());
        assertEquals(data, pedido.getData());
        assertEquals("Em Processamento", pedido.getStatus());
        assertEquals(899.99, pedido.getTotal(), 0.01);
        assertNotNull(pedido.getCliente());
    }
    
    @Test
    public void testPedidoComTotalZero() {
        pedido.setId(4);
        pedido.setData(data);
        pedido.setStatus("Pendente");
        pedido.setTotal(0.0);
        pedido.setCliente(cliente);
        
        assertEquals(4, pedido.getId());
        assertEquals(data, pedido.getData());
        assertEquals("Pendente", pedido.getStatus());
        assertEquals(0.0, pedido.getTotal(), 0.01);
        assertNotNull(pedido.getCliente());
    }
} 