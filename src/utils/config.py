import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Google Sheets Configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
CATEGORIES_RANGE = 'Categorias!A:B'
EXPENSES_RANGE = 'Despesas!A:H'
INCOME_RANGE = 'Receitas!A:E'

# Conversation States
DESCRIPTION = 'DESCRIPTION'
CATEGORY = 'CATEGORY'
DATE = 'DATE'
PAYMENT_METHOD = 'PAYMENT_METHOD'
INSTALLMENTS = 'INSTALLMENTS'
VALUE = 'VALUE'
NEW_CATEGORY = 'NEW_CATEGORY'

# Estados da conversa para despesas
DESCRICAO, CATEGORIA, DATA, METODO_PAGAMENTO, PARCELAS, VALOR = range(6)
NOVA_CATEGORIA = 7

# Estados da conversa para receitas
RECEITA_DESCRICAO, RECEITA_CATEGORIA, RECEITA_DATA, RECEITA_VALOR = range(8, 12) 