import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from src.utils.config import DESCRIPTION, CATEGORY, DATE, VALUE, NEW_CATEGORY
from src.services.database import get_user_categories, add_category, save_transaction

logger = logging.getLogger(__name__)

async def add_income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Usuário {update.effective_user.id} iniciou adição de receita")
    context.user_data['user_id'] = update.effective_user.id
    context.user_data['tipo_operacao'] = 'receita'
    await update.message.reply_text(
        'Vamos adicionar uma receita.\n\n'
        'Digite a descrição da receita:\n'
        'Exemplo: Salário'
    )
    return DESCRIPTION

async def description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Usuário {update.effective_user.id} informou descrição: {update.message.text}")
    context.user_data['descricao'] = update.message.text
    
    user_id = update.effective_user.id
    categories = await get_user_categories(user_id)
    
    if not categories:
        await update.message.reply_text(
            'Você ainda não tem categorias cadastradas.\n'
            'Use /nova_categoria para adicionar uma categoria e depois tente novamente.'
        )
        return ConversationHandler.END
    
    categories_text = '\n'.join([f'• {cat}' for cat in categories])
    await update.message.reply_text(
        'Digite a categoria da receita:\n\n'
        f'{categories_text}\n\n'
        'Se precisar adicionar uma nova categoria, use /nova_categoria'
    )
    return CATEGORY

async def category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = update.message.text.strip()
    user_id = update.effective_user.id
    categories = await get_user_categories(user_id)
    
    if not categories:
        if await add_category(user_id, category):
            context.user_data['categoria'] = category
            await update.message.reply_text(
                f'✅ Categoria "{category}" adicionada com sucesso!\n\n'
                'Digite a data da receita (formato: DD/MM/AAAA):\n'
                'Exemplo: 31/05/2024'
            )
            return DATE
        else:
            await update.message.reply_text(
                '❌ Erro ao adicionar categoria. Por favor, tente novamente.'
            )
            return CATEGORY
    
    if category.lower() == '/nova_categoria':
        await update.message.reply_text(
            'Digite o nome da nova categoria:'
        )
        return NEW_CATEGORY
    
    if category not in categories:
        categories_text = '\n'.join([f'• {cat}' for cat in categories])
        await update.message.reply_text(
            f'Categoria "{category}" não encontrada.\n\n'
            'Suas categorias atuais:\n' +
            categories_text + '\n\n'
            'Digite /nova_categoria para adicionar uma nova categoria.'
        )
        return CATEGORY
    
    logger.info(f"Usuário {user_id} informou categoria: {category}")
    context.user_data['categoria'] = category
    await update.message.reply_text(
        'Digite a data da receita (formato: DD/MM/AAAA):\n'
        'Exemplo: 31/05/2024'
    )
    return DATE

async def date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        date = datetime.strptime(update.message.text, '%d/%m/%Y')
        context.user_data['data'] = date.strftime('%d/%m/%Y')
        logger.info(f"Usuário {update.effective_user.id} informou data: {update.message.text}")
        await update.message.reply_text(
            'Digite o valor total:\n'
            'Exemplo: 120 ou 120,00'
        )
        return VALUE
    except ValueError:
        logger.warning(f"Usuário {update.effective_user.id} informou data inválida: {update.message.text}")
        await update.message.reply_text(
            'Data inválida. Por favor, use o formato DD/MM/AAAA:\n'
            'Exemplo: 31/05/2024'
        )
        return DATE

async def value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value_text = update.message.text.strip().replace(',', '.')
        
        try:
            total_value = float(value_text)
        except ValueError:
            await update.message.reply_text(
                'Por favor, digite um número válido:\n'
                'Exemplos: 120 ou 120,00'
            )
            return VALUE
        
        if total_value <= 0:
            await update.message.reply_text(
                'O valor deve ser maior que zero. Por favor, digite um valor válido:'
            )
            return VALUE
            
        context.user_data['valor_total'] = total_value
        logger.info(f"Usuário {update.effective_user.id} informou valor: {total_value}")

        if await save_transaction(update.effective_user.id, context.user_data, is_expense=False):
            await update.message.reply_text(
                '✅ Receita registrada com sucesso!\n\n'
                'Para adicionar outra receita, use o comando /receita\n'
                'Para ver as instruções novamente, use /start'
            )
        else:
            await update.message.reply_text(
                '❌ Erro ao salvar receita. Por favor, tente novamente.'
            )
        
        return ConversationHandler.END

    except Exception as e:
        logger.error(f"Erro ao processar valor: {str(e)}")
        await update.message.reply_text(
            'Ocorreu um erro ao processar o valor. Por favor, tente novamente:\n'
            'Exemplos: 120 ou 120,00'
        )
        return VALUE 