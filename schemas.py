from pydantic import BaseModel

class SerieUpdate(BaseModel):
    idserie: int
    titulo: str
    descricao: str
    ano_lancamento: int
    id_categoria: int
    id_ator: int

class AtorUpdate(BaseModel):
    id_ator: int
    nome: str

class CategoriaUpdate(BaseModel):
    id_categoria: int
    nome_categoria: str

class MotivoUpdate(BaseModel):
    id_motivo: int
    serie_id: int
    motivo: str

class AvaliacaoUpdate(BaseModel):
    id_avaliacao: int
    serie_id: int
    usuario_id: int
    nota: int
    comentario: str