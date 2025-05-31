import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from src.utils.config import TELEGRAM_BOT_TOKEN, DESCRIPTION, CATEGORY, DATE, PAYMENT_METHOD, INSTALLMENTS, VALUE, NEW_CATEGORY
from src.handlers.expense_handler import add_expense, description, category, date, payment_method, installments, value
from src.handlers.income_handler import add_income
from src.handlers.category_handler import new_category, save_category, list_categories

# Configuração do logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    await update.message.reply_text(
        'Olá! Eu sou seu assistente financeiro.\n\n'
        'Comandos disponíveis:\n'
        '/despesa - Adicionar uma despesa\n'
        '/receita - Adicionar uma receita\n'
        '/nova_categoria - Adicionar uma nova categoria\n'
        '/categorias - Listar suas categorias\n\n'
        'Exemplo de como adicionar uma despesa:\n'
        '1. Use /despesa\n'
        '2. Digite a descrição (ex: Compras no supermercado)\n'
        '3. Escolha ou adicione uma categoria\n'
        '4. Digite a data (DD/MM/AAAA)\n'
        '5. Escolha o método de pagamento\n'
        '6. Se for crédito, digite o número de parcelas\n'
        '7. Digite o valor total'
    )

async def help(update: Update, context):
    await start(update, context)

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Handler para o comando /start
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("categorias", list_categories))

    # Handler para adicionar despesa
    expense_handler = ConversationHandler(
        entry_points=[CommandHandler("despesa", add_expense)],
        states={
            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, description)],
            CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, category)],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, date)],
            PAYMENT_METHOD: [MessageHandler(filters.TEXT & ~filters.COMMAND, payment_method)],
            INSTALLMENTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, installments)],
            VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, value)],
        },
        fallbacks=[CommandHandler("start", start)]
    )
    application.add_handler(expense_handler)

    # Handler para adicionar receita
    income_handler = ConversationHandler(
        entry_points=[CommandHandler("receita", add_income)],
        states={
            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, description)],
            CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, category)],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, date)],
            VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, value)],
        },
        fallbacks=[CommandHandler("start", start)]
    )
    application.add_handler(income_handler)

    # Handler para adicionar categoria
    category_handler = ConversationHandler(
        entry_points=[CommandHandler("nova_categoria", new_category)],
        states={
            NEW_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_category)],
        },
        fallbacks=[CommandHandler("start", start)]
    )
    application.add_handler(category_handler)

    # Inicia o bot
    application.run_polling()

if __name__ == '__main__':
    main() 