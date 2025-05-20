from fastapi import APIRouter, HTTPException, Body
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