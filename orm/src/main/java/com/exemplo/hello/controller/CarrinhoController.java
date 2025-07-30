    package com.exemplo.hello.controller;

    import com.exemplo.hello.model.*;
    import javafx.collections.FXCollections;
    import javafx.collections.ObservableList;
    import javafx.fxml.FXML;
    import javafx.fxml.Initializable;
    import javafx.scene.control.*;

    import java.net.URL;
    import java.util.ResourceBundle;

    public class CarrinhoController implements Initializable {

        @FXML private TableView<CarrinhoItem> tabelaCarrinhos;
        @FXML private TableColumn<CarrinhoItem, String> idCol;
        @FXML private TableColumn<CarrinhoItem, String> totalCol;

        @FXML private TextField idField;
        @FXML private TextField totalField;

        @FXML private Button adicionarBtn;
        @FXML private Button atualizarBtn;
        @FXML private Button deletarBtn;
        @FXML private Button limparBtn;

        private final ObservableList<CarrinhoItem> itensCarrinho = FXCollections.observableArrayList();

        @Override
        public void initialize(URL location, ResourceBundle resources) {
            idCol.setCellValueFactory(cellData -> new javafx.beans.property.SimpleStringProperty(
                    String.valueOf(cellData.getValue().getProduto().getId())));
            totalCol.setCellValueFactory(cellData -> new javafx.beans.property.SimpleStringProperty(
                    String.format("R$ %.2f", cellData.getValue().getSubtotal())));

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
                } else {
                    selecionado.setQuantidade(novaQuantidade);
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
        }

        @FXML
        public void onLimpar() {
            itensCarrinho.clear();
        }

        @FXML
        public void onAdicionar() {

        }

        private static CarrinhoController instancia;

        public static CarrinhoController getInstancia() {
            return instancia;
        }

        public CarrinhoController() {
            instancia = this;
        }
    }
