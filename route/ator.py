from fastapi import APIRouter, HTTPException, Body
from series_service import Series_service
from pydantic import BaseModel
from schemas import AtorUpdate

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


@router.post("/atores/")
def cadastrar_ator(nome: str):
    novo_id, erro = repo.executar_insert("INSERT INTO ator (nome) VALUES (%s)", (nome,))
    return erro if erro else {"id": novo_id, "mensagem": "Ator cadastrado com sucesso"}

@router.put("/ator/")
def atualizar_ator(dados: AtorUpdate):
    return repo.atualizar_ator(dados)


@router.get("/atores/")
def listar_atores():
    resultado, erro = repo.executar_select("SELECT * FROM ator")
    return erro if erro else resultado

class AssociarAtorRequest(BaseModel):
    ator_id: int
    idserie: int

@router.post("/associar-ator/")
def associar_ator(request: AssociarAtorRequest):
    return repo.associar_ator_com_serie(request.ator_id, request.idserie)

@router.get("/atores-da-serie/{idserie}")
def listar_atores_da_serie(idserie: int):
    return repo.listar_atores_por_serie(idserie)

@router.delete("/ator/{id_ator}")
def deletar_ator(id_ator: int):
    return repo.deletar_ator(id_ator)