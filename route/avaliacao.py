from fastapi import APIRouter, HTTPException, Body
from series_service import Series_service
from pydantic import BaseModel
from schemas import AvaliacaoUpdate

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




@router.post("/avaliacoes/")
def avaliar_serie(id_serie: int, usuario_id: int, nota: int, comentario: str):
    return repo.executar_sql("INSERT INTO avaliacao (id_serie, usuario_id, nota, comentario) VALUES (%s, %s, %s, %s)",
                             (id_serie, usuario_id, nota, comentario))


@router.put("/avaliacao/")
def atualizar_avaliacao(dados: AvaliacaoUpdate):
    return repo.atualizar_avaliacao(dados)

@router.get("/avaliacoes/")
def listar_avaliacoes():
    query = "SELECT * FROM avaliacao"
    resultados, erro = repo.executar_consulta(query)
    if erro:
        raise HTTPException(status_code=500, detail=erro)
    return resultados

@router.delete("/avaliacao/{id_avaliacao}")
def deletar_avaliacao(id_avaliacao: int):
    return repo.deletar_avaliacao(id_avaliacao)
