import os
import sqlite3
from dataclasses import dataclass, field
from src.utils.resultado import Result
from src.core.modelos import Despesa

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
        query = """
        CREATE TABLE IF NOT EXISTS despesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            vencimento TEXT NOT NULL,
            status TEXT NOT NULL,
            tipo TEXT NOT NULL
        )
        """
        self.cursor.execute(query)
        self.conexao.commit()

    def salvar_despesa(self, despesa: Despesa):

        valores_despesa = (despesa.descricao, 
                           despesa.valor, 
                           despesa.vencimento.date().isoformat(),   # Converte datetime para string ISO
                           despesa.status.value,                    # Converte Enum para string 'paga'
                           despesa.tipo.value)                      # Converte Enum para string 'paga'

        sql = """
        INSERT INTO despesas (descricao, valor, vencimento, status, tipo) VALUES (?, ?, ?, ?, ?)
        """
        try:
            self.cursor.execute(sql, valores_despesa)
            self.conexao.commit()
            return Result.ok(mensagem="Despesa salva com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar: {e}")
            self.conexao.rollback()
            return Result.erro(mensagem=f"Erro ao salvar os dados: {e}")