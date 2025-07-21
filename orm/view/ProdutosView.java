package view;

import javafx.beans.property.*;

public class ProdutosView {

    private final SimpleIntegerProperty id;
    private final SimpleStringProperty nome;
    private final SimpleStringProperty descricao;
    private final SimpleDoubleProperty preco;
    private final SimpleIntegerProperty estoque;
    private final SimpleIntegerProperty categoria;

    public ProdutosView(int id, String nome, String descricao, double preco, int estoque, Integer categoria) {
        this.id = new SimpleIntegerProperty(id);
        this.nome = new SimpleStringProperty(nome);
        this.descricao = new SimpleStringProperty(descricao);
        this.preco = new SimpleDoubleProperty(preco);
        this.estoque = new SimpleIntegerProperty(estoque);
        this.categoria = new SimpleIntegerProperty(categoria != null ? categoria : 0);
    }


    public int getId() { return id.get(); }
    public void setId(int id) { this.id.set(id); }
    public IntegerProperty idProperty() { return id; }

    public String getNome() { return nome.get(); }
    public void setNome(String nome) { this.nome.set(nome); }
    public StringProperty nomeProperty() { return nome; }

    public String getDescricao() { return descricao.get(); }
    public void setDescricao(String descricao) { this.descricao.set(descricao); }
    public StringProperty descricaoProperty() { return descricao; }

    public double getPreco() { return preco.get(); }
    public void setPreco(double preco) { this.preco.set(preco); }
    public DoubleProperty precoProperty() { return preco; }

    public int getEstoque() { return estoque.get(); }
    public void setEstoque(int estoque) { this.estoque.set(estoque); }
    public IntegerProperty estoqueProperty() { return estoque; }

    public int getCategoria() { return categoria.get(); }
    public void setCategoria(int categoria) { this.categoria.set(categoria); }
    public IntegerProperty categoriaProperty() { return categoria; }
}
