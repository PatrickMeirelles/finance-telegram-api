import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
from src.utils.config import (
    TELEGRAM_BOT_TOKEN, DESCRIPTION, CATEGORY, DATE, PAYMENT_METHOD, 
    INSTALLMENTS, VALUE, NEW_CATEGORY, MONTH, YEAR,
    VIEW_EXPENSE_MONTH, VIEW_EXPENSE_YEAR, VIEW_INCOME_MONTH, VIEW_INCOME_YEAR
)
from src.handlers.expense_handler import add_expense, description, category, date, payment_method, installments, value
from src.handlers.income_handler import add_income, description as income_description, category as income_category, date as income_date, value as income_value
from src.handlers.category_handler import new_category, save_category, list_categories
from src.handlers.view_expense_handler import (
    view_expenses, handle_expense_period, handle_specific_month as handle_expense_specific_month,
    handle_specific_year as handle_expense_specific_year
)
from src.handlers.view_income_handler import (
    view_incomes, handle_income_period, handle_specific_month as handle_income_specific_month,
    handle_specific_year as handle_income_specific_year
)

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
        '/ver_despesas - Visualizar despesas\n'
        '/ver_receitas - Visualizar receitas\n'
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
            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, income_description)],
            CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, income_category)],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, income_date)],
            VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, income_value)],
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

    # Handler para visualizar despesas
    view_expense_handler = ConversationHandler(
        entry_points=[CommandHandler("ver_despesas", view_expenses)],
        states={
            VIEW_EXPENSE_MONTH: [
                CallbackQueryHandler(handle_expense_period),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_expense_specific_month)
            ],
            VIEW_EXPENSE_YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_expense_specific_year)],
        },
        fallbacks=[CommandHandler("start", start)],
        name="view_expense",
        persistent=False
    )
    application.add_handler(view_expense_handler)

    # Handler para visualizar receitas
    view_income_handler = ConversationHandler(
        entry_points=[CommandHandler("ver_receitas", view_incomes)],
        states={
            VIEW_INCOME_MONTH: [
                CallbackQueryHandler(handle_income_period),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_income_specific_month)
            ],
            VIEW_INCOME_YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_income_specific_year)],
        },
        fallbacks=[CommandHandler("start", start)],
        name="view_income",
        persistent=False
    )
    application.add_handler(view_income_handler)

    # Inicia o bot
    application.run_polling()

if __name__ == '__main__':
    main() 