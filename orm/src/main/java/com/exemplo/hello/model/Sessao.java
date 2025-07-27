package com.exemplo.hello.model;

public class Sessao {
    private static Cliente clienteLogado;

    public static void setCliente(Cliente cliente) {
        clienteLogado = cliente;
    }

    public static Cliente getCliente() {
        return clienteLogado;
    }
}