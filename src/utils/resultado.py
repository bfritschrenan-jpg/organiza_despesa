from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class Result:
    sucesso: bool
    mensagem: str
    dados: Optional[Any] = None

    @staticmethod
    def ok(dados: Any = None, mensagem: str = "Sucesso"):
        return Result(sucesso=True, mensagem=mensagem, dados=dados)

    @staticmethod
    def erro(mensagem: str):
        return Result(sucesso=False, mensagem=mensagem, dados=None)