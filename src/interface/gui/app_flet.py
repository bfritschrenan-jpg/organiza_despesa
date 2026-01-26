import flet as ft
import datetime
from src.interface.gui.tela_inicio import TelaInicial
from src.interface.gui.tela_cadastrar_despesa import TelaCadastrarDespesa
from src.interface.gui.componentes.data_picker import Gerenciador
from src.interface.gui.servicos.service_interface import GerenciadorDespesaInterface
from src.interface.gui.tela_despesa import TelaDespesa
            

class AppFlet():
    def __init__(self, page: ft.Page):
        self.page = page
        page.window.min_width = 400   # Largura mínima
        page.window.min_height = 200  # Altura mínima
        # Zera o preenchimento da página para o container encostar nas bordas
        page.padding = 0 
        page.spacing = 0
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.title = "Organizador de despesa (DEMO)"

        self.gerenciador_interface = GerenciadorDespesaInterface()
        self.gerenciador = Gerenciador(self.page)
        
        self.telas = [
                TelaInicial(appflet = self), # Índice 0
                TelaInicial(appflet = self),      # Índice 1
                TelaCadastrarDespesa(app_flet=self), # índice 2      
                TelaDespesa(app_flet=self)
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

    def mudar_tela(self, indice): # Índici representa a posição da tela na lista de tela é importante saber qual a poisição para carregar a pagina certa.
        indice = indice
        self.container.content = self.telas[indice]
        self.page.update()

if __name__ == "__main__":
    ft.run(AppFlet)

