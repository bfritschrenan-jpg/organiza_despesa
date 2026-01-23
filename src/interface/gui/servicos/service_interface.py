from src.core.servicos import GerenciadorDespesa
from datetime import datetime

class GerenciadorDespesaInterface:
    def __init__(self):
        self.gerente_despesa = GerenciadorDespesa()

    def salvar_despesa(self, descricao, valor, vencimento, tipo):
        
        valor = valor.replace(".", "").replace(",", ".")
        valor = float(valor)
        
        vencimento_obj = datetime.strptime(vencimento, "%d/%m/%Y")   # lê a string

        data_atual = datetime.now().date()
        vencimento_data = datetime.strptime(vencimento, "%d/%m/%Y").date()
        if vencimento_data < data_atual:
            status = "atrasada"
        elif vencimento_data == data_atual:
            status = "pendente"
        else:
            status = "pendente"


        tipo = tipo.lower()

        print(type(vencimento))

        print(descricao, valor, vencimento, status, tipo)


        despesa = self.gerente_despesa.criar_despesa(
                    descricao=descricao,
                    valor=valor,
                    vencimento=vencimento_obj,
                    status=status,
                    tipo=tipo,
                    )

        print(despesa.mensagem)
        if despesa.sucesso:
            print("despesa cadastrasa")
        else:
            print("despesa não cadastrada")

