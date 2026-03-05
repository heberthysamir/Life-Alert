import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
from application.usuariosFactory import UsuarioFactory

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

    # --- PASSO 1: ESCOLHER TIPO ---
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

    # --- PASSO 2: FORMULÁRIO DINÂMICO ---

    def mostrar_form_cadastro(self, tipo):
        self.limpar_tela()
        self.tipo_selecionado = tipo

        # 1. Criar Canvas e Scrollbar
        canvas = tk.Canvas(self.main_container, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=canvas.yview)
        
        # 2. Criar o Frame que vai conter o formulário
        # Importante: Não damos tamanho fixo aqui
        self.scroll_frame = tk.Frame(canvas, bg=BG)

        # 3. Configurar o Scroll dinâmico
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # 4. Inserir o Frame no Canvas
        # Usamos uma largura calculada para manter o card centralizado
        canvas_window = canvas.create_window((self.root.winfo_width() // 2, 20), 
                                           window=self.scroll_frame, 
                                           anchor="n")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 5. Card Branco (Onde ficam os inputs)
        card = tk.Frame(self.scroll_frame, bg=CARD, padx=40, pady=30)
        card.pack(pady=20) # Margem superior e inferior

        titulo_tipo = {"1": "Civil", "2": "Atendente", "3": "Agente"}[tipo]
        tk.Label(card, text=f"CADASTRO: {titulo_tipo.upper()}", fg=PRIMARY, bg=CARD, font=self.font_header).grid(row=0, columnspan=2, pady=(0, 20))

        # 6. Gerar os Campos (Mesma lógica anterior)
        labels = ["Nome", "CPF", "Telefone", "Rua", "Número", "Bairro", "Cidade", "Estado", "Email", "Senha"]
        self.cad_inputs = {}

        for i, label in enumerate(labels):
            tk.Label(card, text=label, bg=CARD, fg=TEXT, font=self.font_sub).grid(row=i+1, column=0, sticky="w", pady=5)
            ent = ttk.Entry(card, width=35)
            if label == "Senha": ent.config(show="*")
            ent.grid(row=i+1, column=1, pady=5, padx=(10, 0))
            self.cad_inputs[label] = ent

        row_idx = len(labels) + 1
        
        # Campo Extra
        if tipo == "2":
            tk.Label(card, text="Turno", bg=CARD, fg=TEXT).grid(row=row_idx, column=0, sticky="w")
            self.ent_extra = ttk.Entry(card, width=35)
            self.ent_extra.grid(row=row_idx, column=1, pady=10)

        elif tipo == "3":
            tk.Label(card, text="Cargo", bg=CARD, fg=TEXT, font=self.font_sub).grid(row=row_idx, column=0, sticky="w", pady=5)
            
            # Criamos o Combobox em vez de um Entry comum
            self.ent_extra = ttk.Combobox(card, width=33, state="readonly") 
            self.ent_extra['values'] = ("Operacional", "Lider") # Opções do Select
            self.ent_extra.current(0) # Define "Operacional" como padrão
            self.ent_extra.grid(row=row_idx, column=1, pady=5, padx=(10, 0))

        # 7. BOTÕES (Substituindo fill por sticky)
        btn_finalizar = tk.Button(card, text="FINALIZAR CADASTRO", bg="#2b6cb0", fg="white", 
                                 font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
                                 command=self.executar_cadastro, pady=12, cursor="hand2")
        # Mudança aqui: fill=tk.X vira sticky="ew"
        btn_finalizar.grid(row=row_idx+1, columnspan=2, sticky="ew", pady=(20, 5))
        
        btn_cancelar = tk.Button(card, text="Cancelar e Voltar", bg=CARD, fg=MUTED, 
                                relief=tk.FLAT, command=self.escolher_tipo_cadastro, cursor="hand2")
        btn_cancelar.grid(row=row_idx+2, columnspan=2, pady=5)

    def executar_login(self):
        user_email = self.ent_login_email.get()
        senha = self.ent_login_senha.get()
        usuario = next((u for u in self.db["usuarios"] if u.email == user_email and u.senha == senha), None)

        if usuario:
            self.usuario_logado = usuario
            messagebox.showinfo("Sucesso", f"Bem-vindo, {usuario.nome}!")
            self.mostrar_dashboard()
        else:
            messagebox.showerror("Erro", "Email ou Senha incorretos.")

    def executar_cadastro(self):
        try:
            dados = {k.lower(): v.get() for k, v in self.cad_inputs.items()}
            dados["num"] = dados.pop("número")
            
            if self.tipo_selecionado == "2":
                dados["turno"] = self.ent_extra.get()
            elif self.tipo_selecionado == "3":
                # O valor virá do Combobox ("Operacional" ou "Lider")
                dados["cargo"] = self.ent_extra.get()
                dados["status"] = True

            # A Factory criará o objeto Agente com o cargo correto
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

        # Conteúdo (Direita) - Onde as telas de formulários vão aparecer
        self.area_conteudo = tk.Frame(self.main_container, bg=BG)
        self.area_conteudo.pack(side="right", fill="both", expand=True)

        # Header da Sidebar
        tk.Label(sidebar, text="LIFE ALERT", fg=PRIMARY, bg=CARD, 
                 font=("Segoe UI", 14, "bold")).pack(pady=20)
        
        tk.Label(sidebar, text=f"Olá, {self.usuario_logado.nome}", fg=TEXT, bg=CARD,
                 font=("Segoe UI", 10)).pack(pady=(0, 20))

        # --- POLIMORFISMO ---
        # Injetamos a referência da GUI no usuário para ele saber quais métodos chamar
        self.usuario_logado.gui_ref = self 
        acoes = self.usuario_logado.obter_funcionalidades()

        for nome_acao, comando in acoes:
            # O comando(self.area_conteudo) limpa a tela da direita e desenha a nova
            btn = tk.Button(sidebar, text=nome_acao, bg=CARD, fg=TEXT, relief=tk.FLAT,
                            anchor="w", padx=20, pady=12, font=("Segoe UI", 10),
                            cursor="hand2")
            btn.configure(command=lambda c=comando: self.preparar_e_executar(c))
            btn.pack(fill=tk.X)

        # Rodapé da Sidebar
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