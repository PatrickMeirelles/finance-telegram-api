import logging
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Usuário {update.effective_user.id} iniciou o bot")
    await update.message.reply_text(
        'Olá! Sou seu assistente financeiro.\n\n'
        'Comandos disponíveis:\n'
        '/despesa - Adicionar uma nova despesa\n'
        '/receita - Adicionar uma nova receita\n'
        '/categorias - Ver suas categorias\n\n'
        'Caso precise de ajuda, use /help'
    )
    return ConversationHandler.END

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '📝 Como usar o bot:\n\n'
        '1. Para adicionar uma despesa:\n'
        '   • Use /despesa\n'
        '   • Siga as instruções para preencher os dados\n\n'
        '2. Para adicionar uma receita:\n'
        '   • Use /receita\n'
        '   • Siga as instruções para preencher os dados\n\n'
        '3. Para gerenciar categorias:\n'
        '   • Use /categorias para ver suas categorias\n'
        '   • Use /nova_categoria para adicionar uma categoria\n\n'
        'Exemplos de valores:\n'
        '• 120\n'
        '• 120,00\n'
        '• 120.00'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Usuário {update.effective_user.id} enviou mensagem: {update.message.text}")
    await update.message.reply_text(
        "Use /start para ver as instruções ou /despesa para adicionar uma nova despesa."
    ) 