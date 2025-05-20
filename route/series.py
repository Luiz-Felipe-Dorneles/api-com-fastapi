from fastapi import APIRouter, HTTPException, Body
from series_service import Series_service
from pydantic import BaseModel

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
    nome_categoria: str
    idautor: int

@router.post("/")
def criar_serie(serie: SerieRequest):
    return repo.criar_serie(
        serie.titulo,
        serie.descricao,
        serie.ano_lancamento,
        serie.nome_categoria,
        serie.idautor
    )

# PUT atualizar série
@router.put("/serie/")
def atualizar_serie(dados: dict = Body(...)):
    if "idserie" not in dados:
        raise HTTPException(status_code=400, detail="Campo 'idserie' é obrigatório")
    query, valores = montar_update_query("serie", "idserie", dados)
    sucesso, erro = repo.executar_update(query, tuple(valores))
    if erro:
        return {"error": erro}
    return {"mensagem": "Série atualizada com sucesso"}

@router.delete("/{idserie}")
def deletar_serie(idserie: int):
    return repo.deletar_serie(idserie)


@router.get("/")
def listar_series():
    resultado, erro = repo.executar_select("SELECT * FROM serie")
    return erro if erro else resultado


@router.post("/atores/")
def cadastrar_ator(nome: str):
    novo_id, erro = repo.executar_insert("INSERT INTO ator (nome) VALUES (%s)", (nome,))
    return erro if erro else {"id": novo_id, "mensagem": "Ator cadastrado com sucesso"}

# PUT atualizar ator
@router.put("/ator/")
def atualizar_ator(dados: dict = Body(...)):
    if "id_ator" not in dados:
        raise HTTPException(status_code=400, detail="Campo 'id_ator' é obrigatório")
    query, valores = montar_update_query("ator", "id_ator", dados)
    sucesso, erro = repo.executar_update(query, tuple(valores))
    if erro:
        return {"error": erro}
    return {"mensagem": "Ator atualizado com sucesso"}


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

@router.delete("/autor/{idautor}")
def deletar_autor(idautor: int):
    return repo.deletar_autor(idautor)



@router.post("/categorias/")
def cadastrar_categoria(nome: str):
    novo_id, erro = repo.executar_insert("INSERT INTO categoria (nome_categoria) VALUES (%s)", (nome,))
    return erro if erro else {"id": novo_id, "mensagem": "Categoria cadastrada com sucesso"}

# PUT atualizar categoria
@router.put("/categoria/")
def atualizar_categoria(dados: dict = Body(...)):
    if "id_categoria" not in dados:
        raise HTTPException(status_code=400, detail="Campo 'id_categoria' é obrigatório")
    query, valores = montar_update_query("categoria", "id_categoria", dados)
    sucesso, erro = repo.executar_update(query, tuple(valores))
    if erro:
        return {"error": erro}
    return {"mensagem": "Categoria atualizada com sucesso"}

@router.delete("/categoria/{idcategoria}")
def deletar_categoria(idcategoria: int):
    return repo.deletar_categoria(idcategoria)

@router.get("/categorias/")
def listar_categorias():
    resultado, erro = repo.executar_select("SELECT * FROM categoria")
    return erro if erro else resultado

@router.post("/motivos/")
def cadastrar_motivo_para_assistir(serie_id: int, motivo: str):
    return repo.executar_sql("INSERT INTO motivo_para_assistir (serie_id, motivo) VALUES (%s, %s)", (serie_id, motivo))


# PUT atualizar motivo_para_assistir
@router.put("/motivo/")
def atualizar_motivo(dados: dict = Body(...)):
    if "id" not in dados:
        raise HTTPException(status_code=400, detail="Campo 'id' é obrigatório")
    query, valores = montar_update_query("motivo_para_assistir", "id", dados)
    sucesso, erro = repo.executar_update(query, tuple(valores))
    if erro:
        return {"error": erro}
    return {"mensagem": "Motivo atualizado com sucesso"}
    

@router.get("/motivos/")
def listar_motivos():
    query = "SELECT * FROM motivo_para_assistir"
    resultados, erro = servico.executar_consulta(query)
    if erro:
        raise HTTPException(status_code=500, detail=erro)
    return resultados


@router.delete("/motivo/{id}")
def deletar_motivo(id: int):
    query = "DELETE FROM motivo_para_assistir WHERE id = %s"
    sucesso, erro = repo.executar_update(query, (id,))
    if erro:
        raise HTTPException(status_code=500, detail=erro)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Motivo não encontrado")
    return {"mensagem": "Motivo deletado com sucesso"}



@router.post("/avaliacoes/")
def avaliar_serie(serie_id: int, usuario_id: int, nota: int, comentario: str):
    return repo.executar_sql("INSERT INTO avaliacao (serie_id, usuario_id, nota, comentario) VALUES (%s, %s, %s, %s)",
                             (serie_id, usuario_id, nota, comentario))


# PUT atualizar avaliação
@router.put("/avaliacao/")
def atualizar_avaliacao(dados: dict = Body(...)):
    if "id" not in dados:
        raise HTTPException(status_code=400, detail="Campo 'id' é obrigatório")
    query, valores = montar_update_query("avaliacao", "id", dados)
    sucesso, erro = repo.executar_update(query, tuple(valores))
    if erro:
        return {"error": erro}
    return {"mensagem": "Avaliação atualizada com sucesso"}

@router.get("/avaliacoes/")
def listar_avaliacoes():
    query = "SELECT * FROM avaliacao"
    resultados, erro = servico.executar_consulta(query)
    if erro:
        raise HTTPException(status_code=500, detail=erro)
    return resultados

@router.delete("/avaliacao/{id}")
def deletar_avaliacao(id: int):
    query = "DELETE FROM avaliacao WHERE id = %s"
    sucesso, erro = repo.executar_update(query, (id,))
    if erro:
        raise HTTPException(status_code=500, detail=erro)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return {"mensagem": "Avaliação deletada com sucesso"}
