import flet as ft

class TelaInicial(ft.Column):
    def __init__(self):
        super().__init__()
        
        self.controls = [
            ft.ResponsiveRow([
                ft.ShaderMask(
                    # O segredo está aqui: o atributo 'col'
                    # 'xs': 12 significa que em telas pequenas ocupa tudo.
                    # 'md': 12 significa que em telas médias também ocupa tudo.
                    col={"xs": 12, "md": 12},

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
            ], alignment=ft.MainAxisAlignment.CENTER)
        ]