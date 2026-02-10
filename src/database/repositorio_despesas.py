import os
import sqlite3
import datetime
from datetime import date
from dataclasses import dataclass, field
from src.utils.resultado import Result
from src.core.modelos import Despesa, DespesaFixa, Status, Tipo


@dataclass
class Db_Despesa:
    nome_banco: str = field(default='data/banco.db', init=False)
    conexao: sqlite3.Connection = field(init=False, repr=False)
    cursor: sqlite3.Cursor = field(init=False, repr=False)

    def __post_init__(self):
        try:
            diretorio = os.path.dirname(self.nome_banco)
            if diretorio and not os.path.exists(diretorio):
                os.makedirs(diretorio)

            self.conexao = sqlite3.connect(self.nome_banco)
            self.cursor = self.conexao.cursor()

            self._criar_tabela()

        except Exception as e:
            print(f"Erro na criação do banco: {e}")

    def __enter__(self):
        # Quando o Service faz: "with Db_Despesa() as db"
        # O Python executa o __post_init__ e depois este método.
        return self # Ele entrega o objeto pronto para a variável 'db'

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Quando o bloco de código do Service acaba (ou dá erro)
        # O Python executa isso AUTOMATICAMENTE.
        self.conexao.close()
        print("Porta do banco trancada com sucesso!")

    def _criar_tabela(self):
        query_fixas = """
        CREATE TABLE IF NOT EXISTS fixas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            dia_vencimento REAL NOT NULL
        )
        """
        self.cursor.execute(query_fixas)
        self.conexao.commit()

        query_despesas = """
        CREATE TABLE IF NOT EXISTS despesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            vencimento TEXT NOT NULL,
            status TEXT NOT NULL,
            tipo TEXT NOT NULL,
            fixa_id INTEGER,
            parcelada_id INTEGER,
            FOREIGN KEY (fixa_id) REFERENCES fixas (id)
        )
        """
        self.cursor.execute(query_despesas)
        self.conexao.commit()
        

    def salvar_despesa(self, despesa: Despesa):

        valores_despesa = (despesa.descricao, 
                           despesa.valor, 
                           str(despesa.vencimento),              #.date().isoformat(),   # Converte datetime para string ISO
                           despesa.status.value,                    # Converte Enum para string 'paga'
                           despesa.tipo.value,                          # Converte Enum para string 'paga'
                           despesa.fixa_id,
                           despesa.parcelada_id
                           )                      

        sql = """
        INSERT INTO despesas (descricao, valor, vencimento, status, tipo, fixa_id, parcelada_id) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        try:
            self.cursor.execute(sql, valores_despesa)
            self.conexao.commit()
            return Result.ok(mensagem="Despesa salva com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar: {e}")
            self.conexao.rollback()
            return Result.erro(mensagem=f"Erro ao salvar os dados: {e}")
        
    def deleta_despesa(self, id):
        sql = """
        DELETE FROM despesas WHERE id = ?
        """
        try:
            self.cursor.execute(sql, (id,))
            # O rowcount diz quantas linhas foram afetadas
            if self.cursor.rowcount == 0:
                return Result.erro(mensagem="Nenhuma despesa encontrada com este ID.")
            
            self.conexao.commit()
            return Result.ok(mensagem="Despesa deletada!")
        
        except Exception as e:
            print(f"Erro ao deletar: {e}")
            self.conexao.rollback()
            return Result.erro(mensagem=f"Erro ao deletar a despesa: {e}")
       
    def editar_despesa(self, despesa: Despesa):
        sql = """
        UPDATE despesas 
        SET descricao = ?, valor = ?, vencimento = ?, status = ?, tipo = ?
        WHERE id = ?
        """
        parametros = (
            despesa.descricao, 
            despesa.valor, 
            str(despesa.vencimento),        #.isoformat(), 
            despesa.status.value, 
            despesa.tipo.value, 
            despesa.id
        )
        
        try:
            self.cursor.execute(sql, parametros)
            self.conexao.commit()
            return Result.ok(mensagem="Despesa editada com sucesso!")
        except Exception as e:
            self.conexao.rollback()
            return Result.erro(mensagem=f"Falha na edição: {e}")
        
    def ler_todas_despesa(self):
        sql = """
        SELECT id, descricao, valor, vencimento, status, tipo FROM despesas
        """
        try:
            self.cursor.execute(sql)
            linhas = self.cursor.fetchall() # Pega todas as linhas encontradas
            
            despesas = []
            
            for linha in linhas:
                d = Despesa(
                    id=linha[0],
                    descricao=linha[1],
                    valor=linha[2],
                    vencimento=date.fromisoformat(linha[3]),
                    status=Status(linha[4]),
                    tipo=Tipo(linha[5])
                )
                despesas.append(d)
                
            return Result.ok(dados=despesas, mensagem="Dados recuperados com sucesso") # Retorna a lista de objetos
        
        except Exception as e:
            print(f"Erro ao ler banco: {e}")
            return Result.erro(mensagem=f"Erro ao carregar despesas: {e}")
        
# CRUD DESPESAS FIXA

    def salvar_despesa_fixa(self, despesa:  DespesaFixa):
        valores_despesa = (
            despesa.descricao,
            despesa.valor,
            despesa.dia_vencimento,
        )
        sql = """
        INSERT INTO fixas (descricao, valor, dia_vencimento) VALUES (?, ?, ?)
        """

        try:
            self.cursor.execute(sql, valores_despesa)
            self.conexao.commit()
            return Result.ok(mensagem="Despesa salva com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar: {e}")
            self.conexao.rollback()
            return Result.erro(mensagem=f"Erro ao salvar os dados: {e}")
        
    def deletar_despesa_fixa(self, id):
        sql = """
        DELETE FROM fixas WHERE id = ?
        """
        try:
            self.cursor.execute(sql, (id,))
            # O rowcount diz quantas linhas foram afetadas
            if self.cursor.rowcount == 0:
                return Result.erro(mensagem="Nenhuma despesa encontrada com este ID.")
            
            self.conexao.commit()
            return Result.ok(mensagem="Despesa deletada!")
        
        except Exception as e:
            print(f"Erro ao deletar: {e}")
            self.conexao.rollback()
            return Result.erro(mensagem=f"Erro ao deletar a despesa: {e}")
    
    def editar_despesa_fixa(self, despesa: DespesaFixa):
        sql = """
        UPDATE fixas 
        SET descricao = ?, valor = ?, dia_vencimento = ?
        WHERE id = ?
        """
        parametros = (
            despesa.descricao,
            despesa.valor,
            despesa.dia_vencimento,
            despesa.id
            )
        try:
            self.cursor.execute(sql, parametros)
            self.conexao.commit()
            return Result.ok(mensagem="Despesa editada com sucesso!")
        except Exception as e:
            self.conexao.rollback()
            return Result.erro(mensagem=f"Falha na edição: {e}")
        
    def ler_todas_despesas_fixas(self):
        sql = """
        SELECT id, descricao, valor, dia_vencimento FROM fixas
        """
        try:
            self.cursor.execute(sql)
            linhas = self.cursor.fetchall() # Pega todas as linhas encontradas
            
            despesas = []
            for linha in linhas:
                despesa = DespesaFixa(
                    id=linha[0],
                    descricao=linha[1],
                    valor=linha[2],
                    dia_vencimento=(linha[3]),
                    
                )
                despesas.append(despesa)
                
            return Result.ok(dados=despesas, mensagem="Dados recuperados com sucesso") # Retorna a lista de objetos
        
        except Exception as e:
            print(f"Erro ao ler banco: {e}")
            return Result.erro(mensagem=f"Erro ao carregar despesas: {e}")
        