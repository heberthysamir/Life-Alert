class AtendimentoService:
    @staticmethod
    def designarAtendente(ocorrencia, lista_usuarios, lista_atendimentos):
        atendentesLocais = [
            u for u in lista_usuarios
            if u.tipo == "Atendente" and u.cidade.lower() == ocorrencia.cidade.lower()
        ]
        if not atendentesLocais:
            return None

        return min(
            atendentesLocais, 
            key=lambda at: len([a for a in lista_atendimentos if a.atendente == at])
        )