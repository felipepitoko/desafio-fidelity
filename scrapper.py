from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from config import (
    EXECUTAVEL, SITE_URL, NADA_CONSTA, CONSTA01, CONSTA02
)

class Scraper:
    def __init__(self):
        edge_options = Options()
        edge_options.add_argument("--headless")
        edge_options.add_argument("--disable-gpu")
        service = Service(executable_path=EXECUTAVEL)
        self.driver = webdriver.Edge(service=service, options=edge_options)

    def perform_search(self, search_type: str, search_value: str) -> str:
        """
        Navega até o site, realiza a pesquisa e retorna o HTML da página de resultado.
        search_type: 'CPF' ou 'NOME' ou 'RG'
        """
        try:
            self.driver.get(SITE_URL)
            
            # Seleciona o tipo de pesquisa
            select_element = self.driver.find_element(By.ID, "cbPesquisa")
            select = Select(select_element)
            
            if search_type == 'CPF':
                select.select_by_value("CPF")
                field_id = "nuProcesso"
            elif search_type == 'NOME':
                select.select_by_value("NMPARTE")
                field_id = "nuProcesso"
            elif search_type == 'RG':
                select.select_by_value("RG")
                field_id = "nuProcesso"
            else:
                raise ValueError("Tipo de pesquisa inválido")

            # Preenche o campo e clica em consultar
            self.driver.find_element(By.ID, field_id).send_keys(search_value)
            self.driver.find_element(By.ID, "botaoConsultarPrimeiroGrau").click()
            
            # Aguardar o resultado (uma melhoria seria usar WebDriverWait)
            return self.driver.page_source

        except (TimeoutException, NoSuchElementException) as e:
            print(f"Erro durante o scraping para o valor {search_value}: {e}")
            return "" # Retorna string vazia em caso de erro
        
    def analyze_result(self, page_html: str) -> int:
        """Analisa o HTML da página e retorna um código de resultado."""
        if not page_html:
            return 7 # Erro no scraping

        if NADA_CONSTA in page_html:
            return 1  # Nada consta
        
        if CONSTA01 in page_html:
            if CONSTA02 in page_html:
                return 2  # Consta criminal
            return 5  # Consta cível
        
        return 7 # Padrão para resultado não identificado

    def close(self):
        """Fecha o driver do navegador."""
        if self.driver:
            self.driver.quit()