from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List
from datetime import date, datetime
import logging

# Importa as funções do módulo de banco de dados
import database

# --- Configuração do Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [API] - %(message)s',
    handlers=[
        logging.FileHandler("api.log"),      # Salva logs no arquivo api.log
        logging.StreamHandler()          # Mostra logs no console
    ]
)

# --- Modelos Pydantic (para validação de dados de requisição/resposta) ---

class PesquisaBase(BaseModel):
    cod_lote: int = Field(..., example=1)
    cpf_consultado: str = Field(..., example="11122233344")
    nome_consultado: str = Field(..., example="Jane Doe")
    rg_consultado: str = Field(..., example="123456789")
    uf_rg: int = Field(..., example=1)
    uf_pesquisa: int = Field(..., example=1)
    data_nascimento: date = Field(..., example="1990-01-30")

class PesquisaCreate(PesquisaBase):
    pass

class PesquisaResponse(PesquisaBase):
    cod_pesquisa: int
    data_pesquisa: datetime
    created_at: datetime

    # Updated for Pydantic v2 compatibility
    model_config = {"from_attributes": True}

class PendingTaskResponse(BaseModel):
    cod_pesquisa: int
    cpf_consultado: str
    nome_consultado: str
    rg_consultado: str
    url_enriquecimento: str
    descricao_filtro: str
    referencia_html_filtro: str

    # Updated for Pydantic v2 compatibility
    model_config = {"from_attributes": True}

class EnrichmentTypeResponse(BaseModel):
    cod_tipo_enriquecimento: int
    descricao_enriquecimento: str
    uf_referencia: int
    url_enriquecimento: str
    cod_filtro: int

    # Updated for Pydantic v2 compatibility
    model_config = {"from_attributes": True}

class LogCreate(BaseModel):
    cod_pesquisa: int
    cod_tipo_enriquecimento: int
    status_enriquecimento: str = Field(..., example="Processado")
    enriquecimento_concluido: bool = Field(..., example=True)
    resultado_enriquecimento: str = Field(..., example="Nada consta.")

# --- Instância da Aplicação FastAPI ---

app = FastAPI(
    title="API de Enriquecimento de Pesquisas",
    description="API para gerenciar e consultar o status de pesquisas de enriquecimento de dados.",
    version="1.0.0"
)

# --- Endpoints da API ---

@app.post("/pesquisas/", response_model=PesquisaResponse, status_code=status.HTTP_201_CREATED, tags=["Pesquisas"])
def create_pesquisa(pesquisa: PesquisaCreate):
    """
    Cria um novo registro de pesquisa no banco de dados.
    """
    pesquisa_data = pesquisa.model_dump()
    pesquisa_data['data_pesquisa'] = datetime.now() # Adiciona o timestamp atual
    
    new_id = database.insert_pesquisa(pesquisa_data)
    if new_id is None:
        raise HTTPException(status_code=500, detail="Falha ao inserir a pesquisa no banco de dados.")
    
    # Constrói o objeto de resposta completo
    response_data = {**pesquisa_data, "cod_pesquisa": new_id, "created_at": datetime.now()}
    return response_data

@app.get("/pesquisas/pendentes/{cod_tipo_enriquecimento}", response_model=List[PendingTaskResponse], tags=["Pesquisas"])
def get_pending_tasks(cod_tipo_enriquecimento: int, limit: int = 100):
    """
    Retorna uma lista de pesquisas pendentes para um tipo de enriquecimento específico.
    """
    tasks = database.fetch_pending_enrichment_tasks(cod_tipo_enriquecimento, limit)
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhuma tarefa pendente encontrada para este tipo de enriquecimento.")
    return tasks

@app.get("/pesquisas/concluidas/", response_model=List[PesquisaResponse], tags=["Pesquisas"])
def get_completed_pesquisas(limit: int = 100):
    """
    Retorna uma lista de pesquisas que já foram concluídas (possuem ao menos um log de sucesso).
    """
    pesquisas = database.fetch_completed_pesquisas(limit)
    if not pesquisas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhuma pesquisa concluída encontrada.")
    return pesquisas

@app.get("/tipos-enriquecimento/", response_model=List[EnrichmentTypeResponse], tags=["Tipos de Enriquecimento"])
def get_enrichment_types():
    """
    Retorna uma lista de tipos de enriquecimento disponíveis.
    """
    enrichment_types = database.fetch_enrichment_types()
    if not enrichment_types:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum tipo de enriquecimento encontrado.")
    return enrichment_types

@app.post("/logs/", status_code=status.HTTP_201_CREATED, tags=["Logs"])
def create_log_entry(log: LogCreate):
    """
    Registra o resultado de uma tentativa de enriquecimento no banco de dados.
    Este endpoint é usado pelo worker para salvar os resultados do scraping.
    """
    try:
        database.log_enrichment_result(**log.model_dump())
        return {"message": "Log entry created successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create log entry: {e}")
    
@app.get("/health-check/", status_code=status.HTTP_200_OK, tags=["Health Check"])
def health_check():
    """
    Verifica o status de saúde da API. Usado pelo worker para garantir que a API está pronta.
    """
    return {"status": "ok"}