import flet as ft
import datetime
from src.interface.gui.tela_inicio import TelaInicial



class TelaCadastrarDespesa(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.ggg = page
        self.date_picker = ft.DatePicker(
            on_change=self.mudar_data,
            on_dismiss=self.cancelar_data,
            first_date=datetime.datetime(1971, 1, 1),
            last_date=datetime.datetime(2050, 12, 31),
                
        )

        # Adicionamos o seletor à lista de overlays da página
        self.ggg.overlay.append(self.date_picker)

        # 2. Componentes visuais
        self.texto_data = ft.Text("Nenhuma data selecionada")
        self.btn_data = ft.ElevatedButton(
            "Selecionar Data",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda _: self.abrir() # Abre o calendário
        )

        self.controls = [
            ft.Text("Data da Despesa:", weight="bold"),
            self.btn_data,
            self.texto_data
        ]


    def abrir(self):
        self.date_picker.open = True
        self.page.update()
    def cancelar_data(self, e):
        pass   
    def mudar_data(self, e):
        pass  
            

class AppFlet():
    def __init__(self, page: ft.Page):
        self.page = page
        page.window.min_width = 400   # Largura mínima
        page.window.min_height = 200  # Altura mínima
        self.page.title = "Organizador de despesa (DEMO)"
        self.telas = [
                TelaInicial(), # Índice 0
                TelaInicial(),      # Índice 1
                TelaCadastrarDespesa(self.page),        
            ]
        

            # A "Moldura" (Container principal)
        self.container = ft.Container(content=self.telas[0], expand=True)

        # Montamos a página
        self.page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.DASHBOARD, label="Início"),
                ft.NavigationBarDestination(icon=ft.Icons.SETTINGS, label="Ajustes"),
                ft.NavigationBarDestination(icon=ft.Icons.ADD_CIRCLE_OUTLINE, label="Cadastrar despesa")
            ],
            on_change=self.mudar_aba
        )
        
        self.page.add(self.container)

    def mudar_aba(self, e):
        indice = e.control.selected_index
        self.container.content = self.telas[indice]
        self.page.update()

if __name__ == "__main__":
    ft.run(AppFlet)

