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
            despesa = self.salvar_despesa_fixa(descricao=descricao, valor=valor, vencimento=vencimento_obj)
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
            
            if tipo == 'parcelada':
                despesa_parcelada = self.salvar_despesa_parcelada(parcelada_id=despesa.dados, descricao=descricao, valor=valor, vencimento_primeira=vencimento_obj, qtd_parcela=qtd_parcela, fixa_id=fixa_id)
                return despesa_parcelada
                
        return despesa

    def salvar_despesa_fixa(self, descricao, valor, vencimento):
        vencimento_dia = vencimento.day

        despesa = self.gerente_despesa.criar_despesa_fixa(
                    descricao=descricao,
                    valor=valor,
                    dia_vencimento=vencimento_dia,
                    )
        return despesa

    def salvar_despesa_parcelada(self, parcelada_id, descricao, valor, vencimento_primeira, qtd_parcela, fixa_id):
        data_atual = datetime.now().date()
        data_parcela = vencimento_primeira

        despesa_um = self.gerente_despesa.buscar_despesa_id_service(parcelada_id)
        despesa_um = despesa_um.dados

        despesa_um.descricao = f"{descricao} - 1/{qtd_parcela}"
        despesa_um.parcelada_id = despesa_um.id

        self.gerente_despesa.editar_despesa(despesa=despesa_um)
        try:

            for i in range(2, int(qtd_parcela) + 1):
                data_parcela = data_parcela + relativedelta(months=1)
                
                if data_parcela < data_atual:
                    status = "atrasada"
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

            return Result.ok(mensagem="Cadastro realizado com sucesso!")
        
        except Exception as e:
            return Result.erro(f"Erro ao cadastrar a despesa parcelada: {e}")

    def buscar_despesas(self):
        despesas = self.gerente_despesa.ler_todas_despesas()
        return despesas.dados
    
    def editar_despesa(self):
        pass