# Chatbot Sentinela Nativense

Este é um projeto de chatbot de assistente cívico criado para a Prefeitura de Natividade da Serra. Ele utiliza uma arquitetura simples com um backend em Flask (Python) e uma interface de usuário web básica.

Toda a lógica, conhecimento e persona do chatbot são carregados dinamicamente a partir do arquivo `config.json`, tornando-o facilmente configurável sem a necessidade de alterar o código-fonte.

---

## Requisitos

- Python 3.7 ou superior
- `pip` (gerenciador de pacotes do Python)
- Uma chave de API (API Key) do [Google AI Studio](https://aistudio.google.com/app/apikey).

---

## Configuração da IA (Google Gemini)

A inteligência do chatbot agora é potencializada pela API do Google Gemini. Para que a aplicação funcione, você precisa fornecer sua chave de API de forma segura através de uma variável de ambiente.

### Para Deploy na Vercel (Produção)

1.  No painel do seu projeto na Vercel, vá para **Settings** -> **Environment Variables**.
2.  Clique em **Add New**.
3.  No campo **Name**, digite `GEMINI_API_KEY`.
4.  No campo **Value**, cole a sua chave de API do Google Gemini.
5.  Salve a variável. A Vercel irá automaticamente reiniciar seu projeto com a nova variável de ambiente configurada.

### Para Testes Locais

Você precisa definir a variável de ambiente no seu terminal antes de rodar o `gunicorn`.

- **No macOS/Linux:**
  ```bash
  export GEMINI_API_KEY="sua_chave_de_api_aqui"
  gunicorn api.chatbot_app.app:app
  ```

- **No Windows (Command Prompt):**
  ```bash
  set GEMINI_API_KEY="sua_chave_de_api_aqui"
  gunicorn api.chatbot_app.app:app
  ```

---

## Instalação

Siga os passos abaixo para configurar o ambiente e instalar as dependências do projeto.

1.  **Navegue até o diretório raiz do projeto:**
    Abra seu terminal e certifique-se de que está na pasta raiz que contém a pasta `api`.

2.  **(Opcional, mas recomendado) Crie e ative um ambiente virtual:**
    - No macOS/Linux: `python3 -m venv venv && source venv/bin/activate`
    - No Windows: `python -m venv venv && .\venv\Scripts\activate`

3.  **Instale as dependências:**
    O arquivo `requirements.txt` está na raiz do projeto.
    ```bash
    pip install -r requirements.txt
    ```

---

## Executando a Aplicação Localmente

Para rodar o servidor localmente para testes, utilizamos o `gunicorn`, que é um servidor WSGI mais robusto e simula melhor o ambiente de produção da Vercel.

1.  **Inicie o servidor Gunicorn:**
    A partir da raiz do projeto, execute:
    ```bash
    gunicorn api.chatbot_app.app:app
    ```

2.  **Verifique a saída:**
    O servidor estará rodando em `http://127.0.0.1:8000`.

3.  **Teste o endpoint de saúde:**
    Em outro terminal, você pode verificar se o servidor está funcionando:
    ```bash
    curl http://127.0.0.1:8000/health
    ```
    A resposta deve ser `{"status":"ok"}`.

---

## Como Usar o Chatbot

1.  **Abra seu navegador:**
    Com o servidor rodando, abra seu navegador.

2.  **Acesse o endereço local:**
    Na barra de endereços, digite `http://127.0.0.1:8000` e pressione Enter.

3.  **Interaja com o chatbot:**
    A interface de chat será carregada.

---

## Estrutura do Projeto para Vercel

O projeto foi reestruturado para seguir as convenções da Vercel para deploy de funções Python.

-   `/api`: Diretório padrão que a Vercel procura por funções serverless.
-   `/api/chatbot_app/`: O nosso código de aplicação, agora como um pacote Python.
    -   `__init__.py`: Arquivo que define `chatbot_app` como um pacote.
    -   `app.py`: O entrypoint da aplicação Flask.
    -   `chatbot_logic.py`: A lógica principal do chatbot.
    -   `config.json`, `static/`, `templates/`: Arquivos e pastas de suporte.
-   `requirements.txt`: Lista de dependências Python na raiz do projeto.
-   `vercel.json`: Arquivo de configuração para o deploy na Vercel.
