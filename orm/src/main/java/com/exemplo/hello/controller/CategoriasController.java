package com.exemplo.hello.controller;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import com.exemplo.hello.model.Categoria;
import com.exemplo.hello.model.Repositorio; 
import com.exemplo.hello.model.Repositorios; 
import com.exemplo.hello.view.CategoriasView;

import java.net.URL;
import java.util.ResourceBundle;

public class CategoriasController extends AbstractCrudController<Categoria, CategoriasView, Integer> implements Initializable {

    @FXML
    private TableView<CategoriasView> tabelaCategorias;

    @FXML
    private TableColumn<CategoriasView, Integer> idCol;
    @FXML
    private TableColumn<CategoriasView, String> nomeCol;

    @FXML
    private TextField idField;
    @FXML
    private TextField nomeField;

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

    private static final Repositorio<Categoria, Integer> CategoriaRepo = Repositorios.CATEGORIA;

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        idCol.setCellValueFactory(new PropertyValueFactory<>("id"));
        nomeCol.setCellValueFactory(new PropertyValueFactory<>("nome"));
        super.initialize();
    }

    @Override
    protected Repositorio<Categoria, Integer> getRepositorio() {
        return CategoriaRepo;
    }

    @Override
    protected CategoriasView modelToView(Categoria model) {
        return new CategoriasView(model.getId(), model.getNome());
    }

    @Override
    protected Categoria viewToModel() {
        Categoria categoria = new Categoria();
        categoria.setNome(nomeField.getText());
        return categoria;
    }

    @Override
    protected void preencherCampos(CategoriasView viewModel) {
        idField.setText(String.valueOf(viewModel.getId()));
        nomeField.setText(viewModel.getNome());
    }

    @Override
    protected void limparCampos() {
        idField.clear();
        nomeField.clear();
    }

    @Override
    protected void desabilitarCampos(boolean desabilitado) {
        nomeField.setDisable(desabilitado);
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
    protected TableView<CategoriasView> getTabela() {
        return tabelaCategorias;
    }

    @Override
    protected Integer getIdFromViewModel(CategoriasView viewModel) {
        return viewModel.getId();
    }

    @Override
    protected void setIdOnEntity(Categoria entidade, Integer id) {
        entidade.setId(id);
    }

    @FXML
    public void onAdicionar() {
        super.onAdicionar();
        desabilitarCampos(false);
    }

    @FXML
    public void onSalvar() {
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
