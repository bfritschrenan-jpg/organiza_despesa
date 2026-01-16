import flet as ft
# Importamos a função que você criou lá na pasta de interface
from src.interface.gui.tela_inicial import InterfacePrincipal


def main(page: ft.Page):
    page.title = "Organizador de Despesas"

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    InterfacePrincipal(page)
    

if __name__ == "__main__":
    # O ft.app inicializa o sistema e chama a sua função de interface
    ft.run(main)
