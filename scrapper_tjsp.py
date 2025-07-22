import time, os , re, logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ScraperTJSP:
    def __init__(self, dados_pesquisa: dict = None, filtro:int = None):
        self.dados_pesquisa = dados_pesquisa
        self.filtro = filtro
        self.driver = self.iniciar_driver()
        self.consulta_concluida:bool = False
        self.resultado_consulta:str = None

    def iniciar_driver(self):
        """Inicializa e retorna uma instância do WebDriver."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox") # Necessário para rodar como root em ambientes linux
        chrome_options.add_argument("--disable-dev-shm-usage") # Evita problemas de memória compartilhada
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--log-level=3')
                
        try:
            # O Selenium irá encontrar o chromedriver instalado no PATH do contêiner ou da máquina.
            driver = webdriver.Chrome(options=chrome_options)
            return driver
        except Exception as e:
            logging.error(f"Erro fatal ao iniciar o driver do Chrome: {e}")
            raise  # Re-raise as the application cannot continue without a driver.

    def open_website(self, url: str):
        """
        Navega para uma URL específica.
        """
        if self.driver:
            self.driver.get(url)

    def wait(self, seconds: int):
        """
        Pausa a execução pelo número de segundos especificado.
        """
        time.sleep(seconds)

    def close(self):
        """Fecha o driver do navegador."""
        if self.driver:
            logging.info("Fechando o navegador.")
            self.driver.quit()
            
    def select_document_type(self):
        """Seleciona o tipo de documento (Nome, CPF, RG) no formulário de busca."""
        try:
            select_element = self.driver.find_element(By.CSS_SELECTOR, "#cbPesquisa")
            select = Select(select_element)

            if self.filtro == 1:
                select.select_by_value("NMPARTE")
            elif self.filtro in [2,3]:
                select.select_by_value("DOCPARTE")

        except NoSuchElementException:
            # This is a critical error; the page structure might have changed.
            logging.error("Não foi possível encontrar o elemento select '#cbPesquisa'. A página pode ter mudado.")
            raise  # Re-raise to stop processing this task.
        except Exception as e:
            # Catch any other unexpected errors.
            logging.error(f"Erro inesperado ao selecionar o tipo de documento: {e}")
            raise
            
    def send_and_search_personal_data(self):
        """Preenche o formulário com os dados da pesquisa e clica no botão de busca."""
        try:
            documento = None
            if self.filtro == 1:
                personal_data_field = self.driver.find_element(By.CSS_SELECTOR, "#campo_NMPARTE")
                complete_name_checkbox = self.driver.find_element(By.CSS_SELECTOR, "#pesquisarPorNomeCompleto")
                complete_name_checkbox.click()
                documento = self.dados_pesquisa.get('nome_consultado')
                personal_data_field.send_keys(documento)
            elif self.filtro == 2:
                personal_data_field = self.driver.find_element(By.CSS_SELECTOR, "#campo_DOCPARTE")
                documento = self.dados_pesquisa.get('cpf_consultado')
                personal_data_field.send_keys(documento)
            elif self.filtro == 3:
                personal_data_field = self.driver.find_element(By.CSS_SELECTOR, "#campo_DOCPARTE")
                documento = self.dados_pesquisa.get('rg_consultado')
                personal_data_field.send_keys(documento)
                
            search_button = self.driver.find_element(By.CSS_SELECTOR, "#botaoConsultarProcessos")
            search_button.click()

        except NoSuchElementException:
            logging.error("Não foi possível encontrar um dos campos de busca ou o botão de consulta. A página pode ter mudado.")
            raise
        except Exception as e:
            logging.error(f"Erro inesperado ao preencher e enviar dados pessoais: {e}")
            raise
            
    def check_response(self):
        """
        Analisa a página de resultados e atualiza o estado do scraper.
        Retorna True se um resultado definitivo foi encontrado, False caso contrário.
        """
        try:
            page_source = self.driver.page_source

            if "Não existem informações disponíveis para os parâmetros informados" in page_source:
                self.resultado_consulta = "Nada consta."
                self.consulta_concluida = True
                logging.info("Resultado da consulta: Nada consta.")
                return True

            # Tenta encontrar o contador de processos.
            try:
                contador_processos_span = self.driver.find_element(By.CSS_SELECTOR, "#contadorDeProcessos")
                contador_processos_text = contador_processos_span.text
                numero_processos = int(re.sub(r'\D', '', contador_processos_text))
                
                if numero_processos > 0:
                    self.resultado_consulta = f"Processos encontrados: {numero_processos}"
                    self.consulta_concluida = True
                    logging.info(f"Resultado da consulta: {self.resultado_consulta}")
                    return True
            except NoSuchElementException:
                # Se o contador não for encontrado, pode ser uma página de erro ou um estado inesperado.
                logging.warning("Página de resultado em formato inesperado: nem 'nada consta' nem contador de processos encontrado.")
                self.resultado_consulta = "Página em formato desconhecido."
                self.consulta_concluida = False
                return False

        except Exception as e:
            logging.error(f"Erro inesperado ao verificar a resposta: {e}")
            self.resultado_consulta = f"Erro ao processar resultado: {e}"
            self.consulta_concluida = False
        return False
    
    def executar_pesquisa(self)->tuple[bool,str]:
        try:
            self.open_website("https://esaj.tjsp.jus.br/cpopg/open.do")
            self.select_document_type()
            self.send_and_search_personal_data()
            self.wait(2)
            self.check_response()
            return self.consulta_concluida, self.resultado_consulta

        except Exception as e:
            logging.error(f"Uma exceção não tratada ocorreu durante a execução da pesquisa: {e}")
            return False, f"Erro crítico no scraper: {e}"
            
if __name__ == '__main__':
    # Exemplo de uso: abre o site, espera 5 segundos e fecha.
    scraper = ScraperTJSP(dados_pesquisa={
        'cpf_consultado': '11122233344',
        'nome_consultado': 'Felipe Sousa da Costa'
        }, filtro=1)
    