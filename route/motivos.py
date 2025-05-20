from fastapi import APIRouter, HTTPException, Body
from series_service import Series_service
from pydantic import BaseModel
from schemas import MotivoUpdate

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


@router.post("/motivos/")
def cadastrar_motivo_para_assistir(id_serie: int, motivo: str):
    return repo.executar_sql("INSERT INTO motivo_assistir (id_serie, motivo) VALUES (%s, %s)", (id_serie, motivo))


@router.put("/motivo/")
def atualizar_motivo(dados: MotivoUpdate):
    return repo.atualizar_motivo(dados)
    

@router.get("/motivos/")
def listar_motivos():
    query = "SELECT * FROM motivo_assistir"
    resultados, erro = repo.executar_consulta(query)
    if erro:
        raise HTTPException(status_code=500, detail=erro)
    return resultados

@router.delete("/motivo/{id_motivo}")
def deletar_motivo(id_motivo: int):
    return repo.deletar_motivo(id_motivo)
