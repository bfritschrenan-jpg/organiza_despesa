import flet as ft

class TelaInicial(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.constraints=ft.BoxConstraints(min_width=350, max_width=600),
        self.alignment = ft.Alignment.CENTER
        self.content = ft.ListView(
            expand=True, # Ocupa o espaço disponível no container
            divider_thickness=10, # Adiciona uma linha divisória visual entre os itens com a espessura definida.
            spacing=10, # Define o espaço em pixels entre cada item da lista.
            padding=20, #Espaçamento interno entre a borda da lista e os itens.
            width=900, # Aqui você define a largura máxima pros cards!
            item_extent=110, # Altura fixa para scroll liso
            cache_extent= 600,

            controls=[]  
        )
        self.lista = ["1","2","3","4","5",]
        self.cards = [self.card_despesa(nome) for nome in self.lista]
        for card in self.cards: 
            self.content.controls.append(card)

    def mudar(self):
        self.content.controls.append(self.card_despesa("Teste"))
        

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

    def card_despesa(self, nome):
        # g = self.content.controls
        # print(self.g)
        return ft.ShaderMask(
                    border_radius=ft.border_radius.all(15),
                    blend_mode=ft.BlendMode.MODULATE,
                    shader=ft.LinearGradient(
                        colors=[ft.Colors.RED_400, ft.Colors.WHITE], # Muda as cores do gradiente
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
                                    title=ft.Text(nome, color=ft.Colors.BLACK),
                                    subtitle=ft.Text("data", color=ft.Colors.BLACK),
                                    trailing=ft.Text(value="R$ 1000,00", size=24, color=ft.Colors.BLACK )
                                )   
                    )      
                )

