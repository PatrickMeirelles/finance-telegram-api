from datetime import datetime
from src.utils.database import get_db_connection
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

def get_expenses_by_month(user_id: int, month: int, year: int) -> List[Dict]:
    """Busca despesas do mês especificado."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT t.id, t.description, t.total_amount, t.date, t.installments, t.amount_installment,
                           c.description as category_name
                    FROM transactions t
                    LEFT JOIN categories c ON t.category_id = c.id
                    WHERE t.user = %s::text
                    AND t.is_expense = true
                    AND EXTRACT(MONTH FROM t.date) = %s
                    AND EXTRACT(YEAR FROM t.date) = %s
                    ORDER BY t.date DESC
                """, (str(user_id), month, year))
                expenses = cur.fetchall()
                return [
                    {
                        'id': expense[0],
                        'description': expense[1],
                        'value': float(expense[2]),
                        'date': expense[3].strftime('%d/%m/%Y'),
                        'installments': expense[4],
                        'amount_installment': float(expense[5]) if expense[5] else None,
                        'category': expense[6]
                    }
                    for expense in expenses
                ]
    except Exception as e:
        logger.error(f"Erro ao buscar despesas do mês: {e}")
        return []

def get_expenses_by_year(user_id: int, year: int) -> List[Dict]:
    """Busca despesas do ano especificado."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT t.id, t.description, t.total_amount, t.date, t.installments, t.amount_installment,
                           c.description as category_name
                    FROM transactions t
                    LEFT JOIN categories c ON t.category_id = c.id
                    WHERE t.user = %s::text
                    AND t.is_expense = true
                    AND EXTRACT(YEAR FROM t.date) = %s
                    ORDER BY t.date DESC
                """, (str(user_id), year))
                expenses = cur.fetchall()
                return [
                    {
                        'id': expense[0],
                        'description': expense[1],
                        'value': float(expense[2]),
                        'date': expense[3].strftime('%d/%m/%Y'),
                        'installments': expense[4],
                        'amount_installment': float(expense[5]) if expense[5] else None,
                        'category': expense[6]
                    }
                    for expense in expenses
                ]
    except Exception as e:
        logger.error(f"Erro ao buscar despesas do ano: {e}")
        return [] 