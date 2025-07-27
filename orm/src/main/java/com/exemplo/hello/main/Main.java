package com.exemplo.hello.main;

import com.j256.ormlite.jdbc.JdbcConnectionSource;
import com.j256.ormlite.support.ConnectionSource;
import com.j256.ormlite.table.TableUtils;

import com.exemplo.hello.model.Endereco;
import com.exemplo.hello.model.Produto;
import com.exemplo.hello.model.Cliente;
import com.exemplo.hello.model.Administrador;
import com.exemplo.hello.model.Categoria;
import com.exemplo.hello.model.Pedido;
import com.exemplo.hello.model.Carrinho;
import com.exemplo.hello.model.ItemCarrinho;
import com.exemplo.hello.model.Envio;
import com.exemplo.hello.model.Pagamento;

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
