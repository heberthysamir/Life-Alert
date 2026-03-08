import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
from datetime import datetime
from domain.usuarios.Usuario import Usuario
from domain.Atendimento import Atendimento
from domain.Resgate import Resgate
from application.usuariosFactory import UsuarioFactory
from application.ocorrenciaFactory import OcorrenciaFactory
from application.perfilMedicoFactory import PerfilMedicoFactory
from application.alertasFactory import AlertaFactory
from infrastructure.api.screens.authScreen import AuthScreen
from infrastructure.api.screens.civilSreen import CivilScreen
from infrastructure.api.screens.atendenteScreen import AtendenteScreen
from infrastructure.api.screens.agenteScreen import AgenteScreen

PRIMARY = "#c53030"  
BG = "#f4f7fb"
CARD = "#ffffff"
TEXT = "#243444"
MUTED = "#6b7280"

class LifeAlertGUI:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.usuario_logado = None

        self.root.title("Life Alert")
        self.root.geometry("1000x700")
        self.root.configure(bg=BG)

        self.font_header = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.font_sub = tkfont.Font(family="Segoe UI", size=10)

        self.main_container = tk.Frame(self.root, bg=BG)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Inicia pela tela de login (agora externa)
        AuthScreen.render_login(self)

    def limpar_tela(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    # --- NAVEGAÇÃO E TRANSIÇÕES ---
    def mostrar_tela_login(self):
        self.usuario_logado = None
        AuthScreen.render_login(self)

    def preparar_e_executar(self, comando):
        """Limpa apenas a área de conteúdo antes de carregar uma nova função"""
        for widget in self.area_conteudo.winfo_children():
            widget.destroy()
        comando(self.area_conteudo)

    # --- LÓGICA DE AUTENTICAÇÃO E CADASTRO ---
    def executar_login(self):
        email = self.ent_login_email.get()
        senha = self.ent_login_senha.get()
        
        usuario = None
        for u in self.db["usuarios"]:
            if u.email == email.lower():
                usuario = u
                break
        
        if usuario and usuario.verificar_senha(senha):
            self.usuario_logado = usuario
            messagebox.showinfo("Sucesso", f"Bem-vindo, {usuario.nome}!")
            self.mostrar_dashboard()
        else:
            messagebox.showerror("Erro", "E-mail ou senha incorretos.")

    def executar_cadastro(self):
        try:
            dados = {k.lower(): v.get() for k, v in self.cad_inputs.items()}
            dados["num"] = dados.pop("número")
            
            if self.tipo_selecionado == "2":
                dados["turno"] = self.ent_extra.get()
            elif self.tipo_selecionado == "3":
                dados["cargo"] = self.ent_extra.get()
                dados["status"] = True

            novo_usuario = UsuarioFactory.criar(self.tipo_selecionado, **dados)
            self.db["usuarios"].append(novo_usuario)
            
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.mostrar_tela_login()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cadastrar: {e}")

    # --- DASHBOARD PRINCIPAL ---
    def mostrar_dashboard(self):
        self.limpar_tela()
        
        # Sidebar (Esquerda)
        sidebar = tk.Frame(self.main_container, bg=CARD, width=250)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Conteúdo (Direita) 
        self.area_conteudo = tk.Frame(self.main_container, bg=BG)
        self.area_conteudo.pack(side="right", fill="both", expand=True)
        header_frame = tk.Frame(self.area_conteudo, bg=BG)
        header_frame.pack(fill=tk.X, pady=30, padx=40)

        tk.Label(header_frame, text=f"Bem-vindo, {self.usuario_logado.nome}", 
                 font=self.font_header, bg=BG, fg=TEXT, anchor="w").pack(fill=tk.X)
        tk.Label(header_frame, text=f"Resumo de alertas para {self.usuario_logado.bairro}, {self.usuario_logado.cidade}:", 
                 font=("Segoe UI", 10), bg=BG, fg=MUTED, anchor="w").pack(fill=tk.X)

        # 2. Chamada automática dos Alertas
        # Criamos um sub-container para os alertas para não bagunçar o layout
        alertas_container = tk.Frame(self.area_conteudo, bg=BG)
        alertas_container.pack(fill=tk.BOTH, expand=True, padx=20)
        CivilScreen.render_lista_alertas(self, alertas_container)

        self.usuario_logado.gui_ref = self 
        acoes = self.usuario_logado.obter_funcionalidades()

        for nome_acao, comando in acoes:
            btn = tk.Button(sidebar, text=nome_acao, bg=CARD, fg=TEXT, relief=tk.FLAT,
                            anchor="w", padx=20, pady=12, font=("Segoe UI", 10), cursor="hand2")
            btn.configure(command=lambda c=comando: self.preparar_e_executar(c))
            btn.pack(fill=tk.X)

        tk.Button(sidebar, text="🚪 Sair", bg=CARD, fg=PRIMARY, relief=tk.FLAT, 
                  command=self.mostrar_tela_login).pack(fill=tk.X, side="bottom", pady=20)

        self.label_boas_vindas = tk.Label(self.area_conteudo, text=f"Bem-vindo, {self.usuario_logado.nome}", 
                                         font=self.font_header, bg=BG, fg=MUTED)
        self.label_boas_vindas.pack(pady=100)

    #Telas do civil
    def tela_central_alertas(self, container):
        CivilScreen.render_lista_alertas(self,container)
    def tela_criar_ocorrencia(self, container):
        CivilScreen.render_criar_ocorrencia(self, container)

    def tela_listar_ocorrencias(self, container):
        CivilScreen.render_listar_ocorrencias(self, container)

    def tela_perfil_medico(self, container):
        CivilScreen.render_perfil_medico(self, container)

    def tela_atualizar_dados(self, container):
        CivilScreen.render_atualizar_dados(self, container)

    def tela_excluir_conta(self, container):
        CivilScreen.render_excluir_conta(self, container)
    
    def tela_criar_ocorrencia(self, container):
        CivilScreen.render_criar_ocorrencia(self, container)

    def tela_listar_ocorrencias(self, container):
        CivilScreen.render_listar_ocorrencias(self, container)

    #Telas do Atendente
    def tela_gerenciar_atendimentos(self, container):
        AtendenteScreen.render_gerenciar_atendimentos(self, container)

    def tela_painel_alertas(self, container):
        AtendenteScreen.render_painel_alertas(self, container)
    
    # --- PONTES PARA O AGENTE ---
    def tela_gerenciar_vitimas(self, container):
        from infrastructure.api.screens.agenteScreen import AgenteScreen
        AgenteScreen.render_gerenciar_vitimas(self, container)

    def tela_cadastrar_vitima(self, container):
        from infrastructure.api.screens.agenteScreen import AgenteScreen
        AgenteScreen.render_cadastrar_vitima(self, container)

    def tela_criar_equipe(self, container):
        from infrastructure.api.screens.agenteScreen import AgenteScreen
        AgenteScreen.render_criar_equipe(self, container)

    def tela_menu_equipe(self, container):
        from infrastructure.api.screens.agenteScreen import AgenteScreen
        AgenteScreen.render_menu_equipes(self, container)

    def tela_relatorios(self, container):
        from infrastructure.api.screens.agenteScreen import AgenteScreen
        AgenteScreen.render_relatorios(self, container)
    
    def tela_painel_operacional(self, container):
        from infrastructure.api.screens.agenteScreen import AgenteScreen
        AgenteScreen.render_painel_operacional(self, container)

    def atualizar_campos_extras_oc(self):
        for widget in self.frame_extra_oc.winfo_children():
            widget.destroy()
        self.inputs_extras_oc = {}
        linha = 0

        if self.tipos_selecionados["Policial"].get():
            tk.Label(self.frame_extra_oc, text="--- DETALHES POLICIAIS ---", fg="#c53030", bg="#ffffff", font=("Segoe UI", 8, "bold")).grid(row=linha, columnspan=2, pady=5)
            linha += 1
            self.criar_campo_extra("Tipo de Crime", "tipoCrime", linha); linha += 1
            self.criar_campo_extra("Qtd Criminosos", "qtdCriminosos", linha); linha += 1
            self.criar_campo_extra("Descrição Suspeito", "descricaoSuspeito", linha); linha += 1

        if self.tipos_selecionados["Médica"].get():
            tk.Label(self.frame_extra_oc, text="--- DETALHES MÉDICOS ---", fg="#c53030", bg="#ffffff", font=("Segoe UI", 8, "bold")).grid(row=linha, columnspan=2, pady=5)
            linha += 1
            self.criar_campo_extra("Sintomas Atuais", "sintomas", linha); linha += 1
            tk.Label(self.frame_extra_oc, text="ℹ️ Seu perfil médico será enviado automaticamente.", 
                     fg="#6b7280", bg="#ffffff", font=("Segoe UI", 8, "italic")).grid(row=linha, columnspan=2)

    def criar_campo_extra(self, label, chave, row):
        tk.Label(self.frame_extra_oc, text=f"{label}:", bg="#ffffff").grid(row=row, column=0, sticky="w", pady=2)
        ent = ttk.Entry(self.frame_extra_oc, width=33)
        ent.grid(row=row, column=1, pady=2, padx=10)
        self.inputs_extras_oc[chave] = ent

    def confirmar_ocorrencia(self):
        # 1. Validação de seleção
        selecionados = [tipo for tipo, var in self.tipos_selecionados.items() if var.get()]
        
        if not selecionados:
            messagebox.showwarning("Aviso", "Selecione pelo menos um tipo de ocorrência!")
            return

        # 2. Lógica de Perfil Médico (Sua lógica original preservada)
        dados_perfil = None
        if "Médica" in selecionados:
            perfil = getattr(self.usuario_logado, 'perfil_medico', None)
            if perfil is None:
                if not messagebox.askyesno("Perfil Médico Ausente", "Enviar mesmo sem perfil médico?"):
                    self.preparar_e_executar(lambda container: self.tela_perfil_medico(container))
                    return 
                dados_perfil = "Não cadastrado pelo usuário."
            else:
                dados_perfil = str(perfil)

        try:
            # 3. Coleta de dados dos inputs
            dados = {k: v.get() for k, v in self.inputs_oc.items()}
            dados.update({k: v.get() for k, v in self.inputs_extras_oc.items()})
            
            # Definição do ID do Tipo para a Factory
            mapa_map = {"Policial": "1", "Médica": "2", "Incêndio": "3", "Enchente": "4", "Outros": "5"}
            id_tipo_principal = "2" if "Médica" in selecionados else mapa_map[selecionados[0]]

            # 4. Preparação dos dados para a Factory
            # CORREÇÃO: Garantindo que Agente/Equipe iniciem como None ou string vazia com segurança
            dados.update({
                "civil": self.usuario_logado,
                "dataHora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "Aberta",
                "tipo": ", ".join(selecionados),
                "perfilMedico": dados_perfil,
                "atendente": None, 
                "agente": None,    # Corrigido: Inicializa explicitamente como None
                "equipe": None,    # Corrigido: Inicializa explicitamente como None
            })

            # 5. Criação da Ocorrência
            nova_oc = OcorrenciaFactory.criar(id_tipo_principal, **dados)
            self.db["ocorrencias"].append(nova_oc)

            # 6. INTEGRAÇÃO: DESIGNAR ATENDENTE AUTOMATICAMENTE
            from application.atendimentoService import AtendimentoService
            atendente_escolhido = AtendimentoService.designarAtendente(
                nova_oc, 
                self.db["usuarios"], 
                self.db.get("atendimentos", [])
            )

            if atendente_escolhido:
                # Criar o objeto Atendimento (já que você não tem Factory para isso)
                novo_atendimento = Atendimento(
                    atendente=atendente_escolhido,
                    ocorrencia=nova_oc,
                    horaInicio=dados["dataHora"]
                )
                
                # Inicializa a lista de atendimentos se não existir no "DB"
                if "atendimentos" not in self.db:
                    self.db["atendimentos"] = []
                self.db["atendimentos"].append(novo_atendimento)
                
                nova_oc.status = "Em Atendimento"
                nova_oc.atendente = atendente_escolhido
                
                msg_sucesso = f"Ocorrência registrada!\nAtendente {atendente_escolhido.nome} foi designado."
            else:
                msg_sucesso = "Ocorrência registrada! Aguardando atendente disponível."

            messagebox.showinfo("Sucesso", msg_sucesso)
            self.mostrar_dashboard()

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao registrar ocorrência: {e}")

    def confirmar_atualizacao(self):
        try:
            self.usuario_logado.atualizarUsuario(
                novo_nome=self.inputs_atualizar["nome"].get(),
                novo_telefone=self.inputs_atualizar["telefone"].get(),
                novo_email=self.inputs_atualizar["email"].get(),
                nova_senha=self.inputs_atualizar["senha"].get(),
                nova_rua=self.inputs_atualizar["rua"].get(),
                novo_num=self.inputs_atualizar["num"].get(),
                novo_bairro=self.inputs_atualizar["bairro"].get(),
                nova_cidade=self.inputs_atualizar["cidade"].get(),
                novo_estado=self.inputs_atualizar["estado"].get()
            )
            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
            self.mostrar_dashboard()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar: {e}")

    def confirmar_exclusao(self):
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir sua conta permanentemente?"):
            sucesso = self.usuario_logado.excluirUsuario(self.db["usuarios"])
            if sucesso:
                messagebox.showinfo("Encerrado", "Conta excluída com sucesso.")
                self.mostrar_tela_login()
            else:
                messagebox.showerror("Erro", "Não foi possível excluir a conta.")
                
    def exibir_detalhes_oc_selecionada(self, tabela, lista_ocs):
            item_selecionado = tabela.selection()
            if not item_selecionado:
                messagebox.showwarning("Aviso", "Selecione uma ocorrência na lista primeiro!")
                return

            # Busca o objeto original
            valores = tabela.item(item_selecionado)['values']
            id_oc = valores[0]
            oc = next((o for o in lista_ocs if o.id == id_oc), None)
            
            if oc:
                # Limpa o container para desenhar os detalhes
                for widget in self.area_conteudo.winfo_children():
                    widget.destroy()

                # Título e Botão Voltar
                header_frame = tk.Frame(self.area_conteudo, bg=BG)
                header_frame.pack(fill=tk.X, padx=20, pady=10)
                
                tk.Button(header_frame, text="← Voltar para Lista", bg=CARD, fg=PRIMARY, 
                        command=lambda: self.preparar_e_executar(self.usuario_logado.obter_funcionalidades()[4][1])).pack(side=tk.LEFT)
                
                tk.Label(self.area_conteudo, text=f"DETALHES DA OCORRÊNCIA #{oc.id}", 
                        font=self.font_header, bg=BG, fg=PRIMARY).pack(pady=10)

                # Card de Informações
                card = tk.Frame(self.area_conteudo, bg=CARD, padx=30, pady=20)
                card.pack(pady=10, padx=50, fill=tk.BOTH)

                info = [
                    ("Status", oc.status),
                    ("Data/Hora", oc.dataHora),
                    ("Tipo", oc.tipo),
                    ("Endereço", f"{oc.rua}, {oc.bairro}, {oc.cidade}"),
                    ("Descrição", oc.descricao),
                    ("Gravidade", oc.gravidade)
                ]

                # Adiciona informações dinâmicas (Crime/Médico)
                if hasattr(oc, 'tipoCrime') and oc.tipoCrime:
                    info.append(("Tipo de Crime", oc.tipoCrime))
                if hasattr(oc, 'sintomas') and oc.sintomas:
                    info.append(("Sintomas", oc.sintomas))
                if hasattr(oc, 'perfilMedico') and oc.perfilMedico:
                    info.append(("Perfil Médico", oc.perfilMedico))

                # Renderiza os labels no card
                for i, (label, valor) in enumerate(info):
                    tk.Label(card, text=f"{label}:", bg=CARD, font=("Segoe UI", 10, "bold")).grid(row=i, column=0, sticky="w", pady=5)
                    tk.Label(card, text=valor, bg=CARD, font=("Segoe UI", 10), wraplength=400, justify="left").grid(row=i, column=1, sticky="w", padx=10, pady=5)

                # Informações do Atendimento (se houver)
                atendimento = next((a for a in self.db.get("atendimentos", []) if a.ocorrencia == oc), None)
                if atendimento:
                    tk.Frame(card, height=1, bg=BG).grid(row=len(info), columnspan=2, sticky="ew", pady=10)
                    tk.Label(card, text="INFORMAÇÕES DE ATENDIMENTO", bg=CARD, fg=MUTED, font=("Segoe UI", 9, "bold")).grid(row=len(info)+1, columnspan=2, sticky="w")
                    
                    at_info = [
                        ("Atendente", atendimento.atendente.nome),
                        ("Início", atendimento.horaInicio), # Atributo da sua classe
                        ("Urgência", atendimento.grauUrgencia) # Atributo da sua classe
                    ]
                    
                    for i, (label, valor) in enumerate(at_info):
                        row = len(info) + 2 + i
                        tk.Label(card, text=f"{label}:", bg=CARD, font=("Segoe UI", 10, "bold")).grid(row=row, column=0, sticky="w", pady=5)
                        tk.Label(card, text=valor, bg=CARD).grid(row=row, column=1, sticky="w", padx=10)
    
    def salvar_perfil_medico(self):
        try:

            dados = {
                "alergias": self.inputs_perfil["alergias"].get(),
                "doencas": self.inputs_perfil["doencas"].get(),
                "deficiencia": self.inputs_perfil["deficiencia"].get(),
                "tipo_sanguineo": self.inputs_perfil["tipo_sanguineo"].get(),
                "contatoEmerg": self.inputs_perfil["contatoEmerg"].get()
            }
            novo_perfil = PerfilMedicoFactory.criar(**dados)
            self.usuario_logado.perfil_medico = novo_perfil
            
            messagebox.showinfo("Sucesso", "Perfil médico atualizado com sucesso!")
            self.mostrar_dashboard() # Volta para a tela inicial do sistema
            
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar o perfil: {e}")
    
    def logica_emitir_alerta(self):
        try:
            idx_combo = self.combo_oc_alerta.current()
            if idx_combo == -1: raise Exception("Selecione uma ocorrência.")

            oc_base = self.db["ocorrencias"][idx_combo]
            
            dados = {
                "titulo": self.ent_titulo_alerta.get(),
                "mensagem": self.txt_msg_alerta.get("1.0", tk.END).strip(),
                "ocorrencia": oc_base,
                "escopo": self.combo_escopo.get(),
                "horario": datetime.now().strftime("%H:%M:%S")
            }

            novo_alerta = AlertaFactory.criar_alerta(**dados)
            self.db["alertas"].append(novo_alerta)
            messagebox.showinfo("Sucesso", "Alerta disparado para a população!")
            self.mostrar_dashboard()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def logica_cancelar_alerta(self, indice):
        if messagebox.askyesno("Confirmar", "Deseja cancelar este alerta?"):
            self.db["alertas"].pop(indice)
            self.mostrar_dashboard()

    def logica_atualizar_atendimento(self, tabela, lista_atendimentos):
        item_selecionado = tabela.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um atendimento!")
            return

        valores = tabela.item(item_selecionado)['values']
        id_at = valores[0]
        at_obj = next((a for a in lista_atendimentos if a.id == id_at), None)

        if at_obj:
            # Se você quiser apenas mudar a urgência como no seu método atualizarAtendimento:
            novo_grau = "alta" # Exemplo: você pode abrir um simpledialog para isso
            at_obj.alterarUrgencia(novo_grau)
            
            # Se o objetivo for finalizar o atendimento:
            at_obj.encerrarAtendimento()
            
            messagebox.showinfo("Sucesso", "Atendimento atualizado!")
            self.mostrar_dashboard()

    def preparar_analise_atendimento(self, tabela, lista_ats):
            item_selecionado = tabela.selection()
            if not item_selecionado:
                messagebox.showwarning("Aviso", "Selecione um atendimento na lista!")
                return

            # Pega o ID da linha selecionada
            valores = tabela.item(item_selecionado)['values']
            id_at = valores[0]
            
            # Busca o objeto Atendimento correspondente
            atendimento = next((at for at in lista_ats if at.id == id_at), None)
            
            if atendimento:
                from infrastructure.api.screens.atendenteScreen import AtendenteScreen
                # Abre a tela de detalhes e despacho que criamos
                AtendenteScreen.render_analisar_atendimento(self, atendimento, self.area_conteudo)

    def processar_despacho_final(self, atendimento):
        try:
            # Coleta dados da interface (Comboboxes e Text)
            urgencia = self.ent_urgencia.get()
            relatorio = self.txt_relatorio.get("1.0", tk.END).strip()
            idx_equipe = self.ent_equipe_resgate.current()

            if not urgencia or idx_equipe == -1:
                messagebox.showwarning("Aviso", "Preencha a urgência e selecione uma equipe!")
                return

            # 1. Atualiza atributos do atendimento (conforme sua classe Atendimento)
            atendimento.grauUrgencia = urgencia
            atendimento.ocorrencia.complemento = relatorio
            
            # 2. Lógica de Resgate (conforme sua classe Atendimento)
            equipe_sel = self.db["equipes"][idx_equipe]
            
            # Atualiza agentes da equipe
            if hasattr(equipe_sel, 'agentes'):
                for agente in equipe_sel.agentes:
                    agente.status = "Em ocorrência"
            
            equipe_sel.status = "Em ocorrência"
            atendimento.ocorrencia.equipe = equipe_sel
            atendimento.ocorrencia.status = "Encaminhada para Resgate"

            # 3. Finaliza o atendimento (grava horaFinal e move para lista de concluídos)
            if "atendimentos_concluidos" not in self.db:
                self.db["atendimentos_concluidos"] = []
            
            atendimento.finalizarAtendimento(self.db["atendimentos_concluidos"])
            
            # Remove da lista de ativos para não poluir a tabela
            if atendimento in self.db.get("atendimentos", []):
                self.db["atendimentos"].remove(atendimento)

            messagebox.showinfo("Sucesso", f"Ocorrência #{atendimento.ocorrencia.id} despachada com sucesso!")
            self.mostrar_dashboard()

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao processar despacho: {e}")

    def logica_iniciar_resgate_direto(self, ocorrencia, container):
        """Altera o status da ocorrência para 'Em Resgate' e atualiza a tela"""
        try:
            ocorrencia.status = "Em Resgate"
            # Se a equipe estiver vinculada, atualiza o status dela também
            if ocorrencia.equipe:
                ocorrencia.equipe.status = "Em atendimento"
                for agente in ocorrencia.equipe.agentes:
                    agente.status = "Em ocorrência"
            
            messagebox.showinfo("Sucesso", f"Resgate iniciado para a Ocorrência #{ocorrencia.id}")
            
            # Recarrega a tela atual para atualizar os botões
            from infrastructure.api.screens.agenteScreen import AgenteScreen
            AgenteScreen.render_painel_operacional(self, container)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível iniciar o resgate: {e}")

    def logica_concluir_resgate_direto(self, ocorrencia, relato, total_vitimas):
        try:
            # 1. Validação de Vítimas Perdidas
            v_perdidas = [v for v in self.db.get("vitimas", []) 
                        if v.ocorrencia.id == ocorrencia.id and v.situacao == "Perdido"]
            if v_perdidas:
                return messagebox.showerror("Erro", "Há vítimas com status 'Perdido'. Resolva antes de fechar.")
            
            agora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            
            novo_resgate = Resgate(
                id=None, 
                ocorrencia=ocorrencia,
                dataInicio=ocorrencia.dataHora, 
                descricao=relato,
                dataFim=agora,
                qtdResgatados=total_vitimas
            )
            
            if "resgates_historico" not in self.db: 
                self.db["resgates_historico"] = []
            self.db["resgates_historico"].append(novo_resgate)

            # 3. Atualiza Status da Ocorrência e Equipe
            ocorrencia.status = "Finalizada"
            ocorrencia.hora_finalizado = agora 
            
            if ocorrencia.equipe:
                ocorrencia.equipe.status = "Disponível"
                for ag in ocorrencia.equipe.agentes:
                    ag.status = "Disponível"

            messagebox.showinfo("Sucesso", "Resgate finalizado e histórico salvo!")
            self.mostrar_dashboard()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao fechar resgate: {e}")
            
    def logica_salvar_vitima(self, nome, situacao, oc_str):
        if not nome or not situacao or not oc_str:
            return messagebox.showerror("Erro", "Preencha todos os campos")
        
        try:
            id_oc = int(oc_str.split(" - ")[0])
            oc = next(o for o in self.db["ocorrencias"] if o.id == id_oc)
            
            # Aqui você chamaria sua VitimaFactory.criar(...)
            # nova_v = VitimaFactory.criar(nome, "N/A", situacao, oc)
            # self.db["vitimas"].append(nova_v)
            
            messagebox.showinfo("Sucesso", f"Vítima {nome} vinculada à ocorrência #{id_oc}")
            self.mostrar_dashboard()
        except Exception as e:
            messagebox.showerror("Erro", str(e))