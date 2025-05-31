from datetime import datetime
from src.utils.database import get_db_connection
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

def get_incomes_by_month(user_id: int, month: int, year: int) -> List[Dict]:
    """Busca receitas do mês especificado."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT t.id, t.description, t.total_amount, t.date,
                           c.description as category_name
                    FROM transactions t
                    LEFT JOIN categories c ON t.category_id = c.id
                    WHERE t.user = %s::text
                    AND t.is_expense = false
                    AND EXTRACT(MONTH FROM t.date) = %s
                    AND EXTRACT(YEAR FROM t.date) = %s
                    ORDER BY t.date DESC
                """, (str(user_id), month, year))
                incomes = cur.fetchall()
                return [
                    {
                        'id': income[0],
                        'description': income[1],
                        'value': float(income[2]),
                        'date': income[3].strftime('%d/%m/%Y'),
                        'category': income[4]
                    }
                    for income in incomes
                ]
    except Exception as e:
        logger.error(f"Erro ao buscar receitas do mês: {e}")
        return []

def get_incomes_by_year(user_id: int, year: int) -> List[Dict]:
    """Busca receitas do ano especificado."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT t.id, t.description, t.total_amount, t.date,
                           c.description as category_name
                    FROM transactions t
                    LEFT JOIN categories c ON t.category_id = c.id
                    WHERE t.user = %s::text
                    AND t.is_expense = false
                    AND EXTRACT(YEAR FROM t.date) = %s
                    ORDER BY t.date DESC
                """, (str(user_id), year))
                incomes = cur.fetchall()
                return [
                    {
                        'id': income[0],
                        'description': income[1],
                        'value': float(income[2]),
                        'date': income[3].strftime('%d/%m/%Y'),
                        'category': income[4]
                    }
                    for income in incomes
                ]
    except Exception as e:
        logger.error(f"Erro ao buscar receitas do ano: {e}")
        return [] 