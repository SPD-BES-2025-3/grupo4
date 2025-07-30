package com.exemplo.hello.controller;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.*;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.scene.control.cell.PropertyValueFactory;
import com.exemplo.hello.model.Repositorio; 
import com.exemplo.hello.model.Repositorios; 
import com.exemplo.hello.view.ClientesView;
import com.exemplo.hello.model.ClienteCRM;

import java.awt.*;
import java.net.URL;
import java.util.ResourceBundle;

public class ClientesController extends AbstractCrudController<ClienteCRM, ClientesView, Integer> implements Initializable {

    @FXML
    private TableView<ClientesView> tabelaClientes;

    @FXML
    private TableColumn<ClientesView, Integer> idCol;
    @FXML
    private TableColumn<ClientesView, String> nomeCol;
    @FXML
    private TableColumn<ClientesView, String> emailCol;
    @FXML
    private TableColumn<ClientesView, String> telefoneCol;

    @FXML
    private TextField idField;
    @FXML
    private TextField nomeField;
    @FXML
    private TextField emailField;
    @FXML
    private TextField telefoneField;

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

    private static final Repositorio<ClienteCRM, Integer> clienteRepo = Repositorios.CLIENTECRM;

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        idCol.setCellValueFactory(new PropertyValueFactory<>("id"));
        nomeCol.setCellValueFactory(new PropertyValueFactory<>("nome"));
        emailCol.setCellValueFactory(new PropertyValueFactory<>("email"));
        telefoneCol.setCellValueFactory(new PropertyValueFactory<>("telefone"));
        super.initialize();
    }

    @Override
    protected Repositorio<ClienteCRM, Integer> getRepositorio() {
        return clienteRepo;
    }

    @Override
    protected ClientesView modelToView(ClienteCRM c) {
        return new ClientesView(c.getId(), c.getNome(), c.getEmail(), c.getNumeroTelefone());
    }

    @Override
    protected ClienteCRM viewToModel() {
        ClienteCRM c = new ClienteCRM();
        c.setNome(nomeField.getText());
        c.setEmail(emailField.getText());
        c.setNumeroTelefone(telefoneField.getText());
        return c;
    }

    @Override
    protected void preencherCampos(ClientesView cliente) {
        idField.setText(String.valueOf(cliente.getId()));
        nomeField.setText(cliente.getNome());
        emailField.setText(cliente.getEmail());
        telefoneField.setText(cliente.getTelefone());
    }

    @Override
    protected void limparCampos() {
        idField.clear();
        nomeField.clear();
        emailField.clear();
        telefoneField.clear();
    }

    @Override
    protected void desabilitarCampos(boolean desabilitado) {
        nomeField.setDisable(desabilitado);
        emailField.setDisable(desabilitado);
        telefoneField.setDisable(desabilitado);
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
    protected TableView<ClientesView> getTabela() {
        return tabelaClientes;
    }

    @Override
    protected Integer getIdFromViewModel(ClientesView viewModel) {
        return viewModel.getId();
    }

    @Override
    protected void setIdOnEntity(ClienteCRM entidade, Integer id) {
        entidade.setId(id);
    }

    @FXML
    public void onAdicionar() {
        super.onAdicionar();
        desabilitarCampos(false);
    }

    @FXML
    public void onSalvar() {
        System.out.println("Clicou em Adicionar:");
        System.out.println("Nome: " + nomeField.getText());
        System.out.println("Email: " + emailField.getText());
        System.out.println("Telefone: " + telefoneField.getText());
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
