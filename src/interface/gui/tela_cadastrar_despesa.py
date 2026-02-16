import flet as ft
from datetime import datetime 

class TelaCadastrarDespesa(ft.Container):
    def __init__(self, app_flet: object):
        super().__init__()
        self.app_flet = app_flet
        self.page_app = self.app_flet.page
        self.gerenciador = self.app_flet.gerenciador_interface
        self.width=1200
        self.expand=True
        self.margin = ft.Margin.symmetric(horizontal=20)
        
        self.content = ft.Column(
            
            margin=ft.Margin.only(top=25),
            alignment = ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            controls=[],  # Lista responsavel por agrupar o conteudo da tela.
        )

        # TITULO DA PAGINA
        self.titulo = ft.ShaderMask(                   
            content=ft.Text(
                value="CADASTRO DE DESPESA", 
                size=24, 
                weight="bold",
                text_align=ft.TextAlign.CENTER
            ), 
            blend_mode=ft.BlendMode.SRC_IN, # ESSENCIAL: Faz o texto assumir a cor do gradiente
            shader=ft.LinearGradient(
                colors=[ft.Colors.BLUE, ft.Colors.PURPLE],
                begin=ft.Alignment.TOP_LEFT,      # CORREÇÃO: Usar ft.Alignment.TOP_LEFT
                end=ft.Alignment.BOTTOM_RIGHT,   # CORREÇÃO: Usar ft.Alignment.BOTTOM_RIGHT
            )
        )

        # CAIXA DE TEXTO DESCRIÇÃO DA DESPESA
        self.descricao = ft.TextField(
            label = "Descrição:",
            border_radius=ft.BorderRadius.all(15),
            border_color=ft.Colors.LIGHT_BLUE,
            focused_border_color=ft.Colors.BLUE_600,
            focused_border_width=2,
            width=400,   # Tamanho ideal/máximo
            expand=True  # Permite que ele diminua se a tela for menor
            )

        # CAIXA DE TEXTO VALOR DA DESPESA
        self.valor =ft.TextField(
            label = "Valor da Despesa:",
            
            border_radius=ft.BorderRadius.all(15),
            border_color=ft.Colors.LIGHT_BLUE,
            focused_border_color=ft.Colors.BLUE_600,
            focused_border_width=2,
            width=400,
            expand=True,

            # prefix="R$ ",
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]"),
            # hint_text="0,00",
            on_change=self.mascara_valor
            )
        
        # CAIXA DE SELEÇÃO DE TIPO DE DESPESA
        self.tipo = ft.Dropdown(
            value="Única",
            border_radius=ft.BorderRadius.all(15),
            border_color=ft.Colors.LIGHT_BLUE,
            focused_border_color=ft.Colors.BLUE_600,
            on_select=self.mostra_caixa_parcela,
            label="Tipo de Despesa",
            width=400,
            options=[
                ft.dropdown.Option("Fixa"),
                ft.dropdown.Option("Única"),
                ft.dropdown.Option("Parcelada"),
            ],
        ) 

        # CAIXA DE TEXTO QUANTIDADE PARCELAS
        self.caixa_qtd_parcelas = ft.TextField(
            label="Qtd. Parcelas:",
            border_radius=ft.BorderRadius.all(15),
            border_color=ft.Colors.LIGHT_BLUE,
            focused_border_color=ft.Colors.BLUE_600,
            keyboard_type=ft.KeyboardType.NUMBER,
            width=400,
            visible=False,
            input_filter=ft.NumbersOnlyInputFilter()
        )

        # CAIXA DE TEXTO DATA DE VENCIMENTO
        hoje = datetime.now().strftime("%d/%m/%Y") # OBTEM DATA ATUAL DO DIA

        self.data_vencimento = ft.TextField(
            label = "Data de Vencimento:",
            value = hoje,
            border_radius=ft.BorderRadius.all(15),
            border_color=ft.Colors.LIGHT_BLUE,
            focused_border_color=ft.Colors.BLUE_600,
            focused_border_width=2,
            width=350, # Tamanho ideal/máximo
            expand=7, # Permite que ele diminua se a tela for menor
            on_change=self.mascara_data
        )

        # ICONE DO CALENDARIO
        self.btn_data = ft.ShaderMask(
            blend_mode=ft.BlendMode.SRC_IN, # ESSENCIAL: Faz o texto assumir a cor do gradiente
            shader=ft.LinearGradient(
                colors=[ft.Colors.BLUE, ft.Colors.PURPLE],
                begin=ft.Alignment.TOP_LEFT,      # CORREÇÃO: Usar ft.Alignment.TOP_LEFT
                end=ft.Alignment.BOTTOM_RIGHT,   # CORREÇÃO: Usar ft.Alignment.BOTTOM_RIGHT
            ),
            content=ft.IconButton(
                expand=1,
                width=50, # Tamanho ideal/máximo
                icon=ft.Icons.CALENDAR_MONTH,
                align= ft.Alignment.CENTER_RIGHT,
                on_click=self.abrir # Abre o calendário
            )
        )
        # BOTÃO SALVAR DESPESA
        self.btn_salvar = ft.ShaderMask(
            shader=ft.LinearGradient(
                colors=[ft.Colors.BLUE, ft.Colors.WHITE],
                begin=ft.Alignment.TOP_LEFT,      # CORREÇÃO: Usar ft.Alignment.TOP_LEFT
                end=ft.Alignment.BOTTOM_RIGHT,   # CORREÇÃO: Usar ft.Alignment.BOTTOM_RIGHT
            ),
            content= ft.Button(
                width=200, # Largura definida para notar a centralização
                height=45,   # Altura definida para notar a centralização
                align=ft.Alignment.CENTER,
                content=ft.Text("Salvar Despesa", size=20,), 
                on_click= self.salva_despesa
            )
        )

        # ESPAÇO PARA COLOCAR OS ELEMENTOS NA TELA
        
        self.content.controls = [
            self.titulo,
            self.descricao,
            self.valor,
            self.tipo,
            self.caixa_qtd_parcelas,

            ft.Row( 
                expand=False,
                width=400,
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    self.data_vencimento, 
                    self.btn_data,
                ]
            ),

            self.btn_salvar,
        ]

    # FUNÇÕES DE APAIO

    def mascara_data(self, e):
        # 1. Remove qualquer caractere que não seja número
        texto = "".join(filter(str.isdigit, e.control.value))
        
        # 2. Limita a quantidade de dígitos para uma data (DDMMYYYY = 8 dígitos)
        texto = texto[:8]
        
        # 3. Aplica a máscara de acordo com o preenchimento
        if len(texto) <= 2:
            novo_valor = texto
        elif len(texto) <= 4:
            novo_valor = f"{texto[:2]}/{texto[2:]}"
        else:
            novo_valor = f"{texto[:2]}/{texto[2:4]}/{texto[4:]}"
        
        # 4. Atualiza o campo se o valor formatado for diferente do atual
        if e.control.value != novo_valor:
            e.control.value = novo_valor
            # Mantém o cursor sempre ao final do texto
            posicao = len(novo_valor)
            e.control.selection_start = posicao
            e.control.selection_end = posicao
            
        e.control.update()

    def mascara_valor(self, e):
        # 1. Remove tudo que não é dígito
        numeros = "".join(filter(str.isdigit, e.control.value))
        # 2. Se o campo for limpo (apagado), reseta e para a execução
        if not numeros:
            e.control.value = ""
            e.control.update()
            return

        # 3. Transforma em decimal e formata (Padrão BR: 1.234,56)
        valor_decimal = int(numeros) / 100
        novo_texto = f"{valor_decimal:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        # 4. Só atualiza se o valor mudou (evita recursão infinita no on_change)
        if e.control.value != novo_texto:
            e.control.value = novo_texto
            # Mantém o cursor sempre no final para evitar saltos
            posicao = len(novo_texto)
            e.control.selection_start = posicao
            e.control.selection_end = posicao
            
        e.control.update()
                 
    def mostra_caixa_parcela(self, e):
        if e.control.value == "Parcelada":
            self.caixa_qtd_parcelas.visible = True 
            self.caixa_qtd_parcelas.update()
        else:
            self.caixa_qtd_parcelas.visible = False 
            self.caixa_qtd_parcelas.update()

    def abrir(self, e):
        self.app_flet.gerenciador.abrir_calendario(self.salva_data)
        
    def salva_data(self, e):
        data = e.control.value.strftime("%d/%m/%Y")
        self.data_vencimento.value = data
        self.data_vencimento.update()
          
    # FUNÇÃO RESPONSAVEL POR CAPTA OS DADOS E ENVIAR PARA O SERVICE SALVAR AS DESPESAS
    def salva_despesa(self, e):
        tipo = self.tipo.value
        valor = self.valor.value
        descricao = self.descricao.value
        data_vencimento = self.data_vencimento.value
        qtd_parcelas = self.caixa_qtd_parcelas.value

        resposta = self.gerenciador.salvar_despesa(descricao, valor, data_vencimento, tipo, qtd_parcelas)
        if resposta.sucesso == True:
            print(resposta.sucesso)
            self.app_flet.page.update()
