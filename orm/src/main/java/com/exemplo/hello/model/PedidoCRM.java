package com.exemplo.hello.model;

import com.j256.ormlite.table.DatabaseTable;
import com.j256.ormlite.field.DatabaseField;

import java.util.Date;

@DatabaseTable(tableName = "pedido_crm")
public class PedidoCRM {

    @DatabaseField(generatedId = true)
    private int id;

    @DatabaseField(canBeNull = false)
    private Date data;

    @DatabaseField(canBeNull = false)
    private String status;

    @DatabaseField(canBeNull = false)
    private double total;

    @DatabaseField(canBeNull = false, foreign = true, foreignAutoRefresh = true)
    private ClienteCRM cliente;

    // Getters e Setters

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public Date getData() {
        return data;
    }

    public void setData(Date data) {
        this.data = data;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public double getTotal() {
        return total;
    }

    public void setTotal(double total) {
        this.total = total;
    }

    public ClienteCRM getCliente() {
        return cliente;
    }

    public void setCliente(ClienteCRM cliente) {
        this.cliente = cliente;
    }
}
