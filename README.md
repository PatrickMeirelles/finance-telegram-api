# Bot Telegram - Gerenciador Financeiro

Este é um bot do Telegram que ajuda a gerenciar suas finanças, registrando despesas e receitas em um banco de dados PostgreSQL.

## Requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)
- PostgreSQL
- Bot do Telegram criado através do @BotFather

## Instalação

1. Clone este repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Configuração

1. Crie um bot no Telegram através do [@BotFather](https://t.me/botfather)
2. Copie o token fornecido pelo BotFather
3. Crie um arquivo `.env` na raiz do projeto e adicione:
```
TELEGRAM_BOT_TOKEN=seu_token_aqui
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=nome_do_banco
DB_HOST=localhost
DB_PORT=5432
```

4. Configure o banco de dados PostgreSQL:
   - Crie um banco de dados
   - Execute os scripts SQL para criar as tabelas necessárias:
     ```sql
     CREATE TABLE categories (
         id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
         "user" TEXT,
         description TEXT,
         created_at TEXT DEFAULT now(),
         updated_at TEXT DEFAULT now()
     );

     CREATE TABLE transactions (
         id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
         "user" TEXT,
         description TEXT,
         category_id INTEGER,
         date DATE DEFAULT now(),
         type_id INTEGER,
         installments TEXT,
         total_amount NUMERIC(20, 2),
         amount_installment NUMERIC(20, 2),
         created_at TEXT DEFAULT now(),
         updated_at TEXT DEFAULT now(),
         is_expense BOOLEAN DEFAULT true,
         CONSTRAINT transactions_pkey PRIMARY KEY (id)
     );
     ```

## Uso

Para iniciar o bot, execute:
```bash
python bot.py
```

O bot oferece as seguintes funcionalidades:
- Adicionar despesas com suporte a parcelamento
- Adicionar receitas
- Visualizar despesas e receitas (em desenvolvimento)

Para adicionar uma despesa:
1. Clique em "Adicionar Despesa"
2. Siga as instruções do bot:
   - Informe a descrição
   - Selecione a categoria
   - Digite a data (DD/MM/AAAA)
   - Escolha o método de pagamento
   - Se for crédito, informe o número de parcelas
   - Digite o valor total

Para parar o bot, pressione `Ctrl+C` no terminal. 