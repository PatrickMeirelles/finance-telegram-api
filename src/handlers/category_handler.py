import logging
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from src.utils.config import NEW_CATEGORY
from src.services.google_sheets import get_user_categories, add_category

logger = logging.getLogger(__name__)

async def list_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    categories = await get_user_categories(user_id)
    
    if not categories:
        await update.message.reply_text(
            'Você ainda não tem categorias cadastradas.\n'
            'Use /nova_categoria para adicionar uma categoria.'
        )
    else:
        categories_text = '\n'.join([f'• {cat}' for cat in categories])
        await update.message.reply_text(
            'Suas categorias:\n\n' + categories_text + '\n\n'
            'Use /nova_categoria para adicionar uma nova categoria.'
        )

async def new_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Usuário {update.effective_user.id} iniciou adição de categoria")
    await update.message.reply_text(
        'Digite o nome da nova categoria:'
    )
    return NEW_CATEGORY

async def save_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = update.message.text.strip()
    user_id = update.effective_user.id
    
    if await add_category(user_id, category):
        logger.info(f"Usuário {user_id} adicionou categoria: {category}")
        await update.message.reply_text(
            f'✅ Categoria "{category}" adicionada com sucesso!\n\n'
            'Para adicionar uma despesa, use /despesa\n'
            'Para adicionar uma receita, use /receita'
        )
    else:
        logger.error(f"Erro ao adicionar categoria para usuário {user_id}: {category}")
        await update.message.reply_text(
            '❌ Erro ao adicionar categoria. Por favor, tente novamente.'
        )
    
    return ConversationHandler.END 