package com.exemplo.hello.model;

public class Repositorios {
    public static Database database = new Database("projetospd");

    public static final Repositorio<ProdutoCRM, Integer> PRODUTOCRM =
        new Repositorio<>(database, ProdutoCRM.class);

    public static final Repositorio<PedidoCRM, Integer> PEDIDOCRM =
        new Repositorio<>(database, PedidoCRM.class);

    public static final Repositorio<ClienteCRM, Integer> CLIENTECRM =
        new Repositorio<>(database, ClienteCRM.class);

    public static final Repositorio<Endereco, Integer> ENDERECO =
        new Repositorio<>(database, Endereco.class);
      
    public static final Repositorio<Administrador, Integer> ADMINISTRADOR =
        new Repositorio<>(database, Administrador.class);
}
