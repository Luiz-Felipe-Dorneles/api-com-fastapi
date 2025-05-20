from database import Database

class Series_service:

    def __init__(self):
        self.db = Database()

    def executar_update(self, query, valores):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute(query, valores)
            conn.commit()
            cursor.close()
            self.db.desconectar()
            return True, None
        except Exception as e:
            return False, str(e)



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
    
    def executar_consulta(self, query, parametros=None):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, parametros)
            resultado = cursor.fetchall()
            cursor.close()
            self.db.desconectar()
            return resultado, None
        except Exception as e:
            return None, str(e)


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

        
        cursor.execute("SELECT idcategoria FROM categoria WHERE nome_categoria = %s", (nome_categoria,))
        resultado = cursor.fetchone()
        if resultado:
            idcategoria = resultado[0]
        else:
            
            cursor.execute("INSERT INTO categoria (nome_categoria) VALUES (%s)", (nome_categoria,))
            conn.commit()
            idcategoria = cursor.lastrowid

        
        cursor.execute("""
            INSERT INTO serie (titulo, descricao, ano_lancamento, idcategoria, idautor)
            VALUES (%s, %s, %s, %s, %s)
        """, (titulo, descricao, ano_lancamento, idcategoria, idautor))

        conn.commit()
        nova_serie_id = cursor.lastrowid

        cursor.close()
        self.db.desconectar()

        return {"id": nova_serie_id, "mensagem": "Série criada com sucesso"}


    
    def deletar_serie(self, id_serie):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()

            query = "DELETE FROM serie WHERE idserie = %s"
            cursor.execute(query, (id_serie,))
            conn.commit()

            cursor.close()
            self.db.desconectar()

            if cursor.rowcount == 0:
                return {"erro": "Série não encontrada"}
            
            return {"mensagem": "Série deletada com sucesso"}
        except Exception as e:
            return {"erro": str(e)}

    def deletar_ator(self, id_ator):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()

            query = "DELETE FROM ator WHERE id_ator = %s"
            cursor.execute(query, (id_ator,))
            conn.commit()

            cursor.close()
            self.db.desconectar()

            if cursor.rowcount == 0:
                return {"erro": "Ator não encontrado"}
            
            return {"mensagem": "Ator deletado com sucesso"}
        except Exception as e:
            return {"erro": str(e)}
        

    def deletar_categoria(self, id_categoria):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()

            query = "DELETE FROM categoria WHERE id_categoria = %s"
            cursor.execute(query, (id_categoria,))
            conn.commit()

            cursor.close()
            self.db.desconectar()

            if cursor.rowcount == 0:
                return {"erro": "Categoria não encontrada"}
            
            return {"mensagem": "Categoria deletada com sucesso"}
        except Exception as e:
            return {"erro": str(e)}
        

    def deletar_motivo(self, id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()

            query = "DELETE FROM motivo_assistir WHERE id_motivo = %s"
            cursor.execute(query, (id,))
            conn.commit()

            cursor.close()
            self.db.desconectar()

            if cursor.rowcount == 0:
                return {"erro": "Motivo não encontrado"}
            
            return {"mensagem": "Motivo deletado com sucesso"}
        except Exception as e:
            return {"erro": str(e)}
        
    def deletar_avaliacao(self, id_avaliacao):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()

            query = "DELETE FROM avaliacao WHERE id_avaliacao = %s"
            cursor.execute(query, (id_avaliacao,))
            conn.commit()

            cursor.close()
            self.db.desconectar()

            if cursor.rowcount == 0:
                return {"erro": "Avaliação não encontrada"}
            
            return {"mensagem": "Avaliação deletada com sucesso"}
        except Exception as e:
            return {"erro": str(e)}     
    

    def associar_ator_com_serie(self, ator_id, idserie):
        query = "INSERT INTO ator_serie (ator_id, id_serie) VALUES (%s, %s)"
        _, erro = self.executar_insert(query, (ator_id, idserie))
        if erro:
            return {"error": erro}
        return {"mensagem": "Ator associado com sucesso à série"}   
    
    def listar_atores_por_serie(self, idserie):
        query = """
            SELECT a.id_ator, a.nome
            FROM ator_serie ats
            JOIN ator a ON ats.id_ator = a.id_ator
            WHERE ats.id_serie = %s
        """
        resultados, erro = self.executar_consulta(query, (idserie,))
        if erro:
            return {"error": erro}
        return resultados
    

    def atualizar_serie(self, dados):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            query = """
                UPDATE serie
                SET titulo = %s, descricao = %s, ano_lancamento = %s, nome_categoria = %s, id_ator = %s
                WHERE id_serie = %s
            """
            valores = (dados.titulo, dados.descricao, dados.ano_lancamento, dados.nome_categoria, dados.id_ator, dados.idserie)
            cursor.execute(query, valores)
            conn.commit()
            cursor.close()
            self.db.desconectar()
            return {"mensagem": "Série atualizada com sucesso"}
        except Exception as e:
            return {"erro": str(e)}

    def atualizar_ator(self, dados):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            query = "UPDATE ator SET nome = %s WHERE id_ator = %s"
            cursor.execute(query, (dados.nome, dados.id_ator))
            conn.commit()
            cursor.close()
            self.db.desconectar()
            return {"mensagem": "Ator atualizado com sucesso"}
        except Exception as e:
            return {"erro": str(e)}

    def atualizar_categoria(self, dados):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            query = "UPDATE categoria SET nome_categoria = %s WHERE id_categoria = %s"
            cursor.execute(query, (dados.nome_categoria, dados.id_categoria))
            conn.commit()
            cursor.close()
            self.db.desconectar()
            return {"mensagem": "Categoria atualizada com sucesso"}
        except Exception as e:
            return {"erro": str(e)}

    def atualizar_motivo(self, dados):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            query = "UPDATE motivo_para_assistir SET motivo = %s, serie_id = %s WHERE id_motivo = %s"
            cursor.execute(query, (dados.motivo, dados.serie_id, dados.id_motivo))
            conn.commit()
            cursor.close()
            self.db.desconectar()
            return {"mensagem": "Motivo atualizado com sucesso"}
        except Exception as e:
            return {"erro": str(e)}

    def atualizar_avaliacao(self, dados):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            query = """
                UPDATE avaliacao
                SET serie_id = %s, usuario_id = %s, nota = %s, comentario = %s
                WHERE id_avaliacao = %s
            """
            valores = (dados.serie_id, dados.usuario_id, dados.nota, dados.comentario, dados.id_avaliacao)
            cursor.execute(query, valores)
            conn.commit()
            cursor.close()
            self.db.desconectar()
            return {"mensagem": "Avaliação atualizada com sucesso"}
        except Exception as e:
            return {"erro": str(e)}








