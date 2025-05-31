from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from datetime import datetime
import logging
from src.services.expense_service import get_expenses_by_month, get_expenses_by_year
from src.utils.config import VIEW_EXPENSE_MONTH, VIEW_EXPENSE_YEAR

logger = logging.getLogger(__name__)

async def view_expenses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia o processo de visualização de despesas."""
    logger.info("Iniciando visualização de despesas")
    keyboard = [
        [
            InlineKeyboardButton("Este Mês", callback_data="expense_this_month"),
            InlineKeyboardButton("Mês Específico", callback_data="expense_specific_month")
        ],
        [
            InlineKeyboardButton("Este Ano", callback_data="expense_this_year"),
            InlineKeyboardButton("Ano Específico", callback_data="expense_specific_year")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Como você gostaria de visualizar suas despesas?",
        reply_markup=reply_markup
    )
    return VIEW_EXPENSE_MONTH

async def handle_expense_period(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lida com a seleção do período para visualização de despesas."""
    query = update.callback_query
    logger.info(f"Callback recebido: {query.data}")
    
    if not query:
        logger.error("Nenhum callback recebido")
        return ConversationHandler.END
    
    await query.answer()
    
    user_id = query.from_user.id
    current_date = datetime.now()
    
    try:
        if query.data == "expense_this_month":
            logger.info(f"Buscando despesas do mês atual para usuário {user_id}")
            expenses = get_expenses_by_month(user_id, current_date.month, current_date.year)
            await query.edit_message_text(
                f"Despesas de {current_date.strftime('%B/%Y')}:\n\n" + format_expenses(expenses)
            )
            return ConversationHandler.END
        
        elif query.data == "expense_this_year":
            logger.info(f"Buscando despesas do ano atual para usuário {user_id}")
            expenses = get_expenses_by_year(user_id, current_date.year)
            await query.edit_message_text(
                f"Despesas de {current_date.year}:\n\n" + format_expenses(expenses)
            )
            return ConversationHandler.END
        
        elif query.data == "expense_specific_month":
            logger.info("Solicitando mês específico")
            await query.edit_message_text(
                "Por favor, digite o mês e ano no formato MM/AAAA (ex: 03/2024)"
            )
            return VIEW_EXPENSE_MONTH
        
        elif query.data == "expense_specific_year":
            logger.info("Solicitando ano específico")
            await query.edit_message_text(
                "Por favor, digite o ano (ex: 2024)"
            )
            return VIEW_EXPENSE_YEAR
    except Exception as e:
        logger.error(f"Erro ao processar callback: {e}")
        await query.edit_message_text("Desculpe, ocorreu um erro ao processar sua solicitação.")
        return ConversationHandler.END

async def handle_specific_month(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lida com a entrada de um mês específico."""
    logger.info(f"Recebido mês específico: {update.message.text}")
    try:
        month, year = map(int, update.message.text.split('/'))
        expenses = get_expenses_by_month(update.effective_user.id, month, year)
        await update.message.reply_text(
            f"Despesas de {datetime(year, month, 1).strftime('%B/%Y')}:\n\n" + format_expenses(expenses)
        )
        return ConversationHandler.END
    except ValueError:
        logger.error(f"Formato inválido recebido: {update.message.text}")
        await update.message.reply_text(
            "Formato inválido. Por favor, use o formato MM/AAAA (ex: 03/2024)"
        )
        return VIEW_EXPENSE_MONTH

async def handle_specific_year(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lida com a entrada de um ano específico."""
    logger.info(f"Recebido ano específico: {update.message.text}")
    try:
        year = int(update.message.text)
        expenses = get_expenses_by_year(update.effective_user.id, year)
        await update.message.reply_text(
            f"Despesas de {year}:\n\n" + format_expenses(expenses)
        )
        return ConversationHandler.END
    except ValueError:
        logger.error(f"Ano inválido recebido: {update.message.text}")
        await update.message.reply_text(
            "Por favor, digite um ano válido (ex: 2024)"
        )
        return VIEW_EXPENSE_YEAR

def format_expenses(expenses):
    """Formata a lista de despesas para exibição."""
    if not expenses:
        return "Nenhuma despesa encontrada para o período selecionado."
    
    formatted_expenses = []
    total = 0
    
    for expense in expenses:
        formatted_expense = [
            f"📝 {expense['description']}",
            f"💰 R$ {expense['value']:.2f}"
        ]
        
        if expense['installments'] and expense['amount_installment']:
            formatted_expense.append(f"💳 {expense['installments']}x de R$ {expense['amount_installment']:.2f}")
        
        formatted_expense.extend([
            f"📅 {expense['date']}",
            f"🏷️ {expense['category']}"
        ])
        
        formatted_expenses.append("\n".join(formatted_expense))
        total += expense['value']
    
    formatted_expenses.append(f"\n💰 Total: R$ {total:.2f}")
    return "\n\n".join(formatted_expenses) 