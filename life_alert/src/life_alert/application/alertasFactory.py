from domain.Alerta import Alerta

class AlertaFactory:
    @staticmethod
    def criar_alerta(titulo, mensagem, ocorrencia, escopo, horario):
        if not ocorrencia:
            raise ValueError("Um alerta precisa estar vinculado a uma ocorrência válida.")
            
        escopos_permitidos = ["cidade", "bairro", "rua"]
        escopo_norm = escopo.lower().strip()
        
        if escopo_norm not in escopos_permitidos:
            raise ValueError(f"Escopo inválido: '{escopo}'. Use: cidade, bairro ou rua.")

        if not titulo or not mensagem:
            raise ValueError("O alerta deve conter um título e uma mensagem de orientação.")

        return Alerta(
            titulo=titulo.strip(),
            mensagem=mensagem.strip(),
            ocorrencia=ocorrencia,
            escopo=escopo_norm,
            horario=horario
        )