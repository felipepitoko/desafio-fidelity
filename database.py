import psycopg2
import sys
import logging
from psycopg2.extras import DictCursor
from config import *  # Importa configurações de um arquivo central

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
        logging.error(f"Erro fatal ao conectar ao PostgreSQL: {e}")
        sys.exit(1)

def insert_pesquisa(pesquisa_data: dict):
    """
    Insere uma nova pesquisa no banco de dados a partir de um dicionário.
    Retorna o cod_pesquisa da nova inserção ou None em caso de erro.
    """
    sql = """
        INSERT INTO pesquisa (
            cod_lote, cpf_consultado, nome_consultado, rg_consultado,
            uf_rg, uf_pesquisa, data_nascimento, data_pesquisa
        ) VALUES (
            %(cod_lote)s, %(cpf_consultado)s, %(nome_consultado)s, %(rg_consultado)s,
            %(uf_rg)s, %(uf_pesquisa)s, %(data_nascimento)s, %(data_pesquisa)s
        ) RETURNING cod_pesquisa;
    """
    new_id = None
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, pesquisa_data)
                new_id = cursor.fetchone()[0]
    except psycopg2.Error as e:
        logging.error(f"Database error in insert_pesquisa: {e}")
        return None
    return new_id

def fetch_pending_enrichment_tasks(cod_tipo_enriquecimento: int, limit: int = 100):
    """
    Busca pesquisas que ainda não foram concluídas com sucesso para um tipo de enriquecimento específico.
    Uma tarefa é considerada pendente se não houver um log para ela ou se o log existente
    não estiver marcado como 'enriquecimento_concluido = TRUE'.
    """
    sql = """
        SELECT
            p.cod_pesquisa,
            p.cpf_consultado,
            p.nome_consultado,
            p.rg_consultado,
            t.url_enriquecimento,
            f.descricao_filtro,
            f.referencia_html_filtro
        FROM
            pesquisa p
        JOIN tipo_enriquecimento t ON t.cod_tipo_enriquecimento = %s
        JOIN filtro_enriquecimento f ON t.cod_filtro = f.cod_filtro
        WHERE NOT EXISTS (
            SELECT 1
            FROM log_enriquecimento le
            WHERE le.cod_pesquisa = p.cod_pesquisa
              AND le.cod_tipo_enriquecimento = %s
              AND le.enriquecimento_concluido = TRUE
        )
        ORDER BY p.created_at ASC
        LIMIT %s;
    """
    tasks = []
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(sql, (cod_tipo_enriquecimento, cod_tipo_enriquecimento, limit))
                tasks = [dict(row) for row in cursor.fetchall()]
    except psycopg2.Error as e:
        logging.error(f"Database error in fetch_pending_enrichment_tasks: {e}")
        return []
    return tasks

def fetch_completed_pesquisas(limit: int = 100):
    """
    Busca e retorna todas as pesquisas que possuem pelo menos um log de enriquecimento concluído.
    """
    sql = """
        SELECT DISTINCT p.*
        FROM pesquisa p
        JOIN log_enriquecimento le ON p.cod_pesquisa = le.cod_pesquisa
        WHERE le.enriquecimento_concluido = TRUE
        ORDER BY p.cod_pesquisa DESC
        LIMIT %s;
    """
    pesquisas = []
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(sql, (limit,))
                pesquisas = [dict(row) for row in cursor.fetchall()]
    except psycopg2.Error as e:
        logging.error(f"Database error in fetch_completed_pesquisas: {e}")
        return []
    return pesquisas

def log_enrichment_result(cod_pesquisa: int, cod_tipo_enriquecimento: int, status_enriquecimento: str, enriquecimento_concluido: bool, resultado_enriquecimento: str):
    """
    Insere um novo registro na tabela de log de enriquecimento para cada tentativa.
    """
    sql = """
        INSERT INTO log_enriquecimento (
            cod_pesquisa, cod_tipo_enriquecimento, status_enriquecimento,
            enriquecimento_concluido, resultado_enriquecimento
        ) VALUES (%s, %s, %s, %s, %s);
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (cod_pesquisa, cod_tipo_enriquecimento, status_enriquecimento, enriquecimento_concluido, resultado_enriquecimento))
    except psycopg2.Error as e:
        logging.error(f"Database error in log_enrichment_result: {e}")

def fetch_enrichment_types():
    """
    Busca e retorna todos os tipos de enriquecimento disponíveis no banco de dados.
    """
    sql = "SELECT * FROM tipo_enriquecimento;"
    enrichment_types = []
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(sql)
                enrichment_types = [dict(row) for row in cursor.fetchall()]
    except psycopg2.Error as e:
        logging.error(f"Database error in fetch_enrichment_types: {e}")
        return []
    return enrichment_types


if __name__ == "__main__":
    # Existing tests...
    print("--- Testing database module ---")

    print("\n1. Testing fetch_pending_enrichment_tasks(cod_tipo_enriquecimento=1):")
    pending_tasks = fetch_pending_enrichment_tasks(cod_tipo_enriquecimento=1, limit=5)
    if pending_tasks:
        for task in pending_tasks:
            print(dict(task))
    else:
        print("No pending tasks found for this enrichment type.")

    print("\n2. Testing fetch_completed_pesquisas():")
    # Primeiro, marcamos uma tarefa como concluída para que a função tenha o que encontrar.
    if pending_tasks:
        task_to_complete = pending_tasks[0]
        print(f"Logging a completed result for task {task_to_complete['cod_pesquisa']} to test...")
        log_enrichment_result(task_to_complete['cod_pesquisa'], 1, 'Concluído', True, 'Nada consta.')

    completed_tasks = fetch_completed_pesquisas(limit=5)
    if completed_tasks:
        for task in completed_tasks:
            print(dict(task))
    else:
        print("No completed tasks found.")

    print("\n3. Testing insert_pesquisa():")
    new_pesquisa_data = {
        "cod_lote": 1,
        "cpf_consultado": "12345678901",
        "nome_consultado": "Fulano de Tal",
        "rg_consultado": "123456789",
        "uf_rg": 1,
        "uf_pesquisa": 1,
        "data_nascimento": "2000-01-01",
        "data_pesquisa": "2024-01-01 12:00:00"
    }
    new_id = insert_pesquisa(new_pesquisa_data)
    if new_id:
        print(f"Successfully inserted new pesquisa with cod_pesquisa: {new_id}")
    else:
        print("Failed to insert new pesquisa.")

    print("\n4. Testing fetch_enrichment_types():")
    enrichment_types = fetch_enrichment_types()
    if enrichment_types:
        for et in enrichment_types:
            print(dict(et))
    else:
        print("No enrichment types found.")