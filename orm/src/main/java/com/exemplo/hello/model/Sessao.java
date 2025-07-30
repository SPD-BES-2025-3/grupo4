package com.exemplo.hello.model;

public class Sessao {
    private static ClienteCRM clienteLogado;

    public static void setCliente(ClienteCRM cliente) {
        clienteLogado = cliente;
    }

    public static ClienteCRM getCliente() {
        return clienteLogado;
    }
}