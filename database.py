import mysql.connector as mc
from mysql.connector import Error
from dotenv import load_dotenv
from os import getenv

class Database:
    def __init__(self):
        load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env
        self.host = getenv('DB_HOST')
        self.username = getenv('DB_USER')
        self.password = getenv('DB_PSWD')
        self.database = getenv('DB_NAME')
        self.connection = None
        self.cursor = None

    def get_connection(self):
        try:
            self.connection = mc.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print('Conexão ao banco de dados realizada com sucesso!')
                return self.connection
            else:
                print('Falha na conexão ao banco de dados.')
                return None
        except Error as e:
            print(f'Erro de conexão: {e}')
            return None

    def conectar(self):
        if not self.connection or not self.connection.is_connected():
            return self.get_connection()
        print('Já estamos conectados ao banco de dados!')
        return self.connection

    def desconectar(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
        print('Conexão com o banco de dados encerrada com sucesso!')

    def executar(self, sql, params=None):
        conn = self.conectar()
        if not conn:
            print('Conexão ao banco de dados não estabelecida!')
            return None
        
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql, params)
            self.connection.commit()
            return self.cursor
        except Error as e:
            print(f'Erro de execução: {e}')
            return None

    def consultar(self, sql, params=None):
        conn = self.conectar()
        if not conn:
            print('Conexão ao banco de dados não estabelecida!')
            return None
        
        try:
            self.cursor = self.connection.cursor(dictionary=True)
            self.cursor.execute(sql, params)
            return self.cursor.fetchall()
        except Error as e:
            print(f'Erro de execução: {e}')
            return None
