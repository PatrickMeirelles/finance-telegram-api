import os
import logging
from datetime import datetime, timedelta, date
import asyncpg
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

async def get_connection():
    try:
        conn = await asyncpg.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            host=os.getenv('DB_HOST')
        )
        return conn
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco de dados: {str(e)}")
        raise

async def get_user_categories(user_id):
    try:
        conn = await get_connection()
        categories = await conn.fetch(
            'SELECT description FROM categories WHERE "user" = $1',
            str(user_id)
        )
        await conn.close()
        return [row['description'] for row in categories]
    except Exception as e:
        logger.error(f"Erro ao buscar categorias: {str(e)}")
        return []

async def add_category(user_id, category):
    try:
        conn = await get_connection()
        await conn.execute(
            'INSERT INTO categories ("user", description) VALUES ($1, $2)',
            str(user_id), category
        )
        await conn.close()
        return True
    except Exception as e:
        logger.error(f"Erro ao adicionar categoria: {str(e)}")
        return False

async def save_transaction(user_id, data, is_expense=True):
    try:
        conn = await get_connection()
        
        # Primeiro, vamos buscar o ID da categoria
        category_id = await conn.fetchval(
            'SELECT id FROM categories WHERE "user" = $1 AND description = $2',
            str(user_id), data['categoria']
        )
        
        if not category_id:
            # Se a categoria não existir, vamos criá-la
            category_id = await conn.fetchval(
                'INSERT INTO categories ("user", description) VALUES ($1, $2) RETURNING id',
                str(user_id), data['categoria']
            )
        
        # Converter a data do formato DD/MM/YYYY para um objeto date
        transaction_date = datetime.strptime(data['data'], '%d/%m/%Y').date()
        
        if is_expense and data.get('metodo_pagamento', '').lower() == 'crédito':
            installments = data['parcelas']
            total_value = round(data['valor_total'], 2)
            installment_value = round(total_value / installments, 2)
            
            # Ajusta o valor total para garantir que a soma das parcelas seja igual ao valor total
            adjusted_value = installment_value * installments
            difference = total_value - adjusted_value
            
            for i in range(installments):
                installment_date = datetime.strptime(data['data'], '%d/%m/%Y')
                # Calcula o novo mês e ano
                new_month = installment_date.month + i
                new_year = installment_date.year + (new_month - 1) // 12
                new_month = ((new_month - 1) % 12) + 1
                
                # Ajusta o dia para o último dia do mês se necessário
                if new_month == 12:
                    last_day = 31
                else:
                    last_day = (installment_date.replace(year=new_year, month=new_month + 1, day=1) - timedelta(days=1)).day
                
                new_day = min(installment_date.day, last_day)
                installment_date = installment_date.replace(year=new_year, month=new_month, day=new_day)
                
                # Ajusta o valor da última parcela para compensar a diferença de arredondamento
                final_value = installment_value
                if i == installments - 1 and difference != 0:
                    final_value = round(installment_value + difference, 2)
                
                await conn.execute(
                    '''
                    INSERT INTO transactions 
                    ("user", description, category_id, date, type_id, installments, total_amount, amount_installment, is_expense)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                    ''',
                    str(user_id),
                    data['descricao'],
                    category_id,
                    installment_date.date(),
                    1,  # type_id para crédito
                    f'{i+1}/{installments}',
                    total_value,
                    final_value,
                    True
                )
        else:
            await conn.execute(
                '''
                INSERT INTO transactions 
                ("user", description, category_id, date, type_id, installments, total_amount, amount_installment, is_expense)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                ''',
                str(user_id),
                data['descricao'],
                category_id,
                transaction_date,
                2 if is_expense else 3,  # type_id para débito (2) ou receita (3)
                '1/1',
                round(data['valor_total'], 2),
                round(data['valor_total'], 2),
                is_expense
            )
        
        await conn.close()
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar transação: {str(e)}")
        return False 