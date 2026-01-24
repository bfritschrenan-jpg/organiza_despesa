import flet as ft
from datetime import date
class TelaInicial(ft.Container):
    def __init__(self, gerenciador):

        super().__init__()
        self.gerenciador = gerenciador
        self.expand = True
        self.constraints=ft.BoxConstraints(min_width=350, max_width=600),
        self.alignment = ft.Alignment.CENTER

        self.content = ft.ListView(
            expand=True, # Ocupa o espaço disponível no container
            spacing=10, # Define o espaço em pixels entre cada item da lista.
            padding=20, #Espaçamento interno entre a borda da lista e os itens.
            width=900, # Aqui você define a largura máxima pros cards!
            item_extent=110, # Altura fixa para scroll liso
            cache_extent= 600,

            controls=[]  # Lista responsavel por agrupar o conteudo da tela.
        )
        self.content.controls.append(self.cabecalho()) # Adiciona o titúlo na tela
        self.cria_cards_despesa()
        
    def mudar(self):
        pass
        

    def cabecalho(self):
        return ft.ShaderMask(                   
                    content=ft.Text(
                            "OrganiZA DespeZA", 
                            size=40, 
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

    def card_despesa(self, id, descricao, vencimento, valor, cor):
        
        return ft.ShaderMask(
                    key=id,
                    border_radius=ft.BorderRadius.all(15),
                    blend_mode=ft.BlendMode.MODULATE,
                    shader=ft.LinearGradient(
                        colors=[cor, ft.Colors.WHITE], # Muda as cores do gradiente
                        begin=ft.Alignment.TOP_LEFT,      
                        end=ft.Alignment.BOTTOM_RIGHT,   
                    ),
                    content=ft.Card(
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        shape=ft.RoundedRectangleBorder(radius=15),
                        adaptive=True,
                        shadow_color=ft.Colors.ON_SURFACE_VARIANT,
                        content=ft.ListTile(
                                    on_click=self.mudar,
                                    splash_color=ft.Colors.GREEN_200,
                                    hover_color="#B49B9B00",
                                    bgcolor=ft.Colors.GREY_400,
                                    leading=ft.Icon(ft.Icons.FOREST, color=ft.Colors.BLACK),
                                    title=ft.Text(descricao, color=ft.Colors.BLACK),
                                    subtitle=ft.Text(vencimento, color=ft.Colors.BLACK),
                                    trailing=ft.Text(value=valor, size=24, color=ft.Colors.BLACK )
                                )   
                    )      
                )

    def cria_cards_despesa(self):

        self.lista =  self.gerenciador.buscar_despesas()
        self.lista_card = []
        if self.lista:

            for despesa in self.lista:
                id_card = str(despesa.id)
                data_br = despesa.vencimento.strftime("%d/%m/%Y")
                if despesa.status == despesa.status.ATRASADA:
                    cor = ft.Colors.RED_400
                elif despesa.status == despesa.status.PAGA:
                    cor = ft.Colors.GREEN
                else:
                    cor = ft.Colors.WHITE

                card = self.card_despesa(
                    id=id_card, 
                    descricao=despesa.descricao, 
                    vencimento=data_br,
                    valor=despesa.valor,
                    cor= cor
                )
                
                self.lista_card.append(card)


            self.content.controls.extend(self.lista_card) # ADD os cards na lista do ListView para ser lançado na tela
        else: 
            print('lista vazia')