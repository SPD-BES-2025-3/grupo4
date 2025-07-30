package com.exemplo.hello.redis;

import com.exemplo.hello.model.ProdutoCRM;
import com.google.gson.Gson;
import io.lettuce.core.RedisClient;
import io.lettuce.core.api.sync.RedisCommands;

public class ProdutoEventPublisher {
    private static final RedisClient redisClient = RedisClient.create("redis://localhost:6379");
    private static final RedisCommands<String, String> commands = redisClient.connect().sync();
    private static final Gson gson = new Gson();

    public static void publicarEvento(String acao, ProdutoCRM produto) {
        EventoProduto evento = new EventoProduto(acao, produto);
        String json = gson.toJson(evento);
        commands.publish("produtos", json);
        System.out.println("Evento publicado no Redis: " + json);
    }

    public static void fechar() {
        redisClient.shutdown();
    }

    static class EventoProduto {
        String acao; //
        ProdutoCRM produto;

        public EventoProduto(String acao, ProdutoCRM produto) {
            this.acao = acao;
            this.produto = produto;
        }
    }
}
