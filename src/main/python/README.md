# 🧪 Testes do Projeto Python

Este projeto usa [`pytest`](https://docs.pytest.org/) e [`pytest-asyncio`](https://github.com/pytest-dev/pytest-asyncio) para testes assíncronos em um ambiente Python com [Beanie](https://roman-right.github.io/beanie/) e [MongoDB].

---

## ⚙️ Como configurar o ambiente virtual

1. **Criar o ambiente virtual:**

    ```bash
    python -m venv venv
    ```

2. **Ativar o ambiente virtual:**

    - **Linux/macOS:**

    ```bash
    source venv/bin/activate
    ```

    - **Windows:**

    ```bash
    venv\Scripts\activate
    ```

3. **Instalar as dependências:**

    Certifique-se de estar na mesma pasta que o `requirements.txt`, então execute:

    ```bash
    pip install -r requirements.txt
    ```

---

## 🚀 Como rodar o FastAPI

Este projeto utiliza [FastAPI](https://fastapi.tiangolo.com/) para construir uma API moderna, rápida e assíncrona. Siga os passos abaixo para iniciar a aplicação:

### ▶️ Executar a API localmente

1. **Verifique se todas as dependências estão instaladas** conforme a seção anterior.

2. **Execute o servidor com Uvicorn:**

   ```bash
   uvicorn main:app --reload
   ```

   - `main`: nome do arquivo Python onde está a instância `FastAPI()`.
   - `app`: nome da variável que representa a instância da aplicação.
   - `--reload`: habilita o modo de recarregamento automático em desenvolvimento.

3. **Acesse a documentação automática:**

    Abra seu navegador e visite:

   - [Docs](http://127.0.0.1:8000/docs)

   ou

   - [Redoc](http://127.0.0.1:8000/redoc)

   Ambas oferecem uma visualização interativa da API baseada nos endpoints definidos no projeto.

---

## 🧪 Rodar os testes

Execute o seguinte comando na raiz do projeto para rodar todos os testes com detalhes:

    ```bash
    pytest -v
    ```

---

Se você estiver usando um banco MongoDB local para testes, **certifique-se de que ele esteja rodando** antes de executar `pytest`.
