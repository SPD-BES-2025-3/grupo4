package com.exemplo.hello.controller;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.TextField;
import javafx.scene.control.PasswordField;
import javafx.scene.control.Button;
import javafx.scene.control.Alert;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;
import javafx.scene.Node;
import javafx.scene.input.MouseEvent;

import com.exemplo.hello.model.ClienteCRM;
import com.exemplo.hello.model.Endereco;
import com.exemplo.hello.model.Database;
import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.DaoManager;

import java.net.URL;
import java.util.ResourceBundle;

public class CadastroClienteController implements Initializable {

    @FXML private TextField nomeField;
    @FXML private TextField emailField;
    @FXML private PasswordField senhaField;
    @FXML private TextField telefoneField;
    @FXML private TextField ruaField;
    @FXML private TextField numeroField;
    @FXML private TextField bairroField;
    @FXML private TextField cidadeField;
    @FXML private TextField estadoField;
    @FXML private TextField cepField;
    
    @FXML private Button salvarButton;
    @FXML private Button cancelarButton;

    private Database database;
    private Dao<ClienteCRM, Integer> clienteDao;
    private Dao<Endereco, Integer> enderecoDao;

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        try {
            database = new Database("projetospd");
            clienteDao = DaoManager.createDao(database.getConnection(), ClienteCRM.class);
            enderecoDao = DaoManager.createDao(database.getConnection(), Endereco.class);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @FXML
    private void handleSalvar() {
        try {
            Endereco endereco = new Endereco();
            endereco.setRua(ruaField.getText());
            endereco.setNumero(numeroField.getText());
            endereco.setBairro(bairroField.getText());
            endereco.setCidade(cidadeField.getText());
            endereco.setEstado(estadoField.getText());
            endereco.setCep(cepField.getText());

            enderecoDao.create(endereco);

            ClienteCRM cliente = new ClienteCRM();
            cliente.setNome(nomeField.getText());
            cliente.setEmail(emailField.getText());
            cliente.setSenha(senhaField.getText());
            cliente.setNumeroTelefone(telefoneField.getText());
            cliente.setEndereco(endereco);

            clienteDao.create(cliente);

            Alert alert = new Alert(Alert.AlertType.INFORMATION);
            alert.setTitle("Sucesso");
            alert.setHeaderText(null);
            alert.setContentText("Cliente cadastrado com sucesso!");
            alert.showAndWait();
            
            Parent root = FXMLLoader.load(getClass().getResource("/view/Login.fxml"));
            Stage stage = (Stage) salvarButton.getScene().getWindow();
            stage.setScene(new Scene(root));
            stage.show();
            
            limparCampos();

        } catch (Exception e) {
            e.printStackTrace();
            Alert alert = new Alert(Alert.AlertType.ERROR);
            alert.setTitle("Erro");
            alert.setHeaderText(null);
            alert.setContentText("Erro ao cadastrar cliente.");
            alert.showAndWait();
        }
    }

    @FXML
    private void handleCancelar() {
        limparCampos();
    }

    private void limparCampos() {
        nomeField.clear();
        emailField.clear();
        senhaField.clear();
        telefoneField.clear();
        ruaField.clear();
        numeroField.clear();
        bairroField.clear();
        cidadeField.clear();
        estadoField.clear();
        cepField.clear();
    }
    
    @FXML
    private void handleVoltarLogin(MouseEvent event) {
        try {
            Parent root = FXMLLoader.load(getClass().getResource("/view/Login.fxml"));
            Stage stage = (Stage) ((Node) event.getSource()).getScene().getWindow();
            stage.setScene(new Scene(root));
            stage.show();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
