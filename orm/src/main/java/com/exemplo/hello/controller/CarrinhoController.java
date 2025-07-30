package com.exemplo.hello.controller;

import com.exemplo.hello.model.*;
import com.exemplo.hello.redis.RedisPublisher;

import javafx.beans.property.SimpleDoubleProperty;
import javafx.beans.property.SimpleIntegerProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.*;

import java.net.URL;
import java.util.ResourceBundle;

public class CarrinhoController implements Initializable {

    @FXML private TableView<CarrinhoItem> tabelaCarrinhos;
    @FXML private TableColumn<CarrinhoItem, Integer> idCol;
    @FXML private TableColumn<CarrinhoItem, String> produtoCol;
    @FXML private TableColumn<CarrinhoItem, Double> precoCol;
    @FXML private TableColumn<CarrinhoItem, Integer> quantidadeCol;
    @FXML private TableColumn<CarrinhoItem, Double> totalCol;

    @FXML private TextField idField;
    @FXML private TextField totalField;

    @FXML private Button adicionarBtn;
    @FXML private Button atualizarBtn;
    @FXML private Button deletarBtn;
    @FXML private Button limparBtn;

    private final ObservableList<CarrinhoItem> itensCarrinho = FXCollections.observableArrayList();

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        idCol.setCellValueFactory(cellData -> new SimpleIntegerProperty(cellData.getValue().getProduto().getId()).asObject());
        produtoCol.setCellValueFactory(cellData -> new SimpleStringProperty(cellData.getValue().getProduto().getNome()));
        precoCol.setCellValueFactory(cellData -> new SimpleDoubleProperty(cellData.getValue().getProduto().getPreco()).asObject());
        quantidadeCol.setCellValueFactory(cellData -> new SimpleIntegerProperty(cellData.getValue().getQuantidade()).asObject());
        totalCol.setCellValueFactory(cellData -> new SimpleDoubleProperty(cellData.getValue().getSubtotal()).asObject());

        tabelaCarrinhos.setItems(itensCarrinho);

        tabelaCarrinhos.getSelectionModel().selectedItemProperty().addListener((obs, antigo, novo) -> {
            if (novo != null) {
                idField.setText(String.valueOf(novo.getProduto().getId()));
                totalField.setText(String.valueOf(novo.getQuantidade()));
                atualizarBtn.setDisable(false);
                deletarBtn.setDisable(false);
            } else {
                atualizarBtn.setDisable(true);
                deletarBtn.setDisable(true);
            }
        });
    }

    public void adicionarProduto(ProdutoCRM produto, int quantidade) {
        for (CarrinhoItem item : itensCarrinho) {
            if (item.getProduto().getId() == produto.getId()) {
                item.setQuantidade(item.getQuantidade() + quantidade);
                tabelaCarrinhos.refresh();
                return;
            }
        }
        itensCarrinho.add(new CarrinhoItem(produto, quantidade));
    }

    @FXML
    public void onAtualizar() {
        CarrinhoItem selecionado = tabelaCarrinhos.getSelectionModel().getSelectedItem();
        if (selecionado != null) {
            int novaQuantidade = Integer.parseInt(totalField.getText());
            if (novaQuantidade <= 0) {
                itensCarrinho.remove(selecionado);
                idField.clear();
                totalField.clear();
            } else if (novaQuantidade > selecionado.getProduto().getEstoque()){
                System.out.println("A quantidade não foi alterada porque não há estoque para a quantidade informada do produto escolhido.");
            } else {
                selecionado.setQuantidade(novaQuantidade);
                System.out.println("A quantidade do produto " + selecionado.getProduto().getNome() + " foi alterada para " + novaQuantidade);
            }
            tabelaCarrinhos.refresh();
        }
    }

    @FXML
    public void onDeletar() {
        CarrinhoItem selecionado = tabelaCarrinhos.getSelectionModel().getSelectedItem();
        if (selecionado != null) {
            itensCarrinho.remove(selecionado);
        }
        idField.clear();
        totalField.clear();
    }

    @FXML
    public void onLimpar() {
        itensCarrinho.clear();
        idField.clear();
        totalField.clear();
    }

    @FXML
    public void onAdicionar() {

    }

    @FXML
    public void onFinalizar() {
        if (itensCarrinho.isEmpty()) {
            System.out.println("Carrinho está vazio.");
            return;
        }

        ClienteCRM cliente = Sessao.getCliente();

        RedisPublisher publisher = RedisPublisher.getInstancia();
        publisher.publicarCarrinhoFinalizado(itensCarrinho, cliente.getId());
        System.out.println("Carrinho finalizado enviado para Redis no canal: carrinho:" + cliente.getId());
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle("Sucesso");
        alert.setHeaderText(null);
        alert.setContentText("Carrinho finalizado com sucesso!");
        alert.showAndWait();
        idField.clear();
        totalField.clear();
        onLimpar();
    }

    private static CarrinhoController instancia;

    public static CarrinhoController getInstancia() {
        return instancia;
    }

    public CarrinhoController() {
        instancia = this;
    }
}
