package controller;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.event.ActionEvent;
import javafx.scene.control.TextField;
import javafx.scene.control.Button;
import model.Cliente;
import model.Sessao;

import java.net.URL;
import java.util.ResourceBundle;

public class ClienteController implements Initializable {

    @FXML private TextField nomeField;
    @FXML private TextField emailField;
    @FXML private TextField telefoneField;

    @FXML private Button atualizarButton;
    @FXML private Button salvarButton;
    @FXML private Button cancelarButton;

    private Cliente cliente;

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        cliente = Sessao.getCliente();
        if (cliente != null) {
            preencherCampos(cliente);
            atualizarButton.setDisable(false);
            desabilitarCampos(true);
        }
    }

    private void preencherCampos(Cliente c) {
        nomeField.setText(c.getNome());
        emailField.setText(c.getEmail());
        telefoneField.setText(c.getNumeroTelefone());
    }

    private void desabilitarCampos(boolean desabilitar) {
        nomeField.setDisable(desabilitar);
        emailField.setDisable(desabilitar);
        telefoneField.setDisable(desabilitar);
    }

    @FXML
    public void onAtualizar() {
        desabilitarCampos(false);
        salvarButton.setDisable(false);
        cancelarButton.setDisable(false);
        atualizarButton.setDisable(true);
    }

    @FXML
    public void onSalvar() {
        try {
            cliente.setNome(nomeField.getText());
            cliente.setEmail(emailField.getText());

            model.Repositorios.CLIENTE.update(cliente);

            desabilitarCampos(true);
            salvarButton.setDisable(true);
            cancelarButton.setDisable(true);
            atualizarButton.setDisable(false);

            System.out.println("Cliente atualizado com sucesso.");
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("Erro ao salvar cliente.");
        }
    }

    @FXML
    public void onCancelar() {
        preencherCampos(cliente);
        desabilitarCampos(true);
        salvarButton.setDisable(true);
        cancelarButton.setDisable(true);
        atualizarButton.setDisable(false);
    }

    public void onDeletar(ActionEvent event) {
    }

}

    
