from src.core.modelos import Despesa, DespesaFixa, Tipo, Status
from src.database.repositorio_despesas import Db_Despesa
from src.utils.resultado import Result

class GerenciadorDespesa:
    
    def criar_despesa(self, descricao: str, valor: float, vencimento: str, status: str, tipo: str, fixa_id: int = None, parcelada_id: int = None):
        
        try:
            despesa = Despesa(
                descricao=descricao, 
                valor=valor, 
                vencimento=vencimento,
                status=Status(status), 
                tipo=Tipo(tipo),
                fixa_id=fixa_id,
                parcelada_id=parcelada_id,
                )
            
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
        
    def buscar_despesa_id_service(self, id):
        with Db_Despesa() as banco:
            resposta = banco.buscar_despesa_por_id(id=id)
            return resposta
# CRUD FIXAS
        
    def criar_despesa_fixa(self, descricao: str, valor: float, dia_vencimento: int):
        try:
            despesa = DespesaFixa(
                descricao=descricao,
                valor=valor,
                dia_vencimento=dia_vencimento
            )
        except Exception as e:
            return Result.erro(f"Erro de validação: {e}")
        
        with Db_Despesa() as banco:
           resposta = banco.salvar_despesa_fixa(despesa)
           return resposta
        
    def deletar_despesa_fixa(self, id):
        with Db_Despesa() as banco:
            resposta = banco.deletar_despesa_fixa(id)
            return resposta

    def editar_despesa_fixa(self, despesa: DespesaFixa):
        with Db_Despesa() as banco:
            resposta = banco.editar_despesa_fixa(despesa)
            return resposta
        
    def ler_todas_despesas_fixas(self):
        with Db_Despesa() as banco:
            resposta = banco.ler_todas_despesas_fixas()
            return resposta