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

## 🧪 Rodar os testes

Execute o seguinte comando na raiz do projeto para rodar todos os testes com detalhes:

    ```bash
    pytest -v
    ```

---

Se você estiver usando um banco MongoDB local para testes, **certifique-se de que ele esteja rodando** antes de executar `pytest`.
