package com.exemplo.hello.controller;

import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Parent;
import javafx.scene.control.Tab;

import java.net.URL;
import java.util.ResourceBundle;

public class ClienteAppController implements Initializable {

    @FXML
    private Tab tabClientes;
    @FXML
    private Tab tabProdutos;
    @FXML
    private Tab tabCarrinhos;
    @FXML
    private Tab tabPedidos;
    
    @Override
    public void initialize(URL location, ResourceBundle resources) {
        try {
            Parent clienteContent = FXMLLoader.load(getClass().getResource("/view/Clientes.fxml"));
            tabClientes.setContent(clienteContent);

            Parent produtoContent = FXMLLoader.load(getClass().getResource("/view/Produtos.fxml"));
            tabProdutos.setContent(produtoContent);

            Parent carrinhoContent = FXMLLoader.load(getClass().getResource("/view/Carrinhos.fxml"));
            tabCarrinhos.setContent(carrinhoContent);

            Parent pedidoContent = FXMLLoader.load(getClass().getResource("/view/Pedidos.fxml"));
            tabPedidos.setContent(pedidoContent);

        } catch (Exception e) {
            System.out.println("Erro ao carregar abas:");
            e.printStackTrace();
        }
    }
}
