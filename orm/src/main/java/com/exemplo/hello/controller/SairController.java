package com.exemplo.hello.controller;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class SairController {

    @FXML
    public void onSair(ActionEvent event) {
        try {
            abrirTela("/view/login.fxml", "Login", event);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void abrirTela(String fxmlPath, String titulo, ActionEvent event) throws Exception {
        Stage stage = (Stage) ((javafx.scene.Node) event.getSource()).getScene().getWindow();
        Parent root = FXMLLoader.load(getClass().getResource(fxmlPath));
        stage.setScene(new Scene(root));
        stage.setTitle(titulo);
        stage.show();
    }
}
