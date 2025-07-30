package com.exemplo.hello.redis;

import com.google.gson.Gson;
import io.lettuce.core.RedisClient;
import io.lettuce.core.api.sync.RedisCommands;

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

    public void publicarProdutoParaCarrinho(Object produto, int quantidade, String canal) {
        ProdutoComQuantidade pcq = new ProdutoComQuantidade(produto, quantidade);
        String json = gson.toJson(pcq);
        commands.publish(canal, json);
    }

    public void fechar() {
        client.shutdown();
    }

    public static void publicar(String canal, String json) {
        getInstancia().commands.publish(canal, json);
    }

    private static class ProdutoComQuantidade {
        private final Object produto;
        private final int quantidade;

        public ProdutoComQuantidade(Object produto, int quantidade) {
            this.produto = produto;
            this.quantidade = quantidade;
        }
    }
}