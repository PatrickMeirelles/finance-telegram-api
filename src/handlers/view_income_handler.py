from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from datetime import datetime
import logging
from src.services.income_service import get_incomes_by_month, get_incomes_by_year
from src.utils.config import VIEW_INCOME_MONTH, VIEW_INCOME_YEAR

logger = logging.getLogger(__name__)

async def view_incomes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia o processo de visualização de receitas."""
    logger.info("Iniciando visualização de receitas")
    keyboard = [
        [
            InlineKeyboardButton("Este Mês", callback_data="income_this_month"),
            InlineKeyboardButton("Mês Específico", callback_data="income_specific_month")
        ],
        [
            InlineKeyboardButton("Este Ano", callback_data="income_this_year"),
            InlineKeyboardButton("Ano Específico", callback_data="income_specific_year")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Como você gostaria de visualizar suas receitas?",
        reply_markup=reply_markup
    )
    logger.info("Retornando estado VIEW_INCOME_MONTH")
    return VIEW_INCOME_MONTH

async def handle_income_period(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lida com a seleção do período para visualização de receitas."""
    query = update.callback_query
    logger.info(f"Callback recebido: {query.data}")
    await query.answer()
    
    user_id = query.from_user.id
    current_date = datetime.now()
    
    if query.data == "income_this_month":
        logger.info(f"Buscando receitas do mês atual para usuário {user_id}")
        incomes = get_incomes_by_month(user_id, current_date.month, current_date.year)
        await query.edit_message_text(
            f"Receitas de {current_date.strftime('%B/%Y')}:\n\n" + format_incomes(incomes)
        )
        return ConversationHandler.END
    
    elif query.data == "income_this_year":
        logger.info(f"Buscando receitas do ano atual para usuário {user_id}")
        incomes = get_incomes_by_year(user_id, current_date.year)
        await query.edit_message_text(
            f"Receitas de {current_date.year}:\n\n" + format_incomes(incomes)
        )
        return ConversationHandler.END
    
    elif query.data == "income_specific_month":
        logger.info("Solicitando mês específico")
        await query.edit_message_text(
            "Por favor, digite o mês e ano no formato MM/AAAA (ex: 03/2024)"
        )
        return VIEW_INCOME_MONTH
    
    elif query.data == "income_specific_year":
        logger.info("Solicitando ano específico")
        await query.edit_message_text(
            "Por favor, digite o ano (ex: 2024)"
        )
        return VIEW_INCOME_YEAR

async def handle_specific_month(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lida com a entrada de um mês específico."""
    logger.info(f"Recebido mês específico: {update.message.text}")
    try:
        month, year = map(int, update.message.text.split('/'))
        incomes = get_incomes_by_month(update.effective_user.id, month, year)
        await update.message.reply_text(
            f"Receitas de {datetime(year, month, 1).strftime('%B/%Y')}:\n\n" + format_incomes(incomes)
        )
        return ConversationHandler.END
    except ValueError:
        logger.error(f"Formato inválido recebido: {update.message.text}")
        await update.message.reply_text(
            "Formato inválido. Por favor, use o formato MM/AAAA (ex: 03/2024)"
        )
        return VIEW_INCOME_MONTH

async def handle_specific_year(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lida com a entrada de um ano específico."""
    logger.info(f"Recebido ano específico: {update.message.text}")
    try:
        year = int(update.message.text)
        incomes = get_incomes_by_year(update.effective_user.id, year)
        await update.message.reply_text(
            f"Receitas de {year}:\n\n" + format_incomes(incomes)
        )
        return ConversationHandler.END
    except ValueError:
        logger.error(f"Ano inválido recebido: {update.message.text}")
        await update.message.reply_text(
            "Por favor, digite um ano válido (ex: 2024)"
        )
        return VIEW_INCOME_YEAR

def format_incomes(incomes):
    """Formata a lista de receitas para exibição."""
    if not incomes:
        return "Nenhuma receita encontrada para o período selecionado."
    
    formatted_incomes = []
    total = 0
    
    for income in incomes:
        formatted_incomes.append(
            f"📝 {income['description']}\n"
            f"💰 R$ {income['value']:.2f}\n"
            f"📅 {income['date']}\n"
            f"🏷️ {income['category']}\n"
        )
        total += income['value']
    
    formatted_incomes.append(f"\n💰 Total: R$ {total:.2f}")
    return "\n".join(formatted_incomes) 