from fastapi import APIRouter
from series_service import Series_service
from pydantic import BaseModel
from schemas import SerieUpdate

router = APIRouter(prefix="/series")
repo = Series_service()

def montar_update_query(tabela: str, chave_primaria: str, dados: dict):
    campos = []
    valores = []
    for coluna, valor in dados.items():
        campos.append(f"{coluna} = %s")
        valores.append(valor)
    valores.append(dados[chave_primaria])  # valor para WHERE
    query = f"UPDATE {tabela} SET {', '.join(campos)} WHERE {chave_primaria} = %s"
    return query, valores


class SerieRequest(BaseModel):
    titulo: str
    descricao: str
    ano_lancamento: int
    id_categoria: str
    idautor: int

@router.post("/")
def criar_serie(serie: SerieRequest):
    return repo.criar_serie(
        serie.titulo,
        serie.descricao,
        serie.ano_lancamento,
        serie.id_categoria,
        serie.idautor
    )

# PUT atualizar série
@router.put("/serie/")
def atualizar_serie(dados: SerieUpdate): 
    return repo.atualizar_serie(dados)

@router.get("/")
def listar_series():
    resultado, erro = repo.executar_select("SELECT * FROM serie")
    return erro if erro else resultado


@router.delete("/serie/{id_serie}")
def deletar_serie(id_serie: int):
    return repo.deletar_serie(id_serie)