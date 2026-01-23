from src.core.modelos import Despesa, Tipo, Status
from src.database.repositorio_despesas import Db_Despesa
from src.utils.resultado import Result

class GerenciadorDespesa:
    
    def criar_despesa(self, descricao: str, valor: float, vencimento: str, status: str, tipo: str):

        try:
            despesa = Despesa(descricao, 
                              valor, 
                              vencimento,
                              Status(status), 
                              Tipo(tipo))
            
        except Exception as e:
            return Result.erro(f"Erro de validação: {e}")
        
        with Db_Despesa() as banco:
           resposta = banco.salvar_despesa(despesa)
           return resposta
        
    def deletar_despesa(self, id):
        with Db_Despesa() as banco:
            resposta = banco.deleta_despesa(id)
            return resposta

    def editar_despesa(self, despesa: Despesa):
        with Db_Despesa() as banco:
            resposta = banco.editar_despesa(despesa)
            return resposta
        
    def ler_todas_despesas(self):
        with Db_Despesa() as banco:
            resposta = banco.ler_todas_despesa()
            return resposta
        