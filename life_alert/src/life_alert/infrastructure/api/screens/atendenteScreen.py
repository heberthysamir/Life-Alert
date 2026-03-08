import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Constantes de Estilo para consistência visual
PRIMARY = "#c53030"    
SECONDARY = "#2b6cb0"  
SUCCESS = "#2f855a"    
BG = "#f4f7fb"         
CARD = "#ffffff"       
TEXT = "#243444"       
MUTED = "#6b7280"

class AtendenteScreen:
    @staticmethod
    def render_gerenciar_atendimentos(gui, container):
        """
        Lista todos os atendimentos vinculados ao atendente logado.
        Permite selecionar um atendimento para análise técnica e despacho.
        """
        tk.Label(container, text="MEUS ATENDIMENTOS ATIVOS", font=gui.font_header, bg=BG, fg=SECONDARY).pack(pady=20)
        
        meus_ats = [at for at in gui.db.get("atendimentos", []) if at.atendente == gui.usuario_logado]

        if not meus_ats:
            tk.Label(container, text="Você não possui atendimentos designados no momento.", bg=BG, fg=TEXT).pack(pady=50)
            return

        frame_tabela = tk.Frame(container, bg=BG)
        frame_tabela.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        colunas = ("id", "ocorrencia", "status", "inicio")
        tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
        
        tabela.heading("id", text="ID")
        tabela.heading("ocorrencia", text="Ocorrência")
        tabela.heading("status", text="Status")
        tabela.heading("inicio", text="Início")

        for at in meus_ats:
            tabela.insert("", tk.END, values=(at.id, at.ocorrencia.tipo, at.ocorrencia.status, at.horaInicio))

        tabela.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Button(container, text="Analisar e Despachar Selecionado", 
                  bg=SECONDARY, fg="white", pady=10, relief=tk.FLAT, cursor="hand2",
                  command=lambda: gui.preparar_analise_atendimento(tabela, meus_ats)
                  ).pack(pady=20)
    
    @staticmethod
    def render_painel_alertas(gui, container):
        """
        Interface central de alertas com abas (Notebook).
        Permite a emissão de novos alertas baseados em ocorrências ou cancelamento de alertas ativos.
        """
        tk.Label(container, text="PAINEL DE ALERTAS", font=gui.font_header, bg=BG, fg=PRIMARY).pack(pady=20)
        
        tab_control = ttk.Notebook(container)
        
        # Aba 1: Criar Alerta
        aba_criar = tk.Frame(tab_control, bg=CARD, padx=20, pady=20)
        AtendenteScreen._render_aba_criar_alerta(gui, aba_criar)
        
        # Aba 2: Cancelar Alerta
        aba_cancelar = tk.Frame(tab_control, bg=CARD, padx=20, pady=20)
        AtendenteScreen._render_aba_cancelar_alerta(gui, aba_cancelar)
        
        tab_control.add(aba_criar, text="Emitir Novo Alerta")
        tab_control.add(aba_cancelar, text="Alertas Ativos")
        tab_control.pack(expand=1, fill="both", padx=20, pady=10)

    @staticmethod
    def _render_aba_criar_alerta(gui, frame):
        """Formulário interno para configuração e disparo de alertas em massa."""
        tk.Label(frame, text="Selecione uma Ocorrência Base:", bg=CARD, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        
        todas_ocs = gui.db.get("ocorrencias", [])
        cidade_atendente = gui.usuario_logado.cidade.strip().lower()
        
        # Filtra apenas ocorrências da mesma cidade do atendente
        ocs_disponiveis = [
            (i, oc) for i, oc in enumerate(todas_ocs) 
            if oc.status != "Finalizada" and oc.cidade.strip().lower() == cidade_atendente
        ]

        lista_oc_str = [f"{i} - {oc.tipo} ({oc.bairro}) | Status: {oc.status}" for i, oc in ocs_disponiveis]
        
        gui.combo_oc_alerta = ttk.Combobox(frame, values=lista_oc_str, width=50, state="readonly")
        gui.combo_oc_alerta.pack(pady=10)

        if not lista_oc_str:
            gui.combo_oc_alerta.set("Nenhuma ocorrência ativa para gerar alertas")

        tk.Label(frame, text="Título do Alerta:", bg=CARD).pack(anchor="w")
        gui.ent_titulo_alerta = ttk.Entry(frame, width=53)
        gui.ent_titulo_alerta.pack(pady=5)

        tk.Label(frame, text="Mensagem de Orientação:", bg=CARD).pack(anchor="w")
        gui.txt_msg_alerta = tk.Text(frame, width=40, height=4)
        gui.txt_msg_alerta.pack(pady=5)

        tk.Label(frame, text="Alcance:", bg=CARD).pack(anchor="w")
        gui.combo_escopo = ttk.Combobox(frame, values=["cidade", "bairro", "rua"], state="readonly")
        gui.combo_escopo.current(0)
        gui.combo_escopo.pack(pady=5)

        tk.Button(frame, text="DISPARAR ALERTA", bg=PRIMARY, fg="white", relief=tk.FLAT,
                  command=gui.logica_emitir_alerta, pady=10, cursor="hand2").pack(fill=tk.X, pady=20)

    @staticmethod
    def _render_aba_cancelar_alerta(gui, frame):
        """Lista alertas ativos e permite sua remoção do sistema."""
        alertas = gui.db.get("alertas", [])
        
        if not alertas:
            tk.Label(frame, text="Não há alertas ativos.", bg=CARD, fg=TEXT).pack(pady=20)
            return

        for i, alerta in enumerate(alertas):
            f = tk.Frame(frame, bg="#fef2f2", pady=5, padx=10)
            f.pack(fill=tk.X, pady=2)
            tk.Label(f, text=f"{alerta.titulo} ({alerta.horario})", bg="#fef2f2").pack(side=tk.LEFT)
            tk.Button(f, text="Cancelar", bg="#fee2e2", fg=PRIMARY, relief=tk.FLAT, cursor="hand2",
                      command=lambda idx=i: gui.logica_cancelar_alerta(idx)).pack(side=tk.RIGHT)
    
    @staticmethod
    def render_analisar_atendimento(gui, atendimento, container):
        """
        Interface detalhada para despacho. 
        Exibe dados do solicitante e permite definir urgência real e designar equipes de resgate.
        """
        for widget in container.winfo_children():
            widget.destroy()

        tk.Label(container, text="ANÁLISE E DESPACHO DE OCORRÊNCIA", font=gui.font_header, bg=BG, fg=SECONDARY).pack(pady=20)
        
        main_frame = tk.Frame(container, bg=BG)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # COLUNA ESQUERDA: Detalhes
        left_col = tk.Frame(main_frame, bg=CARD, padx=15, pady=15, relief=tk.RIDGE, borderwidth=1)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(left_col, text="DADOS DA OCORRÊNCIA", font=("Segoe UI", 10, "bold"), bg=CARD).pack(anchor="w")
        detalhes = [
            (f"Civil: {atendimento.civil.nome}"),
            (f"Tipo: {atendimento.ocorrencia.tipo}"),
            (f"Local: {atendimento.ocorrencia.rua}, {atendimento.ocorrencia.bairro}"),
            (f"Descrição: {atendimento.ocorrencia.descricao}"),
            (f"Gravidade Relatada: {atendimento.ocorrencia.gravidade}")
        ]
        
        if hasattr(atendimento.ocorrencia, 'sintomas'): detalhes.append(f"Sintomas: {atendimento.ocorrencia.sintomas}")
        if hasattr(atendimento.ocorrencia, 'tipoCrime'): detalhes.append(f"Crime: {atendimento.ocorrencia.tipoCrime}")
        
        for info in detalhes:
            tk.Label(left_col, text=info, bg=CARD, wraplength=350, justify="left").pack(anchor="w", pady=2)

        # COLUNA DIREITA: Ações
        right_col = tk.Frame(main_frame, bg=CARD, padx=15, pady=15, relief=tk.RIDGE, borderwidth=1)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(right_col, text="DEFINIÇÕES TÉCNICAS", font=("Segoe UI", 10, "bold"), bg=CARD).pack(anchor="w")

        tk.Label(right_col, text="Grau de Urgência Real:", bg=CARD).pack(anchor="w", pady=(10,0))
        gui.ent_urgencia = ttk.Combobox(right_col, values=["baixa", "média", "alta"], state="readonly")
        gui.ent_urgencia.set(atendimento.grauUrgencia)
        gui.ent_urgencia.pack(fill=tk.X, pady=5)

        tk.Label(right_col, text="Designar Equipe de Resgate:", bg=CARD).pack(anchor="w", pady=(10,0))
        equipes_todas = gui.db.get("equipes", [])
        cidade_atendente = gui.usuario_logado.cidade.strip().lower()
        
        equipes_filtradas = [
            eq for eq in equipes_todas 
            if hasattr(eq, 'localidade') and eq.localidade.strip().lower() == cidade_atendente
        ]
        nomes_equipes = [f"ID: {eq.id} | {eq.setor} - {eq.especialidade}" for eq in equipes_filtradas]
        gui.ent_equipe_resgate = ttk.Combobox(right_col, values=nomes_equipes, state="readonly")
        gui.ent_equipe_resgate.pack(fill=tk.X, pady=5)

        if not nomes_equipes:
            gui.ent_equipe_resgate.set("Nenhuma equipe disponível na sua cidade")

        tk.Label(right_col, text="Relatório/Observações:", bg=CARD).pack(anchor="w", pady=(10,0))
        gui.txt_relatorio = tk.Text(right_col, height=4)
        gui.txt_relatorio.pack(fill=tk.X, pady=5)

        tk.Button(right_col, text="FINALIZAR E ENVIAR RESGATE", bg=SUCCESS, fg="white", relief=tk.FLAT,
                  font=("Segoe UI", 10, "bold"), command=lambda: gui.processar_despacho_final(atendimento), cursor="hand2").pack(fill=tk.X, pady=20)
        
    @staticmethod
    def render_gerenciar_membros_equipe(gui, container, equipe):
        """
        Interface para gestão de recursos humanos da equipe. 
        Permite que o atendente adicione ou remova agentes de resgate da equipe selecionada.
        """
        for w in container.winfo_children(): w.destroy()
        
        tk.Label(container, text=f"MEMBROS DA EQUIPE #{equipe.id}", font=gui.font_header, bg=BG, fg=TEXT).pack(pady=20)

        main_frame = tk.Frame(container, bg=BG)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # COLUNA ESQUERDA: Membros Atuais
        left_col = tk.Frame(main_frame, bg=CARD, padx=15, pady=15, relief=tk.RIDGE, borderwidth=1)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        tk.Label(left_col, text="Membros Atuais", font=("Segoe UI", 10, "bold"), bg=CARD).pack()
        
        for agente in equipe.agentes:
            f = tk.Frame(left_col, bg=CARD)
            f.pack(fill=tk.X, pady=2)
            tk.Label(f, text=f"{agente.nome} ({agente.cargo})", bg=CARD).pack(side=tk.LEFT)
            tk.Button(f, text="X", fg=PRIMARY, bg=CARD, relief=tk.FLAT, cursor="hand2",
                      command=lambda a=agente: gui.logica_remover_agente(gui, container, equipe, a)).pack(side=tk.RIGHT)

        # COLUNA DIREITA: Adicionar Novos
        right_col = tk.Frame(main_frame, bg=CARD, padx=15, pady=15, relief=tk.RIDGE, borderwidth=1)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
        tk.Label(right_col, text="Agentes Disponíveis", font=("Segoe UI", 10, "bold"), bg=CARD).pack()

        todos_usuarios = gui.db.get("usuarios", [])
        disponiveis = [u for u in todos_usuarios if u.tipo == "Agente" and u not in equipe.agentes]

        if not disponiveis:
            tk.Label(right_col, text="Nenhum agente disponível.", bg=CARD, fg=MUTED).pack(pady=20)
        else:
            for ag in disponiveis:
                f = tk.Frame(right_col, bg=CARD)
                f.pack(fill=tk.X, pady=2)
                tk.Label(f, text=f"{ag.nome} ({ag.cargo})", bg=CARD).pack(side=tk.LEFT)
                tk.Button(f, text="+ Adicionar", bg=SUCCESS, fg="white", font=("Segoe UI", 8), relief=tk.FLAT, cursor="hand2",
                          command=lambda a=ag: gui.logica_adicionar_agente(gui, container, equipe, a)).pack(side=tk.RIGHT)

        tk.Button(container, text="Voltar", command=lambda: gui.render_menu_equipes(gui, container)).pack(pady=20)

    @staticmethod
    def logica_adicionar_agente(gui, container, equipe, agente):
        equipe.adicionar_membro(agente) 
        messagebox.showinfo("Sucesso", f"{agente.nome} adicionado à equipe!")
        gui.render_gerenciar_membros_equipe(gui, container, equipe)

    @staticmethod
    def logica_remover_agente(gui, container, equipe, agente):
        if messagebox.askyesno("Confirmar", f"Remover {agente.nome} da equipe?"):
            equipe.remover_membro(agente.id) 
            messagebox.showinfo("Sucesso", "Membro removido.")
            gui.render_gerenciar_membros_equipe(gui, container, equipe)
