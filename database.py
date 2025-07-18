import psycopg2
import sys
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
    """Busca tarefas pendentes no banco de dados com base em um filtro."""    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True) # Retorna resultados como dicionários
    
    # A query base é a mesma, mas os joins e wheres mudam com o filtro
    # Esta lógica pode ser melhorada para evitar repetição de código
    query = f"""
        SELECT 
            p.Cod_Pesquisa, p.Nome, p.CPF, p.RG, p.Data_Nascimento 
        FROM 
            pesquisa p 
        LEFT JOIN 
            pesquisa_spv ps ON p.Cod_Pesquisa = ps.Cod_Pesquisa 
        WHERE 
            p.Data_Conclusao IS NULL AND ps.resultado IS NULL AND p.UF = 'SP'
    """
    
    if filtro == 0:
        query += " AND p.CPF IS NOT NULL AND p.CPF != ''"
    elif filtro in [1, 3]:
        query += " AND p.RG IS NOT NULL AND p.RG != ''"
    
    query += f" LIMIT {limit}"
    
    cursor.execute(query)
    tasks = cursor.fetchall()
    
    cursor.close()    
    return tasks

def save_result(cod_pesquisa: int, resultado: int):
    """Salva o resultado de uma pesquisa no banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pesquisa_spv (Cod_Pesquisa, resultado) VALUES (?, ?)", (cod_pesquisa, resultado))
    conn.commit()
    cursor.close()    
    
if __name__ == "__main__":
    # Exemplo de uso
    print(get_db_connection())