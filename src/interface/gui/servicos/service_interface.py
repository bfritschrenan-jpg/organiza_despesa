from src.core.servicos import GerenciadorDespesa
from datetime import datetime
from src.utils.resultado import Result
from dateutil.relativedelta import relativedelta


class GerenciadorDespesaInterface:
    def __init__(self):
        self.gerente_despesa = GerenciadorDespesa()

    def salvar_despesa(self, descricao, valor, vencimento, tipo, qtd_parcela, fixa_id = None, parcelada_id = None):
        
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

        if tipo == 'fixa':
            despesa = self.salvar_despesa_fixa(descricao=descricao, valor=valor, vencimento=vencimento)
        else:    
            despesa = self.gerente_despesa.criar_despesa(
                    descricao=descricao,
                    valor=valor,
                    vencimento=vencimento_obj,
                    status=status,
                    tipo=tipo,
                    fixa_id=fixa_id,
                    parcelada_id=parcelada_id,
                    )
            print("")
            print(type(despesa.dados))
            print(despesa.dados)
            print("")
            if tipo == 'parcelada':
                despesa_parcelada = self.salvar_despesa_parcelada(parcelada_id=despesa.dados, descricao=descricao, valor=valor, vencimento_primeira=vencimento_obj, qtd_parcela=qtd_parcela, fixa_id=fixa_id)
                if despesa_parcelada == "sucesso":
                    print("despesa parcelada cadastrasa")
                    return Result.ok(mensagem='Despesa parcelada cadastrada com Sucesso')
                else:
                    print("despesa parcelada não cadastrada")
                    return Result.erro(mensagem='erro ao cadastar a Despesa parcelada')

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

    def salvar_despesa_parcelada(self, parcelada_id, descricao, valor, vencimento_primeira, qtd_parcela, fixa_id):
        data_atual = datetime.now().date()
        data_parcela = vencimento_primeira
        print('função')
        for i in range(2, int(qtd_parcela) + 1):
            if vencimento_primeira < data_atual:
                status = "atrasada"
            elif vencimento_primeira == data_atual:
                status = "pendente"
            else:
                status = "pendente"

            despesa = self.gerente_despesa.criar_despesa(
                descricao=f'{descricao} - {i}/{qtd_parcela}',
                valor=valor,
                vencimento=data_parcela,
                status=status,
                tipo="parcelada",
                fixa_id= fixa_id,
                parcelada_id=parcelada_id,
                )

            data_parcela = data_parcela + relativedelta(months=1)
            print(despesa.mensagem)
            
        return 'sucesso'


    def buscar_despesas(self):
        despesas = self.gerente_despesa.ler_todas_despesas()
        return despesas.dados
    
    def editar_despesa(self):
        pass