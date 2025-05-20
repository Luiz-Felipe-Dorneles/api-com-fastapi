from fastapi import APIRouter
from series_service import Series_service
from pydantic import BaseModel

router = APIRouter(prefix="/series")
repo = Series_service()



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


@router.delete("/{idserie}")
def deletar_serie(idserie: int):
    return repo.deletar_serie(idserie)


@router.get("/")
def listar_series():
    resultado, erro = repo.executar_select("SELECT * FROM serie")
    return erro if erro else resultado

@router.get("/atores/")
def listar_atores():
    resultado, erro = repo.executar_select("SELECT * FROM ator")
    return erro if erro else resultado

@router.post("/atores/")
def cadastrar_ator(nome: str):
    novo_id, erro = repo.executar_insert("INSERT INTO ator (nome) VALUES (%s)", (nome,))
    return erro if erro else {"id": novo_id, "mensagem": "Ator cadastrado com sucesso"}

class AssociarAtorRequest(BaseModel):
    ator_id: int
    idserie: int

@router.post("/associar-ator/")
def associar_ator(request: AssociarAtorRequest):
    return repo.associar_ator_com_serie(request.ator_id, request.idserie)


@router.delete("/autor/{idautor}")
def deletar_autor(idautor: int):
    return repo.deletar_autor(idautor)



@router.post("/categorias/")
def cadastrar_categoria(nome: str):
    novo_id, erro = repo.executar_insert("INSERT INTO categoria (nome_categoria) VALUES (%s)", (nome,))
    return erro if erro else {"id": novo_id, "mensagem": "Categoria cadastrada com sucesso"}

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

@router.post("/avaliacoes/")
def avaliar_serie(serie_id: int, usuario_id: int, nota: int, comentario: str):
    return repo.executar_sql("INSERT INTO avaliacao (serie_id, usuario_id, nota, comentario) VALUES (%s, %s, %s, %s)",
                             (serie_id, usuario_id, nota, comentario))
