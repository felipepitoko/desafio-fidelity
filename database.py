import psycopg2
import sys
from psycopg2.extras import DictCursor
from config import * # Importa configurações de um arquivo central

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        sys.exit(1)

def fetch_pending_tasks(filtro: int, limit: int = 210):
    """
    Busca tarefas pendentes no banco de dados com base em um filtro.
    Retorna uma lista de dicionários.
    """
    # Note: Query corrected to join 'estado' to filter by UF, and removed non-existent 'Data_Nascimento'.
    # Using parameterized queries for all inputs, including LIMIT, is a security best practice.
    sql = """
        SELECT
            p.cod_pesquisa,
            p.nome,
            p.cpf,
            p.rg
        FROM
            pesquisa p
        INNER JOIN
            estado e ON p.cod_uf = e.Cod_UF
        LEFT JOIN
            pesquisa_spv ps ON p.cod_pesquisa = ps.Cod_Pesquisa
        WHERE
            p.data_conclusao IS NULL
            AND ps.resultado IS NULL
            AND e.UF = 'SP'
    """

    # Append filter-specific conditions
    if filtro == 0:
        sql += " AND p.cpf IS NOT NULL AND p.cpf <> ''"
    elif filtro in [1, 3]:
        sql += " AND p.rg IS NOT NULL AND p.rg <> ''"

    sql += " ORDER BY p.data_entrada ASC LIMIT %s"

    tasks = []
    print(sql)
    try:
        # Use 'with' for automatic connection and cursor closing, preventing resource leaks.
        with get_db_connection() as conn:
            # Use DictCursor to get results as dictionary-like objects.
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(sql, (limit,))
                # Convert list of DictRow objects to a list of plain dicts for maximum compatibility.
                tasks = [dict(row) for row in cursor.fetchall()]
    except psycopg2.Error as e:
        print(f"Database error in fetch_pending_tasks: {e}")
        # Return an empty list on error to prevent crashes downstream.
        return []

    return tasks

def save_result(cod_pesquisa: int, resultado: int):
    """Salva o resultado de uma pesquisa no banco de dados."""
    # Note: Corrected parameter style from '?' to '%s' for psycopg2.
    sql = "INSERT INTO pesquisa_spv (Cod_Pesquisa, resultado) VALUES (%s, %s)"
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (cod_pesquisa, resultado))
                # The transaction is committed automatically when the 'with conn:' block exits without error.
    except psycopg2.Error as e:
        print(f"Database error in save_result: {e}")

if __name__ == "__main__":
    print("--- Testing database module ---")
    print("\nTesting fetch_pending_tasks(filtro=0):")
    pending_tasks = fetch_pending_tasks(filtro=0, limit=5)
    if pending_tasks:
        for task in pending_tasks:
            print(task)
    else:
        print("No pending tasks found or an error occurred.")