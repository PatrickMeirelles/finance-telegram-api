import psycopg2
from src.utils.config import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT

def get_db_connection():
    """Estabelece uma conexão com o banco de dados PostgreSQL."""
    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise 