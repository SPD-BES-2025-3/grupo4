package com.exemplo.hello.redis;

import com.google.gson.Gson;
import io.lettuce.core.RedisClient;
import io.lettuce.core.api.sync.RedisCommands;

public class RedisPublisher {
    private final RedisClient client;
    private final RedisCommands<String, String> commands;
    private final Gson gson = new Gson();

    public RedisPublisher() {
        client = RedisClient.create("redis://localhost:6379");
        commands = client.connect().sync();
    }

    public void publicarProdutoParaCarrinho(Object produto, String canal) {
        String json = gson.toJson(produto);
        commands.publish(canal, json);
    }

    public void fechar() {
        client.shutdown();
    }
}