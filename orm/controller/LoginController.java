package controller;

import javafx.fxml.FXML;
import javafx.scene.control.TextField;
import javafx.scene.control.PasswordField;
import javafx.stage.Stage;
import javafx.scene.Scene;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.DaoManager;
import model.*;
import java.sql.SQLException;

public class LoginController {

    @FXML private TextField emailField;
    @FXML private PasswordField senhaField;

    private Database database;

    public LoginController() {
        database = new Database("app.sqlite");
    }

    @FXML
    private void handleLogin() {
        String email = emailField.getText().trim();
        String senha = senhaField.getText().trim();
    
        try {
            Dao<Cliente, Integer> clienteDao = DaoManager.createDao(database.getConnection(), Cliente.class);
            Cliente cliente = clienteDao.queryBuilder()
                .where().eq("email", email).and().eq("senha", senha)
                .queryForFirst();
    
            if (cliente != null) {
                Stage stage = (Stage) emailField.getScene().getWindow();
                Parent root = FXMLLoader.load(getClass().getResource("/view/appCliente.fxml"));
                stage.setScene(new Scene(root));
                stage.setTitle("Cliente");
                return;
            }
    
            Dao<Administrador, Integer> adminDao = DaoManager.createDao(database.getConnection(), Administrador.class);
            Administrador admin = adminDao.queryBuilder()
                .where().eq("email", email).and().eq("senha", senha)
                .queryForFirst();
    
            if (admin != null) {
                Stage stage = (Stage) emailField.getScene().getWindow();
                Parent root = FXMLLoader.load(getClass().getResource("/view/appAdmin.fxml"));
                stage.setScene(new Scene(root));
                stage.setTitle("Admin");
                return;
            }
    
            System.out.println("Login inválido.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @FXML
    private void abrirTelaCadastro() {
        try {
            Stage stage = (Stage) emailField.getScene().getWindow();
            Parent root = FXMLLoader.load(getClass().getResource("/view/cadastro_cliente.fxml"));
            stage.setScene(new Scene(root));
            stage.setTitle("Cadastro de Cliente");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
}
