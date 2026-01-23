from dataclasses import dataclass
from enum import Enum
import datetime

class Status(Enum):
    PAGA = 'paga'
    PENDENTE = 'pendente'
    ATRASADA = 'atrasada'

class Tipo(Enum):
    FIXA = 'fixa'
    PARCELADA = 'parcelada'
    UNICA = 'única'

@dataclass
class Despesa:
    descricao: str
    valor: float
    vencimento: datetime
    status: Status
    tipo: Tipo
    id: int = None
    
    def __post_init__(self):
        # 1. Validação de Valor
        if self.valor <= 0:
            raise ValueError("Error: O valor da despesa deve ser maior que zero.")

        # 2. Validação de Descrição
        if not self.descricao or not self.descricao.strip():
            raise ValueError("Error: A descrição da despesa não pode estar vazia.")

        # 3. Validação de Tipos (Opcional mas recomendada com Enums)
        if not isinstance(self.status, Status):
            raise TypeError("Error: O campo 'status' deve ser uma opção válida do Enum Status.")
        
        if isinstance(self.vencimento, str):
            try:
                # Tenta converter 'AAAA-MM-DD' para objeto datetime
                self.vencimento = datetime.datetime.strptime(self.vencimento, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Erro: Data deve estar no formato AAAA-MM-DD (ex: 2026-01-30)")
        
        # Garante que agora é datetime mesmo
        if not isinstance(self.vencimento, datetime.datetime):
             raise TypeError("Erro: O campo 'vencimento' deve ser um objeto datetime ou string válida.")
        