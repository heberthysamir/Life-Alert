import tkinter as tk
from tkinter import ttk, messagebox

# Constantes de Estilo para consistência visual
PRIMARY = "#c53030"  
SECONDARY = "#2b6cb0" 
BG = "#f4f7fb"       
CARD = "#ffffff"     
TEXT = "#243444"     
MUTED = "#6b7280"    

class AuthScreen:
    @staticmethod
    def render_login(gui):
        """
        Renderiza a interface de acesso inicial.
        
        Configura um card centralizado com campos de e-mail e senha, 
        além de botões para autenticação e redirecionamento para o fluxo de cadastro.
        """
        gui.limpar_tela()
        
        card = tk.Frame(gui.main_container, bg=CARD, padx=40, pady=40)
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.4, relheight=0.6)

        tk.Label(card, text="LIFE ALERT", fg=PRIMARY, bg=CARD, font=gui.font_header).pack(pady=(0, 5))
        tk.Label(card, text="Acesse o sistema", fg=MUTED, bg=CARD, font=gui.font_sub).pack(pady=(0, 25))

        tk.Label(card, text="Email", bg=CARD, fg=TEXT).pack(anchor="w")
        gui.ent_login_email = ttk.Entry(card)
        gui.ent_login_email.pack(fill=tk.X, pady=(5, 15))

        tk.Label(card, text="Senha", bg=CARD, fg=TEXT).pack(anchor="w")
        gui.ent_login_senha = ttk.Entry(card, show="*")
        gui.ent_login_senha.pack(fill=tk.X, pady=(5, 25))

        tk.Button(card, text="Entrar", bg=PRIMARY, fg="white", relief=tk.FLAT, 
                  command=gui.executar_login, pady=10, cursor="hand2").pack(fill=tk.X, pady=5)
        
        tk.Button(card, text="Não tem conta? Cadastre-se", bg=CARD, fg=PRIMARY, 
                  relief=tk.FLAT, command=lambda: AuthScreen.render_escolha_tipo(gui), cursor="hand2").pack()

    @staticmethod
    def render_escolha_tipo(gui):
        """
        Interface intermediária para seleção do tipo de usuário (Civil, Atendente ou Agente).
        
        Esta escolha define quais campos extras serão exibidos e como o objeto 
        de usuário será instanciado na fábrica (Factory) durante o cadastro.
        """
        gui.limpar_tela()
        card = tk.Frame(gui.main_container, bg=CARD, padx=40, pady=40)
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.5)

        tk.Label(card, text="QUERO ME CADASTRAR COMO:", fg=PRIMARY, bg=CARD, font=gui.font_header).pack(pady=1)

        opcoes = [("Civil", "1"), ("Atendente", "2"), ("Agente de Resgate", "3")]
        
        for texto, valor in opcoes:
            tk.Button(card, text=texto, font=gui.font_sub, bg=BG, fg=TEXT, relief=tk.FLAT,
                      command=lambda v=valor: AuthScreen.render_formulario_cadastro(gui, v), 
                      pady=8, cursor="hand2").pack(fill=tk.X, pady=5)
        
        tk.Button(card, text="Voltar", bg=CARD, fg=MUTED, 
                  command=lambda: AuthScreen.render_login(gui), cursor="hand2").pack(pady=8)

    @staticmethod
    def render_formulario_cadastro(gui, tipo):
        """
        Gera um formulário de cadastro dinâmico com suporte a rolagem (Canvas).
        
        Cria campos comuns a todos os perfis e injeta componentes específicos 
        (Entry para Turno ou Combobox para Cargo) dependendo do parâmetro 'tipo'.
        """
        gui.limpar_tela()
        gui.tipo_selecionado = tipo

        canvas = tk.Canvas(gui.main_container, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(gui.main_container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG)
        
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((gui.root.winfo_width() // 2, 20), window=scroll_frame, anchor="n")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        card = tk.Frame(scroll_frame, bg=CARD, padx=40, pady=30)
        card.pack(pady=20) 

        titulo = {"1": "Civil", "2": "Atendente", "3": "Agente"}[tipo]
        tk.Label(card, text=f"CADASTRO: {titulo.upper()}", fg=PRIMARY, bg=CARD, font=gui.font_header).grid(row=0, columnspan=2, pady=(0, 20))
        
        labels = ["Nome", "CPF", "Telefone", "Rua", "Número", "Bairro", "Cidade", "Estado", "Email", "Senha"]
        gui.cad_inputs = {}

        for i, label in enumerate(labels):
            tk.Label(card, text=label, bg=CARD, fg=TEXT).grid(row=i+1, column=0, sticky="w", pady=5)
            ent = ttk.Entry(card, width=35)
            if label == "Senha": ent.config(show="*")
            ent.grid(row=i+1, column=1, pady=5, padx=(10, 0))
            gui.cad_inputs[label] = ent

        row_idx = len(labels) + 1
        
        if tipo == "2": # Perfil Atendente
            tk.Label(card, text="Turno", bg=CARD, fg=TEXT).grid(row=row_idx, column=0, sticky="w")
            gui.ent_extra = ttk.Entry(card, width=35)
            gui.ent_extra.grid(row=row_idx, column=1, pady=10, padx=(10, 0))
        elif tipo == "3": # Perfil Agente
            tk.Label(card, text="Cargo", bg=CARD, fg=TEXT).grid(row=row_idx, column=0, sticky="w")
            gui.ent_extra = ttk.Combobox(card, width=33, state="readonly", values=("Operacional", "Lider"))
            gui.ent_extra.current(0)
            gui.ent_extra.grid(row=row_idx, column=1, pady=10, padx=(10, 0))

        tk.Button(card, text="FINALIZAR CADASTRO", bg=SECONDARY, fg="white", font=("Segoe UI", 10, "bold"), 
                  relief=tk.FLAT, command=gui.executar_cadastro, pady=12, cursor="hand2").grid(row=row_idx+1, columnspan=2, sticky="ew", pady=(20, 5))
        
        tk.Button(card, text="Cancelar", bg=CARD, fg=MUTED, relief=tk.FLAT,
                  command=lambda: AuthScreen.render_escolha_tipo(gui), cursor="hand2").grid(row=row_idx+2, columnspan=2, pady=5)