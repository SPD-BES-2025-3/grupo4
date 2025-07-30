package com.exemplo.hello.controller;

import com.exemplo.hello.view.ProdutosView;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import com.exemplo.hello.model.Repositorio; 
import com.exemplo.hello.model.Repositorios;
import com.exemplo.hello.model.ProdutoCRM;
import com.exemplo.hello.model.ClienteCRM;

import com.exemplo.hello.redis.ProdutoEventPublisher;

import java.net.URL;
import java.util.ResourceBundle;

public class ProdutosController extends AbstractCrudController<ProdutoCRM, ProdutosView, Integer> implements Initializable {

    @FXML
    private TableView<ProdutosView> tabelaProdutos;

    @FXML
    private TextField quantidadeField;

    @FXML
    private TableColumn<ProdutosView, Integer> idCol;
    @FXML
    private TableColumn<ProdutosView, String> nomeCol;
    @FXML
    private TableColumn<ProdutosView, String> descricaoCol;
    @FXML
    private TableColumn<ProdutosView, Double> precoCol;
    @FXML
    private TableColumn<ProdutosView, Integer> estoqueCol;

    @FXML
    private TextField idField;
    @FXML
    private TextField nomeField;
    @FXML
    private TextField descricaoField;
    @FXML
    private TextField precoField;
    @FXML
    private TextField estoqueField;

    @FXML
    private Button adicionarButton;
    @FXML
    private Button atualizarButton;
    @FXML
    private Button deletarButton;
    @FXML
    private Button cancelarButton;
    @FXML
    private Button salvarButton;

    private ClienteCRM cliente;
    private static final Repositorio<ProdutoCRM, Integer> ProdutoRepo = Repositorios.PRODUTOCRM;

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        idCol.setCellValueFactory(new PropertyValueFactory<>("id"));
        nomeCol.setCellValueFactory(new PropertyValueFactory<>("nome"));
        descricaoCol.setCellValueFactory(new PropertyValueFactory<>("descricao"));
        precoCol.setCellValueFactory(new PropertyValueFactory<>("preco"));
        estoqueCol.setCellValueFactory(new PropertyValueFactory<>("estoque"));
        super.initialize();

        tabelaProdutos.getSelectionModel().selectedItemProperty().addListener((obs, antigo, novo) -> {
            if (novo != null) {
                quantidadeField.clear();
            }
        });
    }

    @Override
    protected Repositorio<ProdutoCRM, Integer> getRepositorio() {
        return ProdutoRepo;
    }

    @Override
    protected ProdutosView modelToView(ProdutoCRM c) {
        return new ProdutosView(
            c.getId(),
            c.getNome(),
            c.getDescricao(),
            c.getPreco(),
            c.getEstoque()
        );
    }

    @Override
    protected ProdutoCRM viewToModel() {
        ProdutoCRM c = new ProdutoCRM();
        c.setNome(nomeField.getText());
        c.setDescricao(descricaoField.getText());
        c.setPreco(Double.parseDouble(precoField.getText()));
        c.setEstoque(Integer.parseInt(estoqueField.getText()));

        return c;
    }

    @Override
    protected void preencherCampos(ProdutosView produto) {
        idField.setText(String.valueOf(produto.getId()));
        nomeField.setText(produto.getNome());
        descricaoField.setText(produto.getDescricao());
        precoField.setText(String.valueOf(produto.getPreco()));
        estoqueField.setText(String.valueOf(produto.getEstoque()));
    }

    @Override
    protected void limparCampos() {
        idField.clear();
        nomeField.clear();
        descricaoField.clear();
        precoField.clear();
        estoqueField.clear();
    }

    @Override
    protected void desabilitarCampos(boolean desabilitado) {
        nomeField.setDisable(desabilitado);
        descricaoField.setDisable(desabilitado);
        precoField.setDisable(desabilitado);
        estoqueField.setDisable(desabilitado);
    }

    @Override
    protected void desabilitarBotoes(boolean adicionar, boolean atualizar, boolean deletar, boolean cancelar, boolean salvar) {
        adicionarButton.setDisable(adicionar);
        atualizarButton.setDisable(atualizar);
        deletarButton.setDisable(deletar);
        cancelarButton.setDisable(cancelar);
        salvarButton.setDisable(salvar);
    }

    @Override
    protected TableView<ProdutosView> getTabela() {
        return tabelaProdutos;
    }

    @Override
    protected Integer getIdFromViewModel(ProdutosView viewModel) {
        return viewModel.getId();
    }

    @Override
    protected void setIdOnEntity(ProdutoCRM entidade, Integer id) {
        entidade.setId(id);
    }

    @FXML
    public void onAdicionar() {
        super.onAdicionar();
        desabilitarCampos(false);
    }

    @FXML
    public void onAdicionarAoCarrinho() {
        ProdutosView selecionado = tabelaProdutos.getSelectionModel().getSelectedItem();
        if (selecionado == null) {
            System.out.println("Nenhum produto selecionado para adicionar ao carrinho.");
            return;
        }

        ProdutoCRM produto = ProdutoRepo.loadFromId(selecionado.getId());
        int quantidade = 1;
        try {
            quantidade = Integer.parseInt(quantidadeField.getText());
            if (quantidade <= 0) {
                System.out.println("Quantidade invalida. Deve ser maior que zero.");
                return;
            } else if (quantidade > produto.getEstoque()){
                System.out.println("Não há estoque para a quantidade informada do produto escolhido.");
                return;
            }
        } catch (NumberFormatException e) {
            System.out.println("Quantidade invalida. Informe um numero inteiro.");
            return;
        }


        CarrinhoController carrinhoController = CarrinhoController.getInstancia();
        carrinhoController.adicionarProduto(produto, quantidade);

        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle("Sucesso");
        alert.setHeaderText(null);
        alert.setContentText("Produto adicionado ao carrinho com sucesso!");
        alert.showAndWait();
        System.out.println("Produto " + produto.getNome() + " adicionado ao carrinho (local), quantidade: " + quantidade);
        quantidadeField.clear();
    }


    @FXML
    public void onSalvar() {
        System.out.println("Salvando produto:");
        System.out.println("Nome: " + nomeField.getText());
        System.out.println("Descrição: " + descricaoField.getText());
        System.out.println("Preço: " + precoField.getText());
        System.out.println("Estoque: " + estoqueField.getText());
        super.onSalvar();

        ProdutoCRM produto = viewToModel();
        String acao = (produto.getId() == 0) ? "criado" : "atualizado";
        ProdutoEventPublisher.publicarEvento(acao, produto);
    }

    @FXML
    public void onAtualizar() {
        ProdutoCRM produto = viewToModel();
        super.onAtualizar();
        ProdutoEventPublisher.publicarEvento("atualizado", produto);
    }

    @FXML
    public void onDeletar() {
        ProdutoCRM produto = viewToModel();
        super.onDeletar();
        ProdutoEventPublisher.publicarEvento("removido", produto);
    }

    @FXML
    public void onCancelar() {
        super.onCancelar();
    }
}
