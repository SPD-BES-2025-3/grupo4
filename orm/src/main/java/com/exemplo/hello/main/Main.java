package com.exemplo.hello.main;

import com.exemplo.hello.model.*;
import com.j256.ormlite.jdbc.JdbcConnectionSource;
import com.j256.ormlite.support.ConnectionSource;
import com.j256.ormlite.table.TableUtils;

public class Main {

    private static final String DATABASE_URL = "jdbc:postgresql://localhost:5432/projetospd";
    private static final String USER = "postgres";
    private static final String PASSWORD = "123456";

    public static void main(String[] args) {
        try (ConnectionSource connectionSource = new JdbcConnectionSource(DATABASE_URL, USER, PASSWORD)) {
            TableUtils.createTableIfNotExists(connectionSource, Endereco.class);
            TableUtils.createTableIfNotExists(connectionSource, ProdutoCRM.class);
            TableUtils.createTableIfNotExists(connectionSource, ClienteCRM.class);
            TableUtils.createTableIfNotExists(connectionSource, Administrador.class);
            TableUtils.createTableIfNotExists(connectionSource, PedidoCRM.class);
        } catch (Exception e) {
            e.printStackTrace();
            return;
        }

        //AdminAppView.launch(AdminAppView.class, args);
    }
}
