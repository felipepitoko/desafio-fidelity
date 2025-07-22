import time
import os
import requests
import logging
from concurrent.futures import ThreadPoolExecutor

from scrapper_tjsp import ScraperTJSP
from config import *

# --- Configuração do Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [WORKER] - %(message)s',
    handlers=[
        logging.FileHandler("worker.log"),   # Salva logs no arquivo worker.log
        logging.StreamHandler()           # Mostra logs no console
    ]
)

def get_enrichment_types():
    """Busca os tipos de enriquecimento disponíveis na API."""
    try:
        response = requests.get(f"{API_URL}/tipos-enriquecimento/")
        if response.status_code == 200:          
            return response.json()

        # Se não houver tipos, a API retorna 404, o que é esperado.
        elif response.status_code == 404:
            logging.info("Nenhum tipo de enriquecimento encontrado para processar.")
            return []

    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao conectar com a API para buscar tipos: {e}")

    return []

def get_pending_tasks(cod_tipo_enriquecimento: int):
    """Busca tarefas pendentes para um tipo de enriquecimento específico."""
    try:
        url = f"{API_URL}/pesquisas/pendentes/{cod_tipo_enriquecimento}"
        response = requests.get(url)         
        if response.status_code == 200:
            return response.json()

        elif response.status_code == 404:
            # Este é um caso normal, apenas significa que não há tarefas para este tipo.
            return []

    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao conectar com a API para buscar tarefas: {e}")

    return []

def log_result(payload:dict):
    """Envia o resultado do processamento para a API."""
    try:
        response = requests.post(f"{API_URL}/logs/", json=payload)
        if response.status_code == 201:
            logging.info(f"Resultado da pesquisa {payload['cod_pesquisa']} logado com sucesso.")
        else:
            logging.error(f"Falha ao logar resultado para a pesquisa {payload['cod_pesquisa']}: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao conectar com a API para logar resultado: {e}")

def process_task(task:dict, cod_tipo_enriquecimento:int):
    """
    Função alvo para cada thread. Executa uma única tarefa de scraping.
    Cada thread terá sua própria instância do Scraper e do WebDriver.
    """
    logging.info(f"Iniciando processamento da tarefa {task['cod_pesquisa']} em uma nova thread.")
    
    filtro_map = {'NOME': 1, 'CPF': 2, 'RG': 3}
    filtro_desc = next((key for key in filtro_map if key in task['descricao_filtro'].upper()), None)
    filtro_id = filtro_map.get(filtro_desc)

    if filtro_id is None:
        log_result({"cod_pesquisa": task['cod_pesquisa'], "cod_tipo_enriquecimento": cod_tipo_enriquecimento, "status_enriquecimento": "Erro de Configuração", "enriquecimento_concluido": False, "resultado_enriquecimento": "Tipo de filtro desconhecido na tarefa."})
        return

    scraper = ScraperTJSP(dados_pesquisa=task, filtro=filtro_id)
    try:
        sucesso, resultado = scraper.executar_pesquisa()
        log_payload = {"cod_pesquisa": task['cod_pesquisa'], "cod_tipo_enriquecimento": cod_tipo_enriquecimento, "status_enriquecimento": "Processado", "enriquecimento_concluido": sucesso, "resultado_enriquecimento": resultado}
        log_result(log_payload)

    except Exception as e:
        logging.error(f"Erro não tratado ao processar a tarefa {task['cod_pesquisa']}: {e}")
        log_result({"cod_pesquisa": task['cod_pesquisa'], "cod_tipo_enriquecimento": cod_tipo_enriquecimento, "status_enriquecimento": "Erro Crítico no Worker", "enriquecimento_concluido": False, "resultado_enriquecimento": str(e)})
    finally:
        # Garante que o navegador seja sempre fechado, mesmo em caso de erro.
        scraper.close()
        
def wait_for_api(max_retries=12, retry_delay=5):
    """Aguarda a API ficar disponível, verificando o endpoint de health check."""
    logging.info("Aguardando a API ficar disponível...")
    for attempt in range(max_retries):
        try:
            response = requests.get(f"{API_URL}/health-check/")
            if response.status_code == 200:
                logging.info("API está pronta e respondendo.")
                return True
        except requests.exceptions.RequestException:
            logging.warning(f"Tentativa {attempt + 1}/{max_retries}: Não foi possível conectar à API. Tentando novamente em {retry_delay}s.")
        
        time.sleep(retry_delay)
    
    logging.error(f"A API não ficou disponível após {max_retries} tentativas. Encerrando o worker.")
    return False

def main():
    """Loop principal do worker."""
    if not wait_for_api():
        return  # Encerra o script se a API não estiver disponível.
    
    while True:
        logging.info("--- Iniciando novo ciclo de processamento ---")
        enrichment_types = get_enrichment_types()

        if not enrichment_types:
            logging.info("Nenhum tipo de enriquecimento configurado. Aguardando...")

        else:
            for etype in enrichment_types:
                cod_tipo = etype['cod_tipo_enriquecimento']
                logging.info(f"Verificando tarefas para o tipo: '{etype['descricao_enriquecimento']}' (ID: {cod_tipo})")
                tasks = get_pending_tasks(cod_tipo)                
                if not tasks:
                    logging.info("Nenhuma tarefa pendente encontrada para este filtro.")
                    continue
                logging.info(f"Encontradas {len(tasks)} tarefas. Submetendo ao pool de {MAX_WORKERS} threads...")
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    # Submete cada tarefa para ser executada em uma thread separada
                    executor.map(process_task, tasks, [cod_tipo] * len(tasks))
                logging.info(f"Lote de tarefas para o tipo '{etype['descricao_enriquecimento']}' concluído.")
        logging.info(f"Ciclo completo. Aguardando {PROCESS_INTERVAL_SECONDS} segundos...")
        time.sleep(PROCESS_INTERVAL_SECONDS)
        
if __name__ == "__main__":    
    main()
