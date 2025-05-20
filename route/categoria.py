from fastapi import APIRouter, HTTPException, Body
from series_service import Series_service
from pydantic import BaseModel
from schemas import CategoriaUpdate

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


@router.post("/categorias/")
def cadastrar_categoria(nome: str):
    novo_id, erro = repo.executar_insert("INSERT INTO categoria (nome_categoria) VALUES (%s)", (nome,))
    return erro if erro else {"id": novo_id, "mensagem": "Categoria cadastrada com sucesso"}

@router.put("/categoria/")
def atualizar_categoria(dados: CategoriaUpdate):
    return repo.atualizar_categoria(dados)

@router.get("/categorias/")
def listar_categorias():
    resultado, erro = repo.executar_select("SELECT * FROM categoria")
    return erro if erro else resultado

@router.delete("/categoria/{id_categoria}")
def deletar_categoria(id_categoria: int):
    return repo.deletar_categoria(id_categoria)

