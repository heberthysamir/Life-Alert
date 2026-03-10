import tkinter as tk
from tkinter import ttk
from life_alert.application.alertasService import AlertaService 

# Constantes de Estilo
PRIMARY = "#c53030"  
BG = "#f4f7fb"
CARD = "#ffffff"
TEXT = "#243444"
MUTED = "#6b7280"

class CivilScreen:
    @staticmethod
    def render_lista_alertas( gui, container, alertas_db):
        """
        Renderiza os alertas filtrados para o usuário.
        alertas_db: lista de objetos Alerta vindos do repositório.
        """
        # Se não recebeu a lista por argumento, tenta buscar no repositório (segurança)
        if alertas_db is None:
            alertas_db = gui.alerta_repo.listarTodos()
            
        # IMPORTANTE: Use a lista que veio do banco, não gui.db["alertas"]
        from application.alertasService import AlertaService
        alertas = AlertaService.filtrar_alertas_para_usuario(gui.usuario_logado, alertas_db)
        
        # Limpa o container antes de desenhar
        for widget in container.winfo_children():
            widget.destroy()
        
        if not alertas:
            tk.Label(container, text="Nenhum alerta relevante para sua região no momento.", 
                     bg=BG, fg=MUTED, font=("Segoe UI", 10, "italic")).pack(pady=20)
            return

        for alerta in alertas:
            card = tk.Frame(container, bg=CARD, padx=15, pady=10, highlightthickness=1, highlightbackground="#fee2e2")
            card.pack(fill=tk.X, padx=20, pady=5)
            
            # Garantir que temos os dados da ocorrência (mesmo que seja um ID)
            tipo = "ALERTA"
            bairro = "Geral"
            
            # Se o repositório retornar o objeto Ocorrência, pegamos os dados reais
            if hasattr(alerta.ocorrencia, 'tipo'):
                tipo = alerta.ocorrencia.tipo
                bairro = alerta.ocorrencia.bairro
            
            tk.Label(card, text=f"🚨 {tipo.upper()}", bg=CARD, 
                     fg=PRIMARY, font=("Segoe UI", 10, "bold")).pack(anchor="w")
            
            tk.Label(card, text=alerta.mensagem, bg=CARD, wraplength=450, justify="left", font=("Segoe UI", 9)).pack(anchor="w")
            
            tk.Label(card, text=f"Local: {bairro} ({alerta.escopo.capitalize()})", 
                     bg=CARD, fg="#9ca3af", font=("Segoe UI", 8)).pack(anchor="w")

    @staticmethod
    def render_atualizar_dados(gui, container):
        """
        Renderiza o formulário com os dados atuais do usuário para edição.
        Mapeia campos de endereço e contato para atualização no banco de dados.
        """
        tk.Label(container, text="ATUALIZAR MEUS DADOS", font=gui.font_header, bg=BG, fg=PRIMARY).pack(pady=20)
        card = tk.Frame(container, bg=CARD, padx=30, pady=20)
        card.pack(pady=10, padx=50, fill=tk.BOTH)

        campos = [
            ("Nome", "nome", gui.usuario_logado.nome),
            ("Telefone", "telefone", gui.usuario_logado.telefone),
            ("Email", "email", gui.usuario_logado.email),
            ("Senha", "senha", gui.usuario_logado._senha),
            ("Rua", "rua", gui.usuario_logado.rua),
            ("Número", "num", gui.usuario_logado.num),
            ("Bairro", "bairro", gui.usuario_logado.bairro),
            ("Cidade", "cidade", gui.usuario_logado.cidade),
            ("Estado", "estado", gui.usuario_logado.estado)
        ]

        gui.inputs_atualizar = {}
        for i, (label, chave, valor_atual) in enumerate(campos):
            tk.Label(card, text=f"{label}:", bg=CARD).grid(row=i, column=0, sticky="w", pady=2)
            ent = ttk.Entry(card, width=40)
            ent.insert(0, str(valor_atual))
            ent.grid(row=i, column=1, pady=2, padx=10)
            gui.inputs_atualizar[chave] = ent

        tk.Button(card, text="Salvar Alterações", bg="#2b6cb0", fg="white", relief=tk.FLAT,
                  command=gui.confirmar_atualizacao, pady=10, cursor="hand2").grid(row=len(campos), columnspan=2, sticky="ew", pady=20)
    
    @staticmethod
    def render_excluir_conta(gui, container):
        """
        Renderiza o aviso crítico de exclusão de conta.
        Exibe um alerta visual antes de permitir a remoção definitiva do usuário.
        """
        tk.Label(container, text="EXCLUIR CONTA", font=gui.font_header, bg=BG, fg=PRIMARY).pack(pady=20)
        
        card = tk.Frame(container, bg=CARD, padx=40, pady=40)
        card.pack(pady=20)

        tk.Label(card, text="Atenção!\nAo excluir sua conta, todos os seus dados serão removidos.\nDeseja prosseguir?", 
                 bg=CARD, justify="center", font=("Segoe UI", 10)).pack(pady=20)

        tk.Button(card, text="Sim, desejo excluir", bg=PRIMARY, fg="white", relief=tk.FLAT,
                  command=gui.confirmar_exclusao, pady=10, cursor="hand2").pack(fill=tk.X)

    @staticmethod
    def render_perfil_medico(gui, container):
        """
        Renderiza ou edita as informações de saúde do usuário.
        Crucial para que equipes de resgate saibam condições pré-existentes em emergências.
        """
        tk.Label(container, text="MEU PERFIL MÉDICO", font=gui.font_header, bg=BG, fg=PRIMARY).pack(pady=20)
        card = tk.Frame(container, bg=CARD, padx=30, pady=20)
        card.pack(pady=10, padx=50, fill=tk.BOTH)
        
        p_atual = getattr(gui.usuario_logado, 'perfil_medico', None)
        campos = [("Alergias", "alergias"), ("Doenças Crônicas", "doencas"), ("Deficiências", "deficiencia"),
                  ("Tipo Sanguíneo", "tipo_sanguineo"), ("Contatos de Emergência", "contatoEmerg")]

        gui.inputs_perfil = {}
        attr_map = {
            "alergias": "alergias",
            "doencas": "doencas",
            "deficiencia": "deficiencia",
            "tipo_sanguineo": "tipoSanguineo",
            "contatoEmerg": "contatoEmerg"
        }

        for i, (label, chave) in enumerate(campos):
            tk.Label(card, text=f"{label}:", bg=CARD).grid(row=i, column=0, sticky="w", pady=5)
            ent = ttk.Entry(card, width=40)
            ent.grid(row=i, column=1, pady=5, padx=10)
            
            if p_atual:
                valor = getattr(p_atual, attr_map[chave], "")
                ent.insert(0, valor if valor else "")
            
            gui.inputs_perfil[chave] = ent

        tk.Button(card, text="Salvar Perfil", bg="#2f855a", fg="white", relief=tk.FLAT,
                  command=gui.salvar_perfil_medico, pady=10, cursor="hand2").grid(row=len(campos), columnspan=2, sticky="ew", pady=20)
    
    @staticmethod
    def render_criar_ocorrencia(gui, container):
        """
        Renderiza o formulário dinâmico para abertura de socorro.
        Inclui seleção múltipla de tipos e campos fixos de localização e descrição.
        """
        tk.Label(container, text="ABERTURA DE OCORRÊNCIA", font=gui.font_header, bg=BG, fg=PRIMARY).pack(pady=20)
        
        card = tk.Frame(container, bg=CARD, padx=30, pady=20)
        card.pack(pady=10, padx=50, fill=tk.BOTH, expand=True)

        tk.Label(card, text="Tipos de Ocorrência (selecione todos que se aplicam):", 
                 bg=CARD, font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        gui.tipos_selecionados = {}
        tipos_disponiveis = ["Policial", "Médica", "Incêndio", "Enchente", "Outros"]
        
        frame_checks = tk.Frame(card, bg=CARD)
        frame_checks.grid(row=1, column=0, columnspan=2, sticky="w", pady=5)

        for tipo in tipos_disponiveis:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(frame_checks, text=tipo, variable=var, bg=CARD, 
                               activebackground=CARD, command=gui.atualizar_campos_extras_oc)
            chk.pack(side=tk.LEFT, padx=5)
            gui.tipos_selecionados[tipo] = var

        campos_fixos = [
            ("Descrição", "descricao"), ("Rua", "rua"), ("Bairro", "bairro"),
            ("Cidade", "cidade"), ("Estado", "estado"), ("Gravidade", "gravidade"),
            ("Pessoas Afetadas", "qtdAfetados")
        ]
        
        gui.inputs_oc = {}
        for i, (label, chave) in enumerate(campos_fixos):
            tk.Label(card, text=f"{label}:", bg=CARD).grid(row=i+2, column=0, sticky="w", pady=2)
            ent = ttk.Entry(card, width=33)
            ent.grid(row=i+2, column=1, pady=2, padx=10)
            gui.inputs_oc[chave] = ent

        gui.frame_extra_oc = tk.Frame(card, bg=CARD)
        gui.frame_extra_oc.grid(row=10, columnspan=2, sticky="ew", pady=10)

        tk.Button(card, text="Enviar Ocorrência", bg=PRIMARY, fg="white", relief=tk.FLAT,
                  command=gui.confirmar_ocorrencia, pady=10, cursor="hand2"
                  ).grid(row=11, columnspan=2, sticky="ew", pady=20)

    @staticmethod
    def render_listar_ocorrencias(gui, container):
        """
        Lista todas as ocorrências vinculadas ao cidadão logado.
        Utiliza um Treeview para exibição tabular com suporte a rolagem.
        """
        tk.Label(container, text="MINHAS OCORRÊNCIAS", font=gui.font_header, bg=BG, fg=PRIMARY).pack(pady=20)
        
        todas_ocs = gui.ocorrencia_repo.listarTodos()
        print("\n--- DEBUG DE LEITURA ---")
        for oc in todas_ocs:
            print(f"Ocorrência {oc.id} lida do banco -> Civil: {oc.civil} | Atendente: {oc.atendente}")
        print("------------------------\n")
        minhas_ocs = [oc for oc in todas_ocs if oc.civil and oc.civil.cpf == gui.usuario_logado.cpf]

        if not minhas_ocs:
            tk.Label(container, text="Você ainda não registrou nenhuma ocorrência.", 
                    font=("Segoe UI", 10), bg=BG, fg=TEXT).pack(pady=50)
            return

        frame_tabela = tk.Frame(container, bg=BG)
        frame_tabela.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        colunas = ("id", "data", "tipo", "status", "gravidade")
        tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=15)
        
        tabela.heading("id", text="ID")
        tabela.heading("data", text="Data/Hora")
        tabela.heading("tipo", text="Tipo")
        tabela.heading("status", text="Status")
        tabela.heading("gravidade", text="Gravidade")

        tabela.column("id", width=50, anchor="center")
        tabela.column("tipo", width=180, anchor="w")

        for oc in minhas_ocs:
            tabela.insert("", tk.END, values=(oc.id, oc.dataHora, oc.tipo, oc.status.upper(), oc.gravidade))

        scrollbar = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=tabela.yview)
        tabela.configure(yscroll=scrollbar.set)
        tabela.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Button(container, text="Ver Detalhes da Ocorrência Selecionada", 
                bg=PRIMARY, fg="white", relief=tk.FLAT, pady=10, cursor="hand2",
                command=lambda: gui.exibir_detalhes_oc_selecionada(tabela, minhas_ocs)
                ).pack(pady=20)