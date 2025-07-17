import time
import sys
import os
from tqdm import tqdm

import database
import scraper

def process_tasks(filtro: int):
    """Busca e processa tarefas para um filtro específico."""
    print(f"\n--- Iniciando processamento para o Filtro {filtro} ---")
    
    tasks = database.fetch_pending_tasks(filtro)
    if not tasks:
        print("Nenhuma tarefa encontrada para este filtro.")
        return # Retorna para o loop principal tentar o próximo filtro

    print(f"Encontradas {len(tasks)} tarefas. Processando...")
    
    web_scraper = scraper.Scraper()
    try:
        for task in tqdm(tasks, desc=f"Filtro {filtro}"):
            cod_pesquisa = task['Cod_Pesquisa']
            
            # Determina o valor a ser pesquisado com base no filtro
            if filtro == 0:
                search_value = task['CPF']
                search_type = 'CPF'
            elif filtro == 2:
                search_value = task['Nome']
                search_type = 'NOME'
            else: # Filtro 1 e 3 usam RG
                search_value = task['RG']
                search_type = 'RG'
            
            if not search_value:
                continue

            page_html = web_scraper.perform_search(search_type, search_value)
            result_code = web_scraper.analyze_result(page_html)
            database.save_result(cod_pesquisa, result_code)

    finally:
        web_scraper.close()

def main_loop():
    """Loop principal que cicla entre os filtros."""
    current_filter = 0
    while True:
        process_tasks(current_filter)
        
        current_filter = (current_filter + 1) % 4 # Cicla de 0 a 3
        
        print(f"Processamento do filtro {current_filter-1 if current_filter > 0 else 3} concluído. Aguardando 10 segundos para o próximo ciclo...")
        time.sleep(10) # Pausa entre os filtros

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\nProcesso interrompido pelo usuário. Saindo...")
        sys.exit(0)