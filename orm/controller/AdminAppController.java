package controller;

import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Parent;
import javafx.scene.control.Tab;

import java.net.URL;
import java.util.ResourceBundle;

public class AdminAppController implements Initializable {

    @FXML
    private Tab tabClientes;
    @FXML
    private Tab tabPedidos;
    @FXML
    private Tab tabCategorias;
    @FXML
    private Tab tabProdutos;

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        try {
            Parent clienteContent = FXMLLoader.load(getClass().getResource("/view/ClientesCadastrados.fxml"));
            tabClientes.setContent(clienteContent);

            Parent pedidoContent = FXMLLoader.load(getClass().getResource("/view/PedidosCadastrados.fxml"));
            tabPedidos.setContent(pedidoContent);

            Parent categoriaContent = FXMLLoader.load(getClass().getResource("/view/CategoriasCadastradas.fxml"));
            tabCategorias.setContent(categoriaContent);

            Parent produtoContent = FXMLLoader.load(getClass().getResource("/view/ProdutosCadastrados.fxml"));
            tabProdutos.setContent(produtoContent);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
