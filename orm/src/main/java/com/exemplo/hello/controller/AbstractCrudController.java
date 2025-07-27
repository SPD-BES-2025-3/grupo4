package com.exemplo.hello.controller;

import com.exemplo.hello.model.Repositorio; 
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.scene.control.Alert;
import javafx.scene.control.TableView;

public abstract class AbstractCrudController<E, V, ID> {

    protected abstract Repositorio<E, ID> getRepositorio();
    protected abstract V modelToView(E entidade);
    protected abstract E viewToModel();
    protected abstract void preencherCampos(V item);
    protected abstract void limparCampos();
    protected abstract void desabilitarCampos(boolean desabilitado);
    protected abstract void desabilitarBotoes(
            boolean adicionar, boolean atualizar,
            boolean deletar, boolean cancelar, boolean salvar);
    protected abstract TableView<V> getTabela();
    protected abstract ID getIdFromViewModel(V viewModel);
    protected abstract void setIdOnEntity(E entidade, ID id);

    public void initialize() {
        getTabela().setItems(loadAll());
        getTabela().getSelectionModel().selectedItemProperty().addListener(
                (obs, oldSelection, newSelection) -> {
                    if (newSelection != null) {
                        preencherCampos(newSelection);
                        desabilitarBotoes(false, false, false, true, true);
                    }
                });
        desabilitarCampos(true);
    }

    protected ObservableList<V> loadAll() {
        ObservableList<V> lista = FXCollections.observableArrayList();
        for (E entidade : getRepositorio().loadAll()) {
            lista.add(modelToView(entidade));
        }
        return lista;
    }

    public void onAdicionar() {
        getTabela().getSelectionModel().clearSelection();
        desabilitarCampos(false);
        desabilitarBotoes(true, true, true, false, false);
        limparCampos();
    }

    public void onSalvar() {
        V selecionado = getTabela().getSelectionModel().getSelectedItem();
        try {
            E entidade = viewToModel();

            if (selecionado != null) {
                ID id = getIdFromViewModel(selecionado);
                setIdOnEntity(entidade, id);
                getRepositorio().update(entidade);
                V atualizado = modelToView(entidade);
                int index = getTabela().getItems().indexOf(selecionado);
                getTabela().getItems().set(index, atualizado);
                getTabela().getSelectionModel().select(atualizado);
            } else {
                E salvo = getRepositorio().create(entidade);
                V viewItem = modelToView(salvo);
                getTabela().getItems().add(viewItem);
                getTabela().getSelectionModel().select(viewItem);
            }

            desabilitarCampos(true);
            desabilitarBotoes(false, true, true, true, true);
        } catch (Exception e) {
            new Alert(Alert.AlertType.ERROR, "Erro ao salvar: " + e.getMessage()).show();
        }
    }

    public void onAtualizar() {
        V selecionado = getTabela().getSelectionModel().getSelectedItem();
        if (selecionado == null) {
            new Alert(Alert.AlertType.WARNING, "Nenhum item selecionado para atualizar.").show();
            return;
        }
        try {
            E entidade = viewToModel();
            ID id = getIdFromViewModel(selecionado);
            setIdOnEntity(entidade, id);
            getRepositorio().update(entidade);
            V atualizado = modelToView(entidade);
            int index = getTabela().getItems().indexOf(selecionado);
            getTabela().getItems().set(index, atualizado);
            getTabela().getSelectionModel().select(atualizado);
            desabilitarCampos(false);
            desabilitarBotoes(true, true, true, false, false);
        } catch (Exception e) {
            new Alert(Alert.AlertType.ERROR, "Erro ao atualizar: " + e.getMessage()).show();
        }
    }

    public void onDeletar() {
        V selecionado = getTabela().getSelectionModel().getSelectedItem();
        if (selecionado == null) {
            new Alert(Alert.AlertType.WARNING, "Nenhum item selecionado para deletar.").show();
            return;
        }
        try {
            ID id = getIdFromViewModel(selecionado);
            E entidade = getRepositorio().loadFromId(id);

            if (entidade == null) {
                new Alert(Alert.AlertType.WARNING, "Registro não encontrado no banco.").show();
                return;
            }

            getRepositorio().delete(entidade);
            getTabela().getItems().remove(selecionado);
            limparCampos();
            desabilitarCampos(true);
            desabilitarBotoes(false, true, true, true, true);
        } catch (Exception e) {
            new Alert(Alert.AlertType.ERROR, "Erro ao deletar: " + e.getMessage()).show();
        }
    }

    public void onCancelar() {
        desabilitarCampos(true);
        desabilitarBotoes(false, true, true, true, true);
        limparCampos();
        getTabela().getSelectionModel().clearSelection();
    }
}
