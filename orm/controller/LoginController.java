package controller;

import javafx.fxml.FXML;
import javafx.scene.control.TextField;
import javafx.scene.control.PasswordField;
import javafx.scene.control.Label;
import javafx.stage.Stage;
import javafx.scene.Scene;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;

import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.DaoManager;

import model.*;

public class LoginController {

    @FXML private TextField emailField;
    @FXML private PasswordField senhaField;
    @FXML private Label mensagemLabel;

    private Database database;

    public LoginController() {

        database = new Database("app.sqlite");
    }

    @FXML
    private void handleLogin() {
        String email = emailField.getText().trim();
        String senha = senhaField.getText().trim();

        mensagemLabel.setText("");

        try {
            Dao<Cliente, Integer> clienteDao = DaoManager.createDao(database.getConnection(), Cliente.class);
            Cliente cliente = clienteDao.queryBuilder()
                    .where().eq("email", email).and().eq("senha", senha)
                    .queryForFirst();

            if (cliente != null) {
                Sessao.setCliente(cliente);
                abrirTela("/view/ClienteApp.fxml", "Cliente");
                return;
            }

            Dao<Administrador, Integer> adminDao = DaoManager.createDao(database.getConnection(), Administrador.class);
            Administrador admin = adminDao.queryBuilder()
                    .where().eq("email", email).and().eq("senha", senha)
                    .queryForFirst();

            if (admin != null) {
                abrirTela("/view/adminApp.fxml", "Admin");
                return;
            }

            mensagemLabel.setText("Email ou senha inválidos.");
        } catch (Exception e) {
            e.printStackTrace();
            mensagemLabel.setText("Erro ao tentar efetuar login.");
        }
    }

    private void abrirTela(String fxmlPath, String titulo) throws Exception {
        Stage stage = (Stage) emailField.getScene().getWindow();
        Parent root = FXMLLoader.load(getClass().getResource(fxmlPath));
        stage.setScene(new Scene(root));
        stage.setTitle(titulo);
    }

    @FXML
    private void abrirTelaCadastro() {
        try {
            abrirTela("/view/cadastro_cliente.fxml", "Cadastro de Cliente");
        } catch (Exception e) {
            e.printStackTrace();
            mensagemLabel.setText("Erro ao abrir cadastro.");
        }
    }
}