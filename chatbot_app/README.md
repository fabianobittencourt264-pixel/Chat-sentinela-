# Chatbot Sentinela Nativense

Este é um projeto de chatbot de assistente cívico criado para a Prefeitura de Natividade da Serra. Ele utiliza uma arquitetura simples com um backend em Flask (Python) e uma interface de usuário web básica.

Toda a lógica, conhecimento e persona do chatbot são carregados dinamicamente a partir do arquivo `config.json`, tornando-o facilmente configurável sem a necessidade de alterar o código-fonte.

---

## Requisitos

- Python 3.7 ou superior
- `pip` (gerenciador de pacotes do Python)

---

## Instalação

Siga os passos abaixo para configurar o ambiente e instalar as dependências do projeto.

1.  **Navegue até o diretório do projeto:**
    Abra seu terminal e navegue até a pasta `chatbot_app` que contém este arquivo `README.md`.

2.  **(Opcional, mas recomendado) Crie e ative um ambiente virtual:**
    Isso isola as dependências do projeto do seu sistema global.

    - No macOS/Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```
    - No Windows:
      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      ```

3.  **Instale as dependências:**
    Com seu ambiente virtual ativado, instale as bibliotecas Python necessárias.
    ```bash
    pip install -r requirements.txt
    ```

---

## Executando a Aplicação

Depois de instalar as dependências, você pode iniciar o servidor do chatbot.

1.  **Inicie o servidor Flask:**
    Certifique-se de que você ainda está no diretório `chatbot_app` e execute o seguinte comando:
    ```bash
    python app.py
    ```

2.  **Verifique a saída:**
    Você deverá ver uma mensagem no seu terminal indicando que o servidor está rodando, algo como:
    ```
     * Running on http://127.0.0.1:5000
    ```

---

## Como Usar o Chatbot

1.  **Abra seu navegador:**
    Abra seu navegador de internet preferido (Chrome, Firefox, etc.).

2.  **Acesse o endereço local:**
    Na barra de endereços, digite `http://127.0.0.1:5000` e pressione Enter.

3.  **Interaja com o chatbot:**
    A interface de chat será carregada. Digite uma pergunta na caixa de mensagem (por exemplo, "Como tiro a segunda via do IPTU?") e clique em "Enviar" para começar.

---

## Estrutura do Projeto

-   `config.json`: O "cérebro" do chatbot. Contém todas as fontes de dados, regras de conversação e persona.
-   `app.py`: O servidor web Flask. Ele serve a interface do usuário e fornece o endpoint `/ask` para a comunicação com o frontend.
-   `chatbot_logic.py`: O módulo principal da lógica do chatbot. É responsável por interpretar as mensagens do usuário e formular respostas com base no `config.json`.
-   `/templates/index.html`: A estrutura HTML da página de chat.
-   `/static/styles.css`: O arquivo de estilo para a interface.
-   `/static/script.js`: O código JavaScript que gerencia a interação do usuário e a comunicação com o backend.
-   `requirements.txt`: Lista as dependências Python do projeto.
