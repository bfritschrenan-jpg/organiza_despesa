from src.core.servicos import GerenciadorDespesa
from datetime import datetime

class GerenciadorDespesaInterface:
    def __init__(self):
        self.gerente_despesa = GerenciadorDespesa()

    def salvar_despesa(self, descricao, valor, vencimento, tipo, qtd_parcela):
        
        valor = valor.replace(".", "").replace(",", ".")
        valor = float(valor)
        
        vencimento_obj = datetime.strptime(vencimento, "%d/%m/%Y").date()   # lê a string

        data_atual = datetime.now().date()

        if vencimento_obj < data_atual:
            status = "atrasada"
        elif vencimento_obj == data_atual:
            status = "pendente"
        else:
            status = "pendente"

        tipo = tipo.lower()

        despesa = self.gerente_despesa.criar_despesa(
                    descricao=descricao,
                    valor=valor,
                    vencimento=vencimento_obj,
                    status=status,
                    tipo=tipo,
                    )

        if despesa.sucesso:
            print("despesa cadastrasa")
        else:
            print("despesa não cadastrada")
        return despesa

    def salvar_despesa_fixa(self, descricao, valor, vencimento):
        valor = valor.replace(".", "").replace(",", ".")
        valor = float(valor)
        
        vencimento_obj = datetime.strptime(vencimento, "%d/%m/%Y").date()   # lê a string
        vencimento_obj = vencimento_obj.day

        # data_atual = datetime.now().date()

        # if vencimento_obj < data_atual:
        #     status = "atrasada"
        # elif vencimento_obj == data_atual:
        #     status = "pendente"
        # else:
        #     status = "pendente"

        despesa = self.gerente_despesa.criar_despesa_fixa(
                    descricao=descricao,
                    valor=valor,
                    dia_vencimento=vencimento_obj,
                    )

        print(despesa.mensagem)

        if despesa.sucesso:
            print("despesa cadastrasa")
        else:
            print("despesa não cadastrada")
        return despesa



    def buscar_despesas(self):
        despesas = self.gerente_despesa.ler_todas_despesas()
        return despesas.dados
    
    def editar_despesa(self):
        pass