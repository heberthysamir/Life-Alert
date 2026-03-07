import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class AtendenteScreen:
    @staticmethod
    def render_gerenciar_atendimentos(gui, container):
        tk.Label(container, text="MEUS ATENDIMENTOS ATIVOS", font=gui.font_header, bg="#f4f7fb", fg="#2b6cb0").pack(pady=20)
        meus_ats = [at for at in gui.db.get("atendimentos", []) if at.atendente == gui.usuario_logado]

        if not meus_ats:
            tk.Label(container, text="Você não possui atendimentos designados no momento.", bg="#f4f7fb").pack(pady=50)
            return

        frame_tabela = tk.Frame(container, bg="#f4f7fb")
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
        
        # No comando do botão "Ver Detalhes/Gerenciar" da lista do atendente:
        tk.Button(container, text="Analisar e Despachar Selecionado", 
                  bg="#2b6cb0", fg="white", pady=10,
                  command=lambda: gui.preparar_analise_atendimento(tabela, meus_ats)
                  ).pack(pady=20)
    
    @staticmethod
    def render_painel_alertas(gui, container):
        tk.Label(container, text="PAINEL DE ALERTAS", font=gui.font_header, bg="#f4f7fb", fg="#c53030").pack(pady=20)
        
        tab_control = ttk.Notebook(container)
        
        # Aba 1: Criar Alerta
        aba_criar = tk.Frame(tab_control, bg="#ffffff", padx=20, pady=20)
        AtendenteScreen._render_aba_criar_alerta(gui, aba_criar)
        
        # Aba 2: Cancelar Alerta
        aba_cancelar = tk.Frame(tab_control, bg="#ffffff", padx=20, pady=20)
        AtendenteScreen._render_aba_cancelar_alerta(gui, aba_cancelar)
        
        tab_control.add(aba_criar, text="Emitir Novo Alerta")
        tab_control.add(aba_cancelar, text="Alertas Ativos")
        tab_control.pack(expand=1, fill="both", padx=20, pady=10)

    @staticmethod
    def _render_aba_criar_alerta(gui, frame):
        tk.Label(frame, text="Selecione uma Ocorrência Base:", bg="#ffffff", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        
        # Combobox com as ocorrências disponíveis
        ocs = gui.db.get("ocorrencias", [])
        lista_oc_str = [f"{i} - {oc.tipo} ({oc.bairro})" for i, oc in enumerate(ocs)]
        
        gui.combo_oc_alerta = ttk.Combobox(frame, values=lista_oc_str, width=50, state="readonly")
        gui.combo_oc_alerta.pack(pady=10)

        tk.Label(frame, text="Título do Alerta:", bg="#ffffff").pack(anchor="w")
        gui.ent_titulo_alerta = ttk.Entry(frame, width=53)
        gui.ent_titulo_alerta.pack(pady=5)

        tk.Label(frame, text="Mensagem de Orientação:", bg="#ffffff").pack(anchor="w")
        gui.txt_msg_alerta = tk.Text(frame, width=40, height=4)
        gui.txt_msg_alerta.pack(pady=5)

        tk.Label(frame, text="Alcance:", bg="#ffffff").pack(anchor="w")
        gui.combo_escopo = ttk.Combobox(frame, values=["cidade", "bairro", "rua"], state="readonly")
        gui.combo_escopo.current(0)
        gui.combo_escopo.pack(pady=5)

        tk.Button(frame, text="DISPARAR ALERTA", bg="#c53030", fg="white", 
                  command=gui.logica_emitir_alerta, pady=10).pack(fill=tk.X, pady=20)

    @staticmethod
    def _render_aba_cancelar_alerta(gui, frame):
        alertas = gui.db.get("alertas", [])
        
        if not alertas:
            tk.Label(frame, text="Não há alertas ativos.", bg="#ffffff").pack(pady=20)
            return

        for i, alerta in enumerate(alertas):
            f = tk.Frame(frame, bg="#fef2f2", pady=5, padx=10)
            f.pack(fill=tk.X, pady=2)
            tk.Label(f, text=f"{alerta.titulo} ({alerta.horario})", bg="#fef2f2").pack(side=tk.LEFT)
            tk.Button(f, text="Cancelar", bg="#fee2e2", fg="#c53030", relief=tk.FLAT,
                      command=lambda idx=i: gui.logica_cancelar_alerta(idx)).pack(side=tk.RIGHT)
    
    @staticmethod
    def render_analisar_atendimento(gui, atendimento, container):
        # Limpa o container
        for widget in container.winfo_children():
            widget.destroy()

        tk.Label(container, text="ANÁLISE E DESPACHO DE OCORRÊNCIA", font=gui.font_header, bg="#f4f7fb", fg="#2b6cb0").pack(pady=20)
        
        # Grid principal para dividir detalhes da ocorrência e formulário de despacho
        main_frame = tk.Frame(container, bg="#f4f7fb")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # COLUNA ESQUERDA: Detalhes (Ocorrência + Civil)
        left_col = tk.Frame(main_frame, bg="#ffffff", padx=15, pady=15, relief=tk.RIDGE, borderwidth=1)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(left_col, text="DADOS DA OCORRÊNCIA", font=("Segoe UI", 10, "bold"), bg="#ffffff").pack(anchor="w")
        detalhes = [
            (f"Civil: {atendimento.civil.nome}"),
            (f"Tipo: {atendimento.ocorrencia.tipo}"),
            (f"Local: {atendimento.ocorrencia.rua}, {atendimento.ocorrencia.bairro}"),
            (f"Descrição: {atendimento.ocorrencia.descricao}"),
            (f"Gravidade Relatada: {atendimento.ocorrencia.gravidade}")
        ]
        # Adiciona campos dinâmicos se existirem
        if hasattr(atendimento.ocorrencia, 'sintomas'): detalhes.append(f"Sintomas: {atendimento.ocorrencia.sintomas}")
        if hasattr(atendimento.ocorrencia, 'tipoCrime'): detalhes.append(f"Crime: {atendimento.ocorrencia.tipoCrime}")
        
        for info in detalhes:
            tk.Label(left_col, text=info, bg="#ffffff", wraplength=350, justify="left").pack(anchor="w", pady=2)

        # COLUNA DIREITA: Ações do Atendente
        right_col = tk.Frame(main_frame, bg="#ffffff", padx=15, pady=15, relief=tk.RIDGE, borderwidth=1)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(right_col, text="DEFINIÇÕES TÉCNICAS", font=("Segoe UI", 10, "bold"), bg="#ffffff").pack(anchor="w")

        # 1. Definir Grau de Urgência
        tk.Label(right_col, text="Grau de Urgência Real:", bg="#ffffff").pack(anchor="w", pady=(10,0))
        gui.ent_urgencia = ttk.Combobox(right_col, values=["baixa", "média", "alta"], state="readonly")
        gui.ent_urgencia.set(atendimento.grauUrgencia)
        gui.ent_urgencia.pack(fill=tk.X, pady=5)

        # 2. Selecionar Equipe (Para o Resgate)
        tk.Label(right_col, text="Designar Equipe de Resgate:", bg="#ffffff").pack(anchor="w", pady=(10,0))
        equipes = gui.db.get("equipes", [])
        nomes_equipes = [f"EQ {eq.id} - {eq.nome}" for eq in equipes]
        gui.ent_equipe_resgate = ttk.Combobox(right_col, values=nomes_equipes, state="readonly")
        gui.ent_equipe_resgate.pack(fill=tk.X, pady=5)

        # 3. Relatório / Complemento
        tk.Label(right_col, text="Relatório/Observações:", bg="#ffffff").pack(anchor="w", pady=(10,0))
        gui.txt_relatorio = tk.Text(right_col, height=4)
        gui.txt_relatorio.pack(fill=tk.X, pady=5)

        # Botão Finalizar e Enviar
        tk.Button(right_col, text="FINALIZAR E ENVIAR RESGATE", bg="#2f855a", fg="white", 
                  font=("Segoe UI", 10, "bold"), command=lambda: gui.processar_despacho_final(atendimento)).pack(fill=tk.X, pady=20)