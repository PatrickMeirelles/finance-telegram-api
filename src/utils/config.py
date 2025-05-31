import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Database Configuration
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# Conversation States
DESCRIPTION = 'DESCRIPTION'
CATEGORY = 'CATEGORY'
DATE = 'DATE'
PAYMENT_METHOD = 'PAYMENT_METHOD'
INSTALLMENTS = 'INSTALLMENTS'
VALUE = 'VALUE'
NEW_CATEGORY = 'NEW_CATEGORY'
MONTH = 'MONTH'
YEAR = 'YEAR'

# Estados da conversa para despesas
DESCRICAO, CATEGORIA, DATA, METODO_PAGAMENTO, PARCELAS, VALOR = range(6)
NOVA_CATEGORIA = 7

# Estados da conversa para receitas
RECEITA_DESCRICAO, RECEITA_CATEGORIA, RECEITA_DATA, RECEITA_VALOR = range(8, 12)

# Estados da conversa para visualização
VIEW_EXPENSE_MONTH, VIEW_EXPENSE_YEAR = range(12, 14)
VIEW_INCOME_MONTH, VIEW_INCOME_YEAR = range(14, 16) 