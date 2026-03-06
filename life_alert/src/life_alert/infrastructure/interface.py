import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
from datetime import datetime
from domain.usuarios.Usuario import Usuario
from application.usuariosFactory import UsuarioFactory
from application.ocorrenciaFactory import OcorrenciaFactory
from application.perfilMedicoFactory import PerfilMedicoFactory

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
        self.root.geometry("900x640")
        self.root.configure(bg=BG)

        self.font_header = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.font_sub = tkfont.Font(family="Segoe UI", size=10)

        self.main_container = tk.Frame(self.root, bg=BG)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        self.mostrar_tela_login()

    def limpar_tela(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def configurar_scroll_dinamico(self, canvas, window_id):
        def redimensionar(event):
            canvas.itemconfig(window_id, width=event.width)
        canvas.bind("<Configure>", redimensionar) 

    def mostrar_tela_login(self):
        self.limpar_tela()
        card = tk.Frame(self.main_container, bg=CARD, padx=40, pady=40)
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.4, relheight=0.6)

        tk.Label(card, text="LIFE ALERT", fg=PRIMARY, bg=CARD, font=self.font_header).pack(pady=(0, 5))
        tk.Label(card, text="Acesse o sistema", fg=MUTED, bg=CARD, font=self.font_sub).pack(pady=(0, 25))

        tk.Label(card, text="Email", bg=CARD, fg=TEXT).pack(anchor="w")
        self.ent_login_email = ttk.Entry(card)
        self.ent_login_email.pack(fill=tk.X, pady=(5, 15))

        tk.Label(card, text="Senha", bg=CARD, fg=TEXT).pack(anchor="w")
        self.ent_login_senha = ttk.Entry(card, show="*")
        self.ent_login_senha.pack(fill=tk.X, pady=(5, 25))

        tk.Button(card, text="Entrar", bg=PRIMARY, fg="white", relief=tk.FLAT, 
                  command=self.executar_login, pady=10).pack(fill=tk.X, pady=5)
        
        tk.Button(card, text="Não tem conta? Cadastre-se", bg=CARD, fg=PRIMARY, 
                  relief=tk.FLAT, command=self.escolher_tipo_cadastro).pack()

    #ESCOLHER TIPO
    def escolher_tipo_cadastro(self):
        self.limpar_tela()
        card = tk.Frame(self.main_container, bg=CARD, padx=40, pady=40)
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.5)

        tk.Label(card, text="QUERO ME CADASTRAR COMO:", fg=PRIMARY, bg=CARD, font=self.font_header).pack(pady=20)

        opcoes = [("Civil", "1"), ("Atendente", "2"), ("Agente de Resgate", "3")]
        
        for texto, valor in opcoes:
            tk.Button(card, text=texto, font=self.font_sub, bg=BG, fg=TEXT, relief=tk.FLAT,
                      command=lambda v=valor: self.mostrar_form_cadastro(v), pady=8).pack(fill=tk.X, pady=5)
        
        tk.Button(card, text="Voltar", bg=CARD, fg=MUTED, command=self.mostrar_tela_login).pack(pady=10)

    #FORMULÁRIO DINÂMICO
    def mostrar_form_cadastro(self, tipo):
        self.limpar_tela()
        self.tipo_selecionado = tipo

        canvas = tk.Canvas(self.main_container, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg=BG)
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas_window = canvas.create_window((self.root.winfo_width() // 2, 20), 
                                           window=self.scroll_frame, 
                                           anchor="n")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        card = tk.Frame(self.scroll_frame, bg=CARD, padx=40, pady=30)
        card.pack(pady=20) 
        titulo_tipo = {"1": "Civil", "2": "Atendente", "3": "Agente"}[tipo]
        tk.Label(card, text=f"CADASTRO: {titulo_tipo.upper()}", fg=PRIMARY, bg=CARD, font=self.font_header).grid(row=0, columnspan=2, pady=(0, 20))
        labels = ["Nome", "CPF", "Telefone", "Rua", "Número", "Bairro", "Cidade", "Estado", "Email", "Senha"]
        self.cad_inputs = {}

        for i, label in enumerate(labels):
            tk.Label(card, text=label, bg=CARD, fg=TEXT, font=self.font_sub).grid(row=i+1, column=0, sticky="w", pady=5)
            ent = ttk.Entry(card, width=35)
            if label == "Senha": ent.config(show="*")
            ent.grid(row=i+1, column=1, pady=5, padx=(10, 0))
            self.cad_inputs[label] = ent

        row_idx = len(labels) + 1
        
        if tipo == "2":
            tk.Label(card, text="Turno", bg=CARD, fg=TEXT).grid(row=row_idx, column=0, sticky="w")
            self.ent_extra = ttk.Entry(card, width=35)
            self.ent_extra.grid(row=row_idx, column=1, pady=10)

        elif tipo == "3":
            tk.Label(card, text="Cargo", bg=CARD, fg=TEXT, font=self.font_sub).grid(row=row_idx, column=0, sticky="w", pady=5)
            self.ent_extra = ttk.Combobox(card, width=33, state="readonly") 
            self.ent_extra['values'] = ("Operacional", "Lider") 
            self.ent_extra.current(0)
            self.ent_extra.grid(row=row_idx, column=1, pady=5, padx=(10, 0))

        btn_finalizar = tk.Button(card, text="FINALIZAR CADASTRO", bg="#2b6cb0", fg="white", 
                                 font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
                                 command=self.executar_cadastro, pady=12, cursor="hand2")
        btn_finalizar.grid(row=row_idx+1, columnspan=2, sticky="ew", pady=(20, 5))
        
        btn_cancelar = tk.Button(card, text="Cancelar e Voltar", bg=CARD, fg=MUTED, 
                                relief=tk.FLAT, command=self.escolher_tipo_cadastro, cursor="hand2")
        btn_cancelar.grid(row=row_idx+2, columnspan=2, pady=5)

    def executar_login(self):
        user_email = self.ent_login_email.get()
        senha = self.ent_login_senha.get()

        usuario = Usuario.Login(self.db["usuarios"], user_email, senha)

        if usuario:
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

    def mostrar_dashboard(self):
        self.limpar_tela()
        
        # Sidebar (Esquerda)
        sidebar = tk.Frame(self.main_container, bg=CARD, width=250)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Conteúdo (Direita) 
        self.area_conteudo = tk.Frame(self.main_container, bg=BG)
        self.area_conteudo.pack(side="right", fill="both", expand=True)

        # Header da Sidebar
        tk.Label(sidebar, text="LIFE ALERT", fg=PRIMARY, bg=CARD, 
                 font=("Segoe UI", 14, "bold")).pack(pady=20)
        
        tk.Label(sidebar, text=f"Olá, {self.usuario_logado.nome}", fg=TEXT, bg=CARD,
                 font=("Segoe UI", 10)).pack(pady=(0, 20))
        self.usuario_logado.gui_ref = self 
        acoes = self.usuario_logado.obter_funcionalidades()

        for nome_acao, comando in acoes:
            btn = tk.Button(sidebar, text=nome_acao, bg=CARD, fg=TEXT, relief=tk.FLAT,
                            anchor="w", padx=20, pady=12, font=("Segoe UI", 10),
                            cursor="hand2")
            btn.configure(command=lambda c=comando: self.preparar_e_executar(c))
            btn.pack(fill=tk.X)

        tk.Frame(sidebar, height=1, bg=BG).pack(fill=tk.X, pady=10)

        tk.Button(sidebar, text="🚪 Sair", bg=CARD, fg=PRIMARY, relief=tk.FLAT, 
                  anchor="w", padx=20, command=self.mostrar_tela_login).pack(fill=tk.X, side="bottom", pady=20)

        # Mensagem Inicial
        self.label_boas_vindas = tk.Label(self.area_conteudo, text=f"Bem-vindo, {self.usuario_logado.nome}\nSelecione uma opção no menu ao lado.", 
                                         font=self.font_header, bg=BG, fg=MUTED)
        self.label_boas_vindas.pack(pady=100)

    def preparar_e_executar(self, comando):
        """Limpa apenas a área de conteúdo antes de carregar uma nova função"""
        for widget in self.area_conteudo.winfo_children():
            widget.destroy()
        comando(self.area_conteudo)
    
    def tela_criar_ocorrencia(self, container):
        tk.Label(container, text="ABERTURA DE OCORRÊNCIA", font=self.font_header, bg=BG, fg=PRIMARY).pack(pady=20)
        
        card = tk.Frame(container, bg=CARD, padx=30, pady=20)
        card.pack(pady=10, padx=50, fill=tk.BOTH, expand=True)

        # 1. Múltipla Seleção de Tipos (Checkbuttons)
        tk.Label(card, text="Tipos de Ocorrência (selecione todos que se aplicam):", 
                 bg=CARD, font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        self.tipos_selecionados = {}
        tipos_disponiveis = ["Policial", "Médica", "Incêndio", "Enchente", "Outros"]
        
        frame_checks = tk.Frame(card, bg=CARD)
        frame_checks.grid(row=1, column=0, columnspan=2, sticky="w", pady=5)

        for i, tipo in enumerate(tipos_disponiveis):
            var = tk.BooleanVar()
            chk = tk.Checkbutton(frame_checks, text=tipo, variable=var, bg=CARD, 
                                 activebackground=CARD, command=self.atualizar_campos_extras_oc)
            chk.pack(side=tk.LEFT, padx=5)
            self.tipos_selecionados[tipo] = var

        # 2. Campos Fixos (Rua, Bairro, etc)
        # Começamos na linha 2 agora
        campos_fixos = [
            ("Descrição", "descricao"), ("Rua", "rua"), ("Bairro", "bairro"),
            ("Cidade", "cidade"), ("Estado", "estado"), ("Gravidade", "gravidade"),
            ("Pessoas Afetadas", "qtdAfetados")
        ]
        
        self.inputs_oc = {}
        for i, (label, chave) in enumerate(campos_fixos):
            tk.Label(card, text=f"{label}:", bg=CARD).grid(row=i+2, column=0, sticky="w", pady=2)
            ent = ttk.Entry(card, width=33)
            ent.grid(row=i+2, column=1, pady=2, padx=10)
            self.inputs_oc[chave] = ent

        # 3. Frame para Campos Dinâmicos (Crime e Médico podem aparecer juntos!)
        self.frame_extra_oc = tk.Frame(card, bg=CARD)
        self.frame_extra_oc.grid(row=10, columnspan=2, sticky="ew", pady=10)
        self.inputs_extras_oc = {}

        # 4. Botão Finalizar
        tk.Button(card, text="Enviar Ocorrência", bg=PRIMARY, fg="white", relief=tk.FLAT,
                  command=self.confirmar_ocorrencia, pady=10, cursor="hand2"
                  ).grid(row=11, columnspan=2, sticky="ew", pady=20)

    def atualizar_campos_extras_oc(self):
        # Limpa campos extras anteriores
        for widget in self.frame_extra_oc.winfo_children():
            widget.destroy()
        self.inputs_extras_oc = {}

        linha = 0
        # Se Policial estiver marcado...
        if self.tipos_selecionados["Policial"].get():
            tk.Label(self.frame_extra_oc, text="--- DETALHES POLICIAIS ---", fg=PRIMARY, bg=CARD, font=("Segoe UI", 8, "bold")).grid(row=linha, columnspan=2, pady=5)
            linha += 1
            self.criar_campo_extra("Tipo de Crime", "tipoCrime", linha); linha += 1
            self.criar_campo_extra("Qtd Criminosos", "qtdCriminosos", linha); linha += 1
            self.criar_campo_extra("Descrição Suspeito", "descricaoSuspeito", linha); linha += 1

        # Se Médica estiver marcado...
        if self.tipos_selecionados["Médica"].get():
            tk.Label(self.frame_extra_oc, text="--- DETALHES MÉDICOS ---", fg=PRIMARY, bg=CARD, font=("Segoe UI", 8, "bold")).grid(row=linha, columnspan=2, pady=5)
            linha += 1
            # Note: NÃO criamos campo para Perfil Médico aqui, pois ele já existe no usuário
            self.criar_campo_extra("Sintomas Atuais", "sintomas", linha); linha += 1
            
            # Apenas um aviso visual opcional
            tk.Label(self.frame_extra_oc, text="ℹ️ Seu perfil médico será enviado automaticamente.", 
                     fg=MUTED, bg=CARD, font=("Segoe UI", 8, "italic")).grid(row=linha, columnspan=2)

    def criar_campo_extra(self, label, chave, row):
        tk.Label(self.frame_extra_oc, text=f"{label}:", bg=CARD).grid(row=row, column=0, sticky="w", pady=2)
        ent = ttk.Entry(self.frame_extra_oc, width=33)
        ent.grid(row=row, column=1, pady=2, padx=10)
        self.inputs_extras_oc[chave] = ent
    
    def confirmar_ocorrencia(self):
        selecionados = [tipo for tipo, var in self.tipos_selecionados.items() if var.get()]
        
        if not selecionados:
            messagebox.showwarning("Aviso", "Selecione pelo menos um tipo de ocorrência!")
            return

        # --- LÓGICA DE PERGUNTA SOBRE PERFIL MÉDICO ---
        if "Médica" in selecionados:
            perfil = getattr(self.usuario_logado, 'perfil_medico', None)
            
            if perfil is None:
                pergunta = messagebox.askyesno(
                    "Perfil Médico Ausente", 
                    "Você não tem um perfil médico cadastrado. Enviar o perfil ajuda no atendimento especializado.\n\n"
                    "Deseja enviar a ocorrência MESMO SEM o perfil?"
                )
                
                if not pergunta: # Se o usuário clicar em "Não"
                    # Opcional: Redirecionar para a tela de perfil
                    messagebox.showinfo("Cadastro", "Redirecionando para o cadastro de Perfil Médico...")
                    self.preparar_e_executar(lambda container: self.tela_perfil_medico(container))
                    return 
                
                # Se clicar em "Sim", define como string vazia ou aviso para o atendente
                dados_perfil = "Não cadastrado pelo usuário."
            else:
                dados_perfil = str(perfil)
        else:
            dados_perfil = None

        # ... segue a lógica de criação do objeto ...
        try:
            dados = {k: v.get() for k, v in self.inputs_oc.items()}
            dados.update({k: v.get() for k, v in self.inputs_extras_oc.items()})
            
            # Priorização Médica que definimos antes
            if "Médica" in selecionados:
                id_tipo_principal = "2"
                dados["perfilMedico"] = dados_perfil
                aviso_extra = "\n\nO atendente enviará as equipes necessárias."
            else:
                mapa_map = {"Policial": "1", "Médica": "2", "Incêndio": "3", "Enchente": "4", "Outros": "5"}
                id_tipo_principal = mapa_map[selecionados[0]]
                aviso_extra = ""

            # Dados automáticos e Factory
            dados.update({
                "civil": self.usuario_logado,
                "dataHora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "Aberta",
                "tipo": ", ".join(selecionados),
                "atendente": None, "agente": None, "equipe": None, "complemento": ""
            })
            nova_oc = OcorrenciaFactory.criar(id_tipo_principal, **dados)
            self.db["ocorrencias"].append(nova_oc)

            messagebox.showinfo("Sucesso", f"Ocorrência registrada!{aviso_extra}")
            self.mostrar_dashboard()

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao registrar: {e}")
    
    def tela_perfil_medico(self, container):
        tk.Label(container, text="MEU PERFIL MÉDICO", font=self.font_header, bg=BG, fg=PRIMARY).pack(pady=20)
        
        card = tk.Frame(container, bg=CARD, padx=30, pady=20)
        card.pack(pady=10, padx=50, fill=tk.BOTH)
        p_atual = getattr(self.usuario_logado, 'perfil_medico', None)
        
        campos = [
            ("Alergias", "alergias"),
            ("Doenças Crônicas", "doencas"),
            ("Deficiências", "deficiencia"),
            ("Tipo Sanguíneo", "tipo_sanguineo"),
            ("Contatos de Emergência", "contatoEmerg")
        ]

        self.inputs_perfil = {}
        for i, (label, chave) in enumerate(campos):
            tk.Label(card, text=f"{label}:", bg=CARD, fg=TEXT).grid(row=i, column=0, sticky="w", pady=5)
            ent = ttk.Entry(card, width=40)
            ent.grid(row=i, column=1, pady=5, padx=10)

            if p_atual:
                attr_map = {"tipo_sanguineo": "tipoSanguineo", "contatoEmerg": "contatoEmerg", 
                            "alergias": "alergias", "doencas": "doencas", "deficiencia": "deficiencia"}
                valor = getattr(p_atual, attr_map[chave], "")
                if valor != "Não cadastrado":
                    ent.insert(0, valor)
            
            self.inputs_perfil[chave] = ent

        tk.Button(card, text="Confirmar e Salvar", bg="#2f855a", fg="white", 
                  relief=tk.FLAT, command=self.salvar_perfil_medico, pady=10, cursor="hand2"
                  ).grid(row=len(campos), columnspan=2, sticky="ew", pady=20)

    def salvar_perfil_medico(self):
        # Coleta os dados dos inputs da tela
        # Os nomes das chaves aqui devem bater com os argumentos da sua Factory
        try:
            dados = {
                "alergias": self.inputs_perfil["alergias"].get(),
                "doencas": self.inputs_perfil["doencas"].get(),
                "deficiencia": self.inputs_perfil["deficiencia"].get(),
                "tipo_sanguineo": self.inputs_perfil["tipo_sanguineo"].get(),
                "contatoEmerg": self.inputs_perfil["contatoEmerg"].get()
            }
            novo_perfil = PerfilMedicoFactory.criar(**dados)
            
            # Salva o objeto no usuário logado
            self.usuario_logado.perfil_medico = novo_perfil
            
            messagebox.showinfo("Sucesso", "Perfil médico atualizado com sucesso!")
            self.mostrar_dashboard()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar o perfil: {e}")

    def tela_listar_ocorrencias(self, container):
            tk.Label(container, text="MINHAS OCORRÊNCIAS", font=self.font_header, bg=BG, fg=PRIMARY).pack(pady=20)
            
            # Filtramos as ocorrências que pertencem ao usuário logado
            minhas_ocs = [oc for oc in self.db["ocorrencias"] if oc.civil == self.usuario_logado]

            if not minhas_ocs:
                tk.Label(container, text="Você ainda não registrou nenhuma ocorrência.", 
                        font=("Segoe UI", 10), bg=BG, fg=TEXT).pack(pady=50)
                return

            # Frame para a Tabela
            frame_tabela = tk.Frame(container, bg=BG)
            frame_tabela.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

            # Configuração da Treeview (Tabela)
            colunas = ("id", "data", "tipo", "status", "gravidade")
            tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=15)
            
            # Cabeçalhos
            tabela.heading("id", text="ID")
            tabela.heading("data", text="Data/Hora")
            tabela.heading("tipo", text="Tipo")
            tabela.heading("status", text="Status")
            tabela.heading("gravidade", text="Gravidade")

            # Largura das colunas
            tabela.column("id", width=50, anchor="center")
            tabela.column("data", width=150, anchor="center")
            tabela.column("tipo", width=180, anchor="w")
            tabela.column("status", width=120, anchor="center")
            tabela.column("gravidade", width=100, anchor="center")

            # Inserindo os dados
            for oc in minhas_ocs:
                tabela.insert("", tk.END, values=(
                    oc.id, 
                    oc.dataHora, 
                    oc.tipo, 
                    oc.status.upper(), 
                    oc.gravidade
                ))

            # Scrollbar para a tabela
            scrollbar = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=tabela.yview)
            tabela.configure(yscroll=scrollbar.set)
            
            tabela.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Botão para ver detalhes (Opcional)
            tk.Button(container, text="Ver Detalhes da Ocorrência Selecionada", 
                    bg=PRIMARY, fg="white", relief=tk.FLAT, pady=10,
                    command=lambda: self.exibir_detalhes_oc_selecionada(tabela, minhas_ocs)
                    ).pack(pady=20)

    def exibir_detalhes_oc_selecionada(self, tabela, lista_ocs):
        item_selecionado = tabela.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione uma ocorrência na lista primeiro!")
            return

        # Pega o ID da linha selecionada
        valores = tabela.item(item_selecionado)['values']
        id_oc = valores[0]
        
        # Busca o objeto original na lista
        oc = next((o for o in lista_ocs if o.id == id_oc), None)
        
        if oc:
            # Aqui usamos o polimorfismo! 
            # Se for Médica, mostrará sintomas; se for Policial, mostrará crimes.
            detalhes = f"ID: {oc.id}\nStatus: {oc.status}\nLocal: {oc.rua}, {oc.bairro}\n"
            detalhes += f"Descrição: {oc.descricao}\n"
            
            # Adiciona informações extras se existirem (kwargs/atributos específicos)
            if hasattr(oc, 'sintomas') and oc.sintomas:
                detalhes += f"\nSINTOMAS: {oc.sintomas}"
            if hasattr(oc, 'tipoCrime') and oc.tipoCrime:
                detalhes += f"\nCRIME: {oc.tipoCrime}"
            if hasattr(oc, 'perfilMedico') and oc.perfilMedico:
                detalhes += f"\n\n{oc.perfilMedico}" # Aqui chama o __str__ que você criou!

            messagebox.showinfo(f"Detalhes da Ocorrência #{oc.id}", detalhes)

    def tela_atualizar_dados(self, container):
        tk.Label(container, text="ATUALIZAR MEUS DADOS", font=self.font_header, bg=BG, fg=PRIMARY).pack(pady=20)
        
        # Usaremos um Canvas com Scroll se a tela ficar muito cheia, 
        # mas aqui vamos apenas listar os campos no frame.
        card = tk.Frame(container, bg=CARD, padx=30, pady=20)
        card.pack(pady=10, padx=50, fill=tk.BOTH)

        campos = [
            ("Nome", "nome", self.usuario_logado.nome),
            ("Telefone", "telefone", self.usuario_logado.telefone),
            ("Email", "email", self.usuario_logado.email),
            ("Senha", "senha", self.usuario_logado.senha),
            ("Rua", "rua", self.usuario_logado.rua),
            ("Número", "num", self.usuario_logado.num),
            ("Bairro", "bairro", self.usuario_logado.bairro),
            ("Cidade", "cidade", self.usuario_logado.cidade),
            ("Estado", "estado", self.usuario_logado.estado)
        ]

        self.inputs_atualizar = {}
        for i, (label, chave, valor_atual) in enumerate(campos):
            tk.Label(card, text=f"{label}:", bg=CARD).grid(row=i, column=0, sticky="w", pady=2)
            ent = ttk.Entry(card, width=40)
            ent.insert(0, valor_atual)
            ent.grid(row=i, column=1, pady=2, padx=10)
            self.inputs_atualizar[chave] = ent

        tk.Button(card, text="Salvar Todas as Alterações", bg="#2b6cb0", fg="white", 
                  relief=tk.FLAT, command=self.confirmar_atualizacao, pady=10
                  ).grid(row=len(campos), columnspan=2, sticky="ew", pady=20)

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
            messagebox.showinfo("Sucesso", "Seus dados e endereço foram atualizados!")
            self.mostrar_dashboard()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar dados: {e}")
    
    def tela_excluir_conta(self, container):
        tk.Label(container, text="EXCLUIR CONTA", font=self.font_header, bg=BG, fg=PRIMARY).pack(pady=20)
        
        card = tk.Frame(container, bg=CARD, padx=40, pady=40)
        card.pack(pady=20)

        tk.Label(card, text="Tem certeza que deseja excluir sua conta?\nEsta ação não pode ser desfeita.", 
                 bg=CARD, fg=TEXT, justify="center").pack(pady=20)

        tk.Button(card, text="Sim, Excluir minha conta", bg=PRIMARY, fg="white", relief=tk.FLAT,
                  command=self.confirmar_exclusao, pady=10).pack(fill=tk.X)
        
        tk.Button(card, text="Cancelar", bg=CARD, fg=MUTED, relief=tk.FLAT,
                  command=self.mostrar_dashboard).pack(pady=10)

    def confirmar_exclusao(self):
        # Chama o método excluirUsuario da sua classe Usuario
        sucesso = self.usuario_logado.excluirUsuario(self.db["usuarios"])
        
        if sucesso:
            messagebox.showinfo("Conta Excluída", "Sua conta foi removida do sistema.")
            self.usuario_logado = None
            self.mostrar_tela_login()
        else:
            messagebox.showerror("Erro", "Não foi possível excluir a conta.")