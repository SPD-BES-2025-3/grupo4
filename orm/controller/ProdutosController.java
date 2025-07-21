package controller;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import model.Repositorio;
import model.Repositorios;
import view.ProdutosView;
import model.Produto;
import model.Categoria;

import java.net.URL;
import java.util.ResourceBundle;

public class ProdutosController extends AbstractCrudController<Produto, ProdutosView, Integer> implements Initializable {

    @FXML
    private TableView<ProdutosView> tabelaProdutos;

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
    private TableColumn<ProdutosView, Integer> categoriaCol;

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
    private TextField categoriaField;

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

    private static final Repositorio<Produto, Integer> ProdutoRepo = Repositorios.PRODUTO;
    private static final Repositorio<Categoria, Integer> CategoriaRepo = Repositorios.CATEGORIA;

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        idCol.setCellValueFactory(new PropertyValueFactory<>("id"));
        nomeCol.setCellValueFactory(new PropertyValueFactory<>("nome"));
        descricaoCol.setCellValueFactory(new PropertyValueFactory<>("descricao"));
        precoCol.setCellValueFactory(new PropertyValueFactory<>("preco"));
        estoqueCol.setCellValueFactory(new PropertyValueFactory<>("estoque"));
        categoriaCol.setCellValueFactory(new PropertyValueFactory<>("categoria"));
        super.initialize();
    }

    @Override
    protected Repositorio<Produto, Integer> getRepositorio() {
        return ProdutoRepo;
    }

    @Override
    protected ProdutosView modelToView(Produto c) {
        return new ProdutosView(
            c.getId(),
            c.getNome(),
            c.getDescricao(),
            c.getPreco(),
            c.getEstoque(),
            c.getCategoria() != null ? c.getCategoria().getId() : null
        );
    }

    @Override
    protected Produto viewToModel() {
        Produto c = new Produto();
        c.setNome(nomeField.getText());
        c.setDescricao(descricaoField.getText());
        c.setPreco(Double.parseDouble(precoField.getText()));
        c.setEstoque(Integer.parseInt(estoqueField.getText()));

        // Busca a categoria pelo ID digitado
        int categoriaId = Integer.parseInt(categoriaField.getText());
        Categoria categoria = CategoriaRepo.loadFromId(categoriaId);
        c.setCategoria(categoria);

        return c;
    }

    @Override
    protected void preencherCampos(ProdutosView produto) {
        idField.setText(String.valueOf(produto.getId()));
        nomeField.setText(produto.getNome());
        descricaoField.setText(produto.getDescricao());
        precoField.setText(String.valueOf(produto.getPreco()));
        estoqueField.setText(String.valueOf(produto.getEstoque()));
        categoriaField.setText(String.valueOf(produto.getCategoria()));
    }

    @Override
    protected void limparCampos() {
        idField.clear();
        nomeField.clear();
        descricaoField.clear();
        precoField.clear();
        estoqueField.clear();
        categoriaField.clear();
    }

    @Override
    protected void desabilitarCampos(boolean desabilitado) {
        nomeField.setDisable(desabilitado);
        descricaoField.setDisable(desabilitado);
        precoField.setDisable(desabilitado);
        estoqueField.setDisable(desabilitado);
        categoriaField.setDisable(desabilitado);
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
    protected void setIdOnEntity(Produto entidade, Integer id) {
        entidade.setId(id);
    }

    @FXML
    public void onAdicionar() {
        super.onAdicionar();
        desabilitarCampos(false);
    }

    @FXML
    public void onSalvar() {
        System.out.println("Salvando produto:");
        System.out.println("Nome: " + nomeField.getText());
        System.out.println("Descrição: " + descricaoField.getText());
        System.out.println("Preço: " + precoField.getText());
        System.out.println("Estoque: " + estoqueField.getText());
        System.out.println("Categoria: " + categoriaField.getText());
        super.onSalvar();
    }

    @FXML
    public void onAtualizar() {
        super.onAtualizar();
    }

    @FXML
    public void onDeletar() {
        super.onDeletar();
    }

    @FXML
    public void onCancelar() {
        super.onCancelar();
    }
}
