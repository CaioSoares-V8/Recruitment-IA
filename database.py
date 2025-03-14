import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

class BancoDeDados:
    def __init__(self):
        """Inicializa a conexão com o banco de dados MySQL"""
        self.host = os.getenv("DB_HOST")
        self.database = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")

    def conectar(self):
        """Cria uma conexão com o banco de dados MySQL."""
        try:
            conexao = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if conexao.is_connected():
                return conexao
        except Error as e:
            print(f"Erro ao conectar ao banco: {e}")
            return None

    def listar_vagas(self):
        """Retorna todas as vagas do banco de dados."""
        conexao = self.conectar()
        if not conexao:
            return []
        
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT * FROM vagas")
            vagas = cursor.fetchall()
            return vagas
        except Error as e:
            print(f"Erro ao listar vagas: {e}")
            return []
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

    def listar_candidaturas_por_vaga(self, vaga_id):
        """Retorna os candidatos de uma vaga específica."""
        conexao = self.conectar()
        if not conexao:
            return []
        
        try:
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT * FROM candidaturas WHERE vaga_id = %s"
            cursor.execute(query, (vaga_id,))
            candidatos = cursor.fetchall()
            return candidatos
        except Error as e:
            print(f"Erro ao listar candidaturas por vaga: {e}")
            return []
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

    def criar_vaga(self, titulo, descricao, responsavel, requisitos, tipo_contrato, salario):
        """Cria uma nova vaga no banco de dados."""
        conexao = self.conectar()
        if not conexao:
            return False
        
        try:
            cursor = conexao.cursor()
            query = """INSERT INTO vagas (titulo, descricao, responsavel, requisitos, tipo_contrato, salario, status) 
                       VALUES (%s, %s, %s, %s, %s, %s, 'Aberta')"""
            valores = (titulo, descricao, responsavel, requisitos, tipo_contrato, salario)
            cursor.execute(query, valores)
            conexao.commit()
            return True
        except Error as e:
            print(f"Erro ao criar vaga: {e}")
            return False
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

    def criar_candidatura(self, vaga_id, nome, email, telefone, experiencia, habilidades):
        """Cria uma nova candidatura para uma vaga."""
        conexao = self.conectar()
        if not conexao:
            return False

        try:
            cursor = conexao.cursor()
            query = """INSERT INTO candidaturas (vaga_id, nome, email, telefone, experiencia, habilidades) 
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            valores = (vaga_id, nome, email, telefone, experiencia, habilidades)
            cursor.execute(query, valores)
            conexao.commit()
            return True
        except Error as e:
            print(f"Erro ao criar candidatura: {e}")
            return False
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

    def excluir_vaga(self, vaga_id):
        """Exclui uma vaga do banco de dados."""
        conexao = self.conectar()
        if not conexao:
            return False

        try:
            cursor = conexao.cursor()
            query = "DELETE FROM vagas WHERE id = %s"
            cursor.execute(query, (vaga_id,))
            conexao.commit()
            return True
        except Error as e:
            print(f"Erro ao excluir vaga: {e}")
            return False
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

    def contratar_candidato(self, vaga_id):
        """Atualiza o status da vaga para 'Fechada' após a contratação de um candidato."""
        conexao = self.conectar()
        if not conexao:
            return False

        try:
            cursor = conexao.cursor()
            query = "UPDATE vagas SET status = 'Fechada' WHERE id = %s"
            cursor.execute(query, (vaga_id,))
            conexao.commit()
            return True
        except Error as e:
            print(f"Erro ao contratar candidato: {e}")
            return False
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()