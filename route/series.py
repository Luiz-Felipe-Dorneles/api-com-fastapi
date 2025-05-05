from fastapi import APIRouter
from database import Database

router = APIRouter(prefix="/series")

# Cadastro de séries
@router.get("/")
def listar_series():
    db = Database()
    conn = db.conectar()

    if not conn:
        return {"error": "Não foi possível conectar ao banco de dados."}
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM serie")
    series = cursor.fetchall()

    cursor.close()
    db.desconectar()

    return series

# Cadastro de atores
@router.post("/atores/")
def cadastrar_ator(nome: str):
    db = Database()
    conn = db.conectar()

    if not conn:
        return {"error": "Não foi possível conectar ao banco de dados."}

    cursor = conn.cursor()
    cursor.execute("INSERT INTO ator (nome) VALUES (%s)", (nome,))
    conn.commit()
    novo_id = cursor.lastrowid

    cursor.close()
    db.desconectar()

    return {"id": novo_id, "mensagem": "Ator cadastrado com sucesso"}

# Listagem de atores
@router.get("/atores/")
def listar_atores():
    db = Database()
    conn = db.conectar()

    if not conn:
        return {"error": "Não foi possível conectar ao banco de dados."}

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ator")
    atores = cursor.fetchall()

    cursor.close()
    db.desconectar()

    return atores

# Associação de atores a uma série
@router.post("/associar_ator/")
def associar_ator_com_serie(serie_id: int, ator_id: int):
    db = Database()
    conn = db.conectar()

    if not conn:
        return {"error": "Não foi possível conectar ao banco de dados."}

    cursor = conn.cursor()
    cursor.execute("INSERT INTO ator_serie (id_serie, ator_id) VALUES (%s, %s)", (serie_id, ator_id))
    conn.commit()

    cursor.close()
    db.desconectar()

    return {"mensagem": "Ator associado com sucesso à série"}

# Cadastro de categorias
@router.post("/categorias/")
def cadastrar_categoria(nome: str):
    db = Database()
    conn = db.conectar()

    if not conn:
        return {"error": "Não foi possível conectar ao banco de dados."}

    cursor = conn.cursor()
    cursor.execute("INSERT INTO categoria (nome_categoria) VALUES (%s)", (nome,))
    conn.commit()
    novo_id = cursor.lastrowid

    cursor.close()
    db.desconectar()

    return {"id": novo_id, "mensagem": "Categoria cadastrada com sucesso"}

# Listagem de categorias
@router.get("/categorias/")
def listar_categorias():
    db = Database()
    conn = db.conectar()

    if not conn:
        return {"error": "Não foi possível conectar ao banco de dados."}

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categoria")
    categorias = cursor.fetchall()

    cursor.close()
    db.desconectar()

    return categorias

# Cadastro de motivos para assistir
@router.post("/motivos/")
def cadastrar_motivo_para_assistir(serie_id: int, motivo: str):
    db = Database()
    conn = db.conectar()

    if not conn:
        return {"error": "Não foi possível conectar ao banco de dados."}

    cursor = conn.cursor()
    cursor.execute("INSERT INTO motivo_para_assistir (serie_id, motivo) VALUES (%s, %s)", (serie_id, motivo))
    conn.commit()

    cursor.close()
    db.desconectar()

    return {"mensagem": "Motivo para assistir registrado com sucesso"}

# Cadastro de avaliação de séries
@router.post("/avaliacoes/")
def avaliar_serie(serie_id: int, usuario_id: int, nota: int, comentario: str):
    db = Database()
    conn = db.conectar()

    if not conn:
        return {"error": "Não foi possível conectar ao banco de dados."}

    cursor = conn.cursor()
    cursor.execute("INSERT INTO avaliacao (serie_id, usuario_id, nota, comentario) VALUES (%s, %s, %s, %s)", 
                   (serie_id, usuario_id, nota, comentario))
    conn.commit()

    cursor.close()
    db.desconectar()

    return {"mensagem": "Avaliação registrada com sucesso"}
