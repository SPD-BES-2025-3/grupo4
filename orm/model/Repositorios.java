package model;

public class Repositorios {
    public static Database database = new Database("projetospd");

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

    public static final Repositorio<ItemCarrinho, Integer> ITEM_CARRINHO =
        new Repositorio<>(database, ItemCarrinho.class);
        
    public static final Repositorio<Administrador, Integer> ADMINISTRADOR =
        new Repositorio<>(database, Administrador.class);
        
    public static final Repositorio<Envio, Integer> ENVIO =
        new Repositorio<>(database, Envio.class);
        
    public static final Repositorio<Pagamento, Integer> PAGAMENTO =
        new Repositorio<>(database, Pagamento.class);
}
