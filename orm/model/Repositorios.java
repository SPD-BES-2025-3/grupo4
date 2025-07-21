package model;

public class Repositorios {
    public static Database database = new Database("app.sqlite");

    public static final Repositorio<Produto, Integer> PRODUTO =
        new Repositorio<>(database, Produto.class);

    public static final Repositorio<Categoria, Integer> CATEGORIA =
        new Repositorio<>(database, Categoria.class);

    public static final Repositorio<Pedido, Integer> PEDIDO =
        new Repositorio<>(database, Pedido.class);

    public static final Repositorio<Cliente, Integer> CLIENTE =
        new Repositorio<>(database, Cliente.class);

    public static final Repositorio<Endereco, Integer> ENDERECO =
        new Repositorio<>(database, Endereco.class);

    public static final Repositorio<ItemPedido, Integer> ITEM_PEDIDO =
        new Repositorio<>(database, ItemPedido.class);
}
