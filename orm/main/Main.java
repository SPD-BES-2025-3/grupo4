package main;

import com.j256.ormlite.jdbc.JdbcConnectionSource;
import com.j256.ormlite.support.ConnectionSource;
import com.j256.ormlite.table.TableUtils;

import model.Usuario;
import model.Endereco;
import model.Produto;
import model.Cliente;
import model.Administrador;
import model.Categoria;
import model.Pedido;
import model.Carrinho;
import model.ItemCarrinho;
import model.Envio;
import model.Pagamento;

import view.AdminAppView;

public class Main {

    private static final String DATABASE_URL = "jdbc:postgresql://localhost:5432/projetospd";
    private static final String USER = "postgres";
    private static final String PASSWORD = "123456";

    public static void main(String[] args) {
        try (ConnectionSource connectionSource = new JdbcConnectionSource(DATABASE_URL, USER, PASSWORD)) {
            TableUtils.createTableIfNotExists(connectionSource, Endereco.class);
            TableUtils.createTableIfNotExists(connectionSource, Produto.class);
            TableUtils.createTableIfNotExists(connectionSource, Cliente.class);
            TableUtils.createTableIfNotExists(connectionSource, Administrador.class);
            TableUtils.createTableIfNotExists(connectionSource, Categoria.class);
            TableUtils.createTableIfNotExists(connectionSource, Pedido.class);
            TableUtils.createTableIfNotExists(connectionSource, Carrinho.class);
            TableUtils.createTableIfNotExists(connectionSource, ItemCarrinho.class);
            TableUtils.createTableIfNotExists(connectionSource, Envio.class);
            TableUtils.createTableIfNotExists(connectionSource, Pagamento.class);
        } catch (Exception e) {
            e.printStackTrace();
            return;
        }

        //AdminAppView.launch(AdminAppView.class, args);
    }
}
