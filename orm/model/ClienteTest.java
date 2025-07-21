package model;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class ClienteTest {

    private Cliente cliente;

    @BeforeEach
    public void setUp() {
        cliente = new Cliente();
        cliente.setNome("Matheus Gonçalves");
        cliente.setEmail("matheusgcv@gmail.com");
        cliente.setTelefone("123456789");
        cliente.setEndereco(new Endereco());
    }

    @AfterEach
    public void tearDown() {
        // limpar dados, se necessário
    }

    @Test
    public void testCriarEDeletarCliente() {
        Cliente clienteSalvo = Repositorios.CLIENTE.create(cliente);
        assertNotNull(clienteSalvo);
        assertTrue(clienteSalvo.getId() > 0, "ID do cliente deve ser gerado");

        int idCliente = clienteSalvo.getId();
        Repositorios.CLIENTE.delete(clienteSalvo);

        Cliente clienteCarregado = Repositorios.CLIENTE.loadFromId(idCliente);
        assertNull(clienteCarregado, "Cliente deve foi deletado corretamente");
    }
}
