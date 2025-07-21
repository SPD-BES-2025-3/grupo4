package view;

import javafx.beans.property.SimpleDoubleProperty;
import javafx.beans.property.SimpleIntegerProperty;
import javafx.beans.property.SimpleStringProperty;

public class Produto {

    private SimpleIntegerProperty id;
    private SimpleStringProperty nome;
    private SimpleStringProperty descricao;
    private SimpleDoubleProperty preco;
    private SimpleIntegerProperty estoque;
    private SimpleStringProperty categoriaNome;

    public Produto(int id, String nome, String descricao, double preco, int estoque, String categoriaNome) {
        this.id = new SimpleIntegerProperty(id);
        this.nome = new SimpleStringProperty(nome);
        this.descricao = new SimpleStringProperty(descricao);
        this.preco = new SimpleDoubleProperty(preco);
        this.estoque = new SimpleIntegerProperty(estoque);
        this.categoriaNome = new SimpleStringProperty(categoriaNome);
    }

    // Getters e setters

    public int getId() {
        return id.get();
    }

    public void setId(int id) {
        this.id.set(id);
    }

    public String getNome() {
        return nome.get();
    }

    public void setNome(String nome) {
        this.nome.set(nome);
    }

    public String getDescricao() {
        return descricao.get();
    }

    public void setDescricao(String descricao) {
        this.descricao.set(descricao);
    }

    public double getPreco() {
        return preco.get();
    }

    public void setPreco(double preco) {
        this.preco.set(preco);
    }

    public int getEstoque() {
        return estoque.get();
    }

    public void setEstoque(int estoque) {
        this.estoque.set(estoque);
    }

    public String getCategoriaNome() {
        return categoriaNome.get();
    }

    public void setCategoriaNome(String categoriaNome) {
        this.categoriaNome.set(categoriaNome);
    }
}
