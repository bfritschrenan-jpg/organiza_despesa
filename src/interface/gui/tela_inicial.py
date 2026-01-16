import flet as ft
import datetime

class InterfacePrincipal:
    def __init__(self, page: ft.Page):
        self.page = page
        self.tela()

    def tela(self):
        self.alerta = ft.SnackBar(ft.Text("Dados salvos com sucesso!"))
        self.page.overlay.append(self.alerta)
        self.page.add(
                    ft.Container(
                        content=ft.Text(
                            "ORGANIZADOR DE DESPESAS",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_900,
                            text_align=ft.TextAlign.CENTER,
                            ),
                        margin=ft.margin.only(bottom=30), # 30 de espaço livre apenas embaixo
                            
                    )
                )
        self.descricao = ft.TextField(label="Descrição")

        self.valor = ft.TextField(
                                label="Valor",
                                keyboard_type=ft.KeyboardType.NUMBER,
                                prefix=ft.Text("R$ "),
                                prefix_icon=ft.Icons.ATTACH_MONEY,
                                hint_text="0,00",
                                on_change=self.formatar_moeda
                                )
        
        self.calendario = ft.DatePicker(
                                on_change=self.mudar_data,
                                cancel_text="Cancelar",
                                confirm_text="OK",
                                help_text="Selecione o vencimento",
                                first_date=datetime.datetime(1971, 1, 1), 
                                last_date=datetime.datetime(2030, 12, 31),
                                value=datetime.datetime.now()                  
        )

        self.page.overlay.append(self.calendario)

        self.vencimento = ft.TextField(
                                label="Vencimento", 
                                read_only=False,
                                expand=False,
                                value=datetime.datetime.now().strftime("%d/%m/%Y"),
                                on_change=self.formatar_data
                                )

        botao_calendario = ft.IconButton(
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=self.abrir_calendario # Abre o calendário
        )

        self.tipo = ft.Dropdown(
            label="Tipo",
            options=[
                ft.dropdown.Option("Unica"),
                ft.dropdown.Option("Fixa"),
                ft.dropdown.Option("Parcelada"),
            ]
        )




        self.status = ft.Checkbox(label="Pago", value=False)

        self.page.add(self.descricao)
        self.page.add(ft.Row([self.valor, self.status], alignment=ft.MainAxisAlignment.CENTER))  # Adiciona os dois em uma linha
        self.page.add(
            ft.Row([self.vencimento, botao_calendario], alignment=ft.MainAxisAlignment.CENTER,)# Coloca um ao lado do outro
        )
        # self.page.add(self.status)
        self.page.add(self.tipo)
        self.page.add(
            ft.ElevatedButton("Clique aqui", on_click=self.botao_salvar))

    def botao_salvar(self, e):
        dados = [self.descricao.value, self.valor.value, self.vencimento.value, self.status.value, self.tipo.value]

        self.alerta.open = True
        self.page.update()

        self.descricao.value = ""
        self.valor.value = ""
        self.page.add(ft.Text(f"Você digitou: {dados}"))
        self.page.update()

    def formatar_moeda(self, e):
        valor = self.valor.value
        valor = ''.join(filter(str.isdigit, valor))
        if valor:          
            valor_float = float(valor) / 100

            texto_formatado = f"{valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            self.valor.value = texto_formatado
        else:
            self.valor.value = ""

        self.page.update()
        self.valor.focus()
        self.valor.selection_start = self.valor.selection_end = len(self.valor.value)
        self.page.update()

    def mudar_data(self, e):
        
        data_escolhida = self.calendario.value.strftime("%d/%m/%Y")
        self.vencimento.value = data_escolhida
        self.page.update()

    def abrir_calendario(self, e):
        self.calendario.open = True
        self.page.update()

    def formatar_data(self, e):
        texto = self.vencimento.value

        # só dígitos
        numeros = ''.join(filter(str.isdigit, texto))

        # limita no máximo 8 dígitos (ddMMyyyy)
        numeros = numeros[:8]

        # monta com barras: dd/mm/aaaa
        formatado = ""
        if len(numeros) >= 2:
            formatado += numeros[:2]
        else:
            formatado += numeros
            self.vencimento.value = formatado
            self.page.update()
            return

        if len(numeros) >= 4:
            formatado += "/" + numeros[2:4]
        else:
            formatado += "/" + numeros[2:]
            self.vencimento.value = formatado
            self.page.update()
            return

        if len(numeros) > 4:
            formatado += "/" + numeros[4:]

        self.vencimento.value = formatado

        # coloca o cursor no final
        self.vencimento.focus()
        self.vencimento.selection_start = self.vencimento.selection_end = len(self.vencimento.value)

        self.page.update()