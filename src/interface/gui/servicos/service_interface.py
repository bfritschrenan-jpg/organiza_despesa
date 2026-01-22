from src.core.servicos import GerenciadorDespesa
from datetime import datetime

class GerenciadorDespesaInterface:
    def __init__(self):
        self.gerente_despesa = GerenciadorDespesa()

    def salvar_despesa(self, descricao, valor, vencimento, tipo):
        
        valor = valor.replace(".", "").replace(",", ".")
        valor = float(valor)

        data_atual = datetime.now().date()
        vencimento = datetime.strptime(vencimento, "%d/%m/%Y").date()   # lê a string

        if vencimento < data_atual:
            status = "atrasada"
        elif vencimento == data_atual:
            status = "pendente"
        else:
            status = "pendente"


        tipo = tipo.lower()

        print(type(vencimento))

        print(descricao, valor, vencimento, status, tipo)


    #    despesa = self.gerente_despesa.criar_despesa(
    #                 descricao=descricao,
    #                 valor=valor,
    #                 vencimento=vencimento,
    #                 status=status,
    #                 tipo=tipo,
    #                 )