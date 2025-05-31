# Bot Telegram - Gerenciador Financeiro

Este é um bot do Telegram que ajuda a gerenciar suas finanças, registrando despesas e receitas em uma planilha do Google Sheets.

## Requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)
- Conta Google com acesso ao Google Sheets
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
SPREADSHEET_ID=id_da_sua_planilha
```

4. Configure o Google Sheets:
   - Acesse o [Google Cloud Console](https://console.cloud.google.com)
   - Crie um novo projeto
   - Ative a API do Google Sheets
   - Crie credenciais OAuth 2.0
   - Baixe o arquivo de credenciais e renomeie para `credentials.json`
   - Coloque o arquivo `credentials.json` na raiz do projeto
   - Crie uma planilha no Google Sheets e copie o ID da planilha (está na URL)
   - Compartilhe a planilha com o email do serviço que você criou

5. Estrutura da planilha:
   - Crie uma aba chamada "Despesas"
   - Configure as colunas na seguinte ordem:
     - Descrição
     - Categoria
     - Data
     - Método de Pagamento
     - Parcela
     - Valor Total
     - Valor Parcela

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