import flet as ft
import datetime 
from collections.abc import Callable


class Calendario(ft.DatePicker):
    def __init__(self):
        super().__init__()
        self.first_date=datetime.datetime(1971, 1, 1)
        self.last_date=datetime.datetime(2050, 12, 31)

        self.open=False
        self.on_change = None
        self.help_text="Selecione uma data"
        self.cancel_text="Cancelar"
        self.confirm_text="OK"

        self.error_invalid_text="Data fora do intervalo permitido"
        self.field_label_text="Digite a data"
        self.error_format_text="Formato Inválido"
        self.error_invalid_text="Texto invalido"

        self.current_date=datetime.datetime.now()        # Destaca o dia atual no calendário

        self.date_picker_mode=ft.DatePickerMode.DAY      # Inicia visualizando os dias (pode ser .YEAR)
        self.entry_mode=ft.DatePickerEntryMode.CALENDAR


class Gerenciador():
    def __init__(self, page: ft.Page):
        self.page = page
        self.calendario = Calendario()
        self.page.overlay.append(self.calendario)

    def abrir_calendario(self, on_change: Callable):
        self.calendario.on_change = on_change
        self.calendario.open=True
        self.calendario.update()
        

