package com.exemplo.hello.redis;

import com.google.gson.Gson;
import com.exemplo.hello.model.CarrinhoItem;
import io.lettuce.core.RedisClient;
import io.lettuce.core.api.sync.RedisCommands;

import java.util.List;

public class RedisPublisher {
    private static RedisPublisher instancia;
    private final RedisClient client;
    private final RedisCommands<String, String> commands;
    private final Gson gson = new Gson();

    public RedisPublisher() {
        client = RedisClient.create("redis://localhost:6379");
        commands = client.connect().sync();
    }

    public static synchronized RedisPublisher getInstancia() {
        if (instancia == null) {
            instancia = new RedisPublisher();
        }
        return instancia;
    }

    public void publicarCarrinhoFinalizado(List<CarrinhoItem> itens, int clienteId) {
        String canal = "carrinho:" + clienteId;
        String json = gson.toJson(itens);
        commands.publish(canal, json);
    }

    public static void publicar(String canal, String json) {
        getInstancia().commands.publish(canal, json);
    }

    public void fechar() {
        client.shutdown();
    }
}
