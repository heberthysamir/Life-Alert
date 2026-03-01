from domain.usuarios.UsuarioCivil import Civil
from domain.usuarios.UsuarioAtendente import Atendente
from domain.usuarios.UsuarioAgente import Agente

class UsuarioFactory:

    @staticmethod
    def criar(tipo, **dados):
        tipos = {
            "1": Civil,
            "2": Atendente,
            "3": Agente
        }

        classe = tipos.get(tipo)
        if not classe:
            raise ValueError("Tipo de usuário inválido")

        return classe(**dados)
