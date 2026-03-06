import tkinter as tk
from tkinter import ttk
from application.alertasService import AlertaService 

class CivilScreen:
    @staticmethod
    def render_lista_alertas(gui, container):
        alertas = AlertaService.filtrar_alertas_para_usuario(gui.usuario_logado, gui.db["alertas"])
        
        if not alertas:
            tk.Label(container, text="Nenhum alerta relevante para sua região no momento.", 
                     bg="#f4f7fb", fg="#6b7280", font=("Segoe UI", 10, "italic")).pack(pady=20)
            return

        # 2. Cria um frame de rolagem se houver muitos alertas (opcional, mas recomendado)
        for alerta in alertas:
            card = tk.Frame(container, bg="#ffffff", padx=15, pady=10, highlightthickness=1, highlightbackground="#fee2e2")
            card.pack(fill=tk.X, padx=20, pady=5)
            
            # Título com ícone (ex: 🚨 ALAGAMENTO)
            tk.Label(card, text=f"🚨 {alerta.ocorrencia.tipo.upper()}", bg="#ffffff", 
                     fg="#c53030", font=("Segoe UI", 10, "bold")).pack(anchor="w")
            
            # Mensagem do Alerta
            tk.Label(card, text=alerta.mensagem, bg="#ffffff", wraplength=400, justify="left", font=("Segoe UI", 9)).pack(anchor="w")
            
            # Localização e Escopo
            tk.Label(card, text=f"Local: {alerta.ocorrencia.bairro} ({alerta.escopo.capitalize()})", 
                     bg="#ffffff", fg="#9ca3af", font=("Segoe UI", 8)).pack(anchor="w")
    @staticmethod
    def render_atualizar_dados(gui, container):
        tk.Label(container, text="ATUALIZAR MEUS DADOS", font=gui.font_header, bg="#f4f7fb", fg="#c53030").pack(pady=20)
        card = tk.Frame(container, bg="#ffffff", padx=30, pady=20)
        card.pack(pady=10, padx=50, fill=tk.BOTH)

        campos = [
            ("Nome", "nome", gui.usuario_logado.nome),
            ("Telefone", "telefone", gui.usuario_logado.telefone),
            ("Email", "email", gui.usuario_logado.email),
            ("Senha", "senha", gui.usuario_logado.senha),
            ("Rua", "rua", gui.usuario_logado.rua),
            ("Número", "num", gui.usuario_logado.num),
            ("Bairro", "bairro", gui.usuario_logado.bairro),
            ("Cidade", "cidade", gui.usuario_logado.cidade),
            ("Estado", "estado", gui.usuario_logado.estado)
        ]

        gui.inputs_atualizar = {}
        for i, (label, chave, valor_atual) in enumerate(campos):
            tk.Label(card, text=f"{label}:", bg="#ffffff").grid(row=i, column=0, sticky="w", pady=2)
            ent = ttk.Entry(card, width=40)
            ent.insert(0, valor_atual)
            ent.grid(row=i, column=1, pady=2, padx=10)
            gui.inputs_atualizar[chave] = ent

        tk.Button(card, text="Salvar Alterações", bg="#2b6cb0", fg="white", relief=tk.FLAT,
                  command=gui.confirmar_atualizacao, pady=10).grid(row=len(campos), columnspan=2, sticky="ew", pady=20)
    
    @staticmethod
    def render_excluir_conta(gui, container):
        tk.Label(container, text="EXCLUIR CONTA", font=gui.font_header, bg="#f4f7fb", fg="#c53030").pack(pady=20)
        
        card = tk.Frame(container, bg="#ffffff", padx=40, pady=40)
        card.pack(pady=20)

        tk.Label(card, text="Atenção!\nAo excluir sua conta, todos os seus dados serão removidos.\nDeseja prosseguir?", 
                 bg="#ffffff", justify="center").pack(pady=20)

        tk.Button(card, text="Sim, desejo excluir", bg="#c53030", fg="white", 
                  command=gui.confirmar_exclusao, pady=10).pack(fill=tk.X)

    @staticmethod
    def render_perfil_medico(gui, container):
        tk.Label(container, text="MEU PERFIL MÉDICO", font=gui.font_header, bg="#f4f7fb", fg="#c53030").pack(pady=20)
        card = tk.Frame(container, bg="#ffffff", padx=30, pady=20)
        card.pack(pady=10, padx=50, fill=tk.BOTH)
        
        p_atual = getattr(gui.usuario_logado, 'perfil_medico', None)
        campos = [("Alergias", "alergias"), ("Doenças Crônicas", "doencas"), ("Deficiências", "deficiencia"),
                  ("Tipo Sanguíneo", "tipo_sanguineo"), ("Contatos de Emergência", "contatoEmerg")]

        gui.inputs_perfil = {}
        for i, (label, chave) in enumerate(campos):
            tk.Label(card, text=f"{label}:", bg="#ffffff").grid(row=i, column=0, sticky="w", pady=5)
            ent = ttk.Entry(card, width=40)
            ent.grid(row=i, column=1, pady=5, padx=10)
            if p_atual:
                attr_map = {"tipo_sanguineo": "tipoSanguineo", "contatoEmerg": "contatoEmerg", 
                            "alergias": "alergias", "doencas": "doencas", "deficiencia": "deficiencia"}
                ent.insert(0, getattr(p_atual, attr_map[chave], ""))
            gui.inputs_perfil[chave] = ent

        tk.Button(card, text="Salvar Perfil", bg="#2f855a", fg="white", relief=tk.FLAT,
                  command=gui.salvar_perfil_medico, pady=10).grid(row=len(campos), columnspan=2, sticky="ew", pady=20)
    
    @staticmethod
    def render_criar_ocorrencia(gui, container):
        tk.Label(container, text="ABERTURA DE OCORRÊNCIA", font=gui.font_header, bg="#f4f7fb", fg="#c53030").pack(pady=20)
        
        card = tk.Frame(container, bg="#ffffff", padx=30, pady=20)
        card.pack(pady=10, padx=50, fill=tk.BOTH, expand=True)

        # 1. Múltipla Seleção de Tipos
        tk.Label(card, text="Tipos de Ocorrência:", bg="#ffffff", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        gui.tipos_selecionados = {}
        tipos_disponiveis = ["Policial", "Médica", "Incêndio", "Enchente", "Outros"]
        
        frame_checks = tk.Frame(card, bg="#ffffff")
        frame_checks.grid(row=1, column=0, columnspan=2, sticky="w", pady=5)

        for tipo in tipos_disponiveis:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(frame_checks, text=tipo, variable=var, bg="#ffffff", 
                                 command=gui.atualizar_campos_extras_oc)
            chk.pack(side=tk.LEFT, padx=5)
            gui.tipos_selecionados[tipo] = var

        # 2. Campos Fixos
        campos_fixos = [
            ("Descrição", "descricao"), ("Rua", "rua"), ("Bairro", "bairro"),
            ("Cidade", "cidade"), ("Estado", "estado"), ("Gravidade", "gravidade"),
            ("Pessoas Afetadas", "qtdAfetados")
        ]
        
        gui.inputs_oc = {}
        for i, (label, chave) in enumerate(campos_fixos):
            tk.Label(card, text=f"{label}:", bg="#ffffff").grid(row=i+2, column=0, sticky="w", pady=2)
            ent = ttk.Entry(card, width=33)
            ent.grid(row=i+2, column=1, pady=2, padx=10)
            gui.inputs_oc[chave] = ent

        # 3. Frame para Campos Dinâmicos
        gui.frame_extra_oc = tk.Frame(card, bg="#ffffff")
        gui.frame_extra_oc.grid(row=10, columnspan=2, sticky="ew", pady=10)
        gui.inputs_extras_oc = {}

        # 4. Botão Finalizar
        tk.Button(card, text="Enviar Ocorrência", bg="#c53030", fg="white", relief=tk.FLAT,
                  command=gui.confirmar_ocorrencia, pady=10, cursor="hand2"
                  ).grid(row=11, columnspan=2, sticky="ew", pady=20)

    @staticmethod
    def render_listar_ocorrencias(gui, container):
        tk.Label(container, text="MINHAS OCORRÊNCIAS", font=gui.font_header, bg="#f4f7fb", fg="#c53030").pack(pady=20)
        
        # Filtro de dados
        minhas_ocs = [oc for oc in gui.db["ocorrencias"] if oc.civil == gui.usuario_logado]

        if not minhas_ocs:
            tk.Label(container, text="Nenhuma ocorrência registrada.", bg="#f4f7fb").pack(pady=50)
            return

        frame_tabela = tk.Frame(container, bg="#f4f7fb")
        frame_tabela.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        colunas = ("id", "data", "tipo", "status", "gravidade")
        tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
        
        tabela.heading("id", text="ID")
        tabela.heading("data", text="Data/Hora")
        tabela.heading("tipo", text="Tipo")
        tabela.heading("status", text="Status")
        tabela.heading("gravidade", text="Gravidade")

        for oc in minhas_ocs:
            tabela.insert("", tk.END, values=(oc.id, oc.dataHora, oc.tipo, oc.status.upper(), oc.gravidade))

        scrollbar = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=tabela.yview)
        tabela.configure(yscroll=scrollbar.set)
        
        tabela.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Button(container, text="Ver Detalhes", bg="#c53030", fg="white", relief=tk.FLAT, pady=10,
                  command=lambda: gui.exibir_detalhes_oc_selecionada(tabela, minhas_ocs)
                  ).pack(pady=20)
    
    