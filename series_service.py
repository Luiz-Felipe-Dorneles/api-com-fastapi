from database import Database

class Series_service:

    def __init__(self):
        self.db = Database()

    def executar_select(self, query, params=None):
        conn = self.db.conectar()
        if not conn:
            return None, {"error": "Não foi possível conectar ao banco de dados."}
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        resultado = cursor.fetchall()
        cursor.close()
        self.db.desconectar()
        return resultado, None

    def executar_insert(self, query, params=None):
        conn = self.db.conectar()
        if not conn:
            return None, {"error": "Não foi possível conectar ao banco de dados."}
        
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        novo_id = cursor.lastrowid
        cursor.close()
        self.db.desconectar()
        return novo_id, None

    def executar_sql(self, query, params=None):
        conn = self.db.conectar()
        if not conn:
            return {"error": "Não foi possível conectar ao banco de dados."}
        
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        cursor.close()
        self.db.desconectar()
        return {"mensagem": "Operação realizada com sucesso"}
    
    def criar_serie(self, titulo, descricao, ano_lancamento, nome_categoria, idautor):
        conn = self.db.conectar()
        if not conn:
            return {"error": "Erro na conexão com o banco de dados"}

        cursor = conn.cursor()

        # Verifica se a categoria já existe
        cursor.execute("SELECT idcategoria FROM categoria WHERE nome_categoria = %s", (nome_categoria,))
        resultado = cursor.fetchone()
        if resultado:
            idcategoria = resultado[0]
        else:
            # Cria a categoria se não existir
            cursor.execute("INSERT INTO categoria (nome_categoria) VALUES (%s)", (nome_categoria,))
            conn.commit()
            idcategoria = cursor.lastrowid

        # Insere a série
        cursor.execute("""
            INSERT INTO serie (titulo, descricao, ano_lancamento, idcategoria, idautor)
            VALUES (%s, %s, %s, %s, %s)
        """, (titulo, descricao, ano_lancamento, idcategoria, idautor))

        conn.commit()
        nova_serie_id = cursor.lastrowid

        cursor.close()
        self.db.desconectar()

        return {"id": nova_serie_id, "mensagem": "Série criada com sucesso"}


    def deletar_serie(self, idserie):
        query = "DELETE FROM serie WHERE idserie = %s"
        _, erro = self.executar_insert(query, (idserie,))
        if erro:
            return {"error": erro}
        return {"mensagem": "Série deletada com sucesso"}

    def deletar_autor(self, idautor):
        query = "DELETE FROM autor WHERE idautor = %s"
        _, erro = self.executar_insert(query, (idautor,))
        if erro:
            return {"error": erro}
        return {"mensagem": "Autor deletado com sucesso"}
    
    def deletar_categoria(self, idcategoria):
        query = "DELETE FROM categoria WHERE idcategoria = %s"
        _, erro = self.executar_insert(query, (idcategoria,))
        if erro:
            return {"error": erro}
        return {"mensagem": "Categoria deletada com sucesso"}
    

    def associar_ator_com_serie(self, ator_id, idserie):
        query = "INSERT INTO ator_serie (ator_id, id_serie) VALUES (%s, %s)"
        _, erro = self.executar_insert(query, (ator_id, idserie))
        if erro:
            return {"error": erro}
        return {"mensagem": "Ator associado com sucesso à série"}




