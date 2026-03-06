class AlertaService:
    @staticmethod
    def filtrar_alertas_para_usuario(usuario, lista_alertas):
        alertas_filtrados = []
        
        for alerta in lista_alertas:
            oc = alerta.ocorrencia
            u_cid = usuario.cidade.lower()
            u_bai = usuario.bairro.lower()
            u_rua = usuario.rua.lower()
            
            o_cid = oc.cidade.lower()
            o_bai = oc.bairro.lower()
            o_rua = oc.rua.lower()

            exibir = False
            if alerta.escopo == "cidade" and o_cid == u_cid:
                exibir = True
            elif alerta.escopo == "bairro" and o_cid == u_cid and o_bai == u_bai:
                exibir = True
            elif alerta.escopo == "rua" and o_cid == u_cid and o_bai == u_bai and o_rua == u_rua:
                exibir = True
            
            if exibir:
                alertas_filtrados.append(alerta)
        
        return alertas_filtrados