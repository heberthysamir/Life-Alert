import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
from datetime import datetime
from domain.usuarios.Usuario import Usuario
from application.usuariosFactory import UsuarioFactory
from application.ocorrenciaFactory import OcorrenciaFactory
from application.perfilMedicoFactory import PerfilMedicoFactory
from infrastructure.api.screens.authScreen import AuthScreen
from infrastructure.api.screens.civilSreen import CivilScreen

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
        
        # Chama o método Login da classe Usuario (atualizado conforme sua solicitação anterior)
        usuario = Usuario.Login(self.db["usuarios"], email, senha)

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

    # --- DELEGAÇÃO PARA TELAS EXTERNAS (CIVIL) ---
    def tela_central_alertas(self, container):
        tk.Label(container, text="CENTRAL DE ALERTAS COMPLETA", font=self.font_header, bg=BG, fg=PRIMARY).pack(pady=20)
        CivilScreen.render_lista_alertas(self, container)
        
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

    def atualizar_campos_extras_oc(self):
        for widget in self.frame_extra_oc.winfo_children():
            widget.destroy()
        self.inputs_extras_oc = {}
        linha = 0

        if self.tipos_selecionados["Policial"].get():
            tk.Label(self.frame_extra_oc, text="Detalhes Policiais", fg=PRIMARY, bg=CARD).grid(row=linha, columnspan=2)
            linha += 1
            self.criar_campo_extra("Tipo de Crime", "tipoCrime", linha); linha += 1
            
        if self.tipos_selecionados["Médica"].get():
            tk.Label(self.frame_extra_oc, text="Detalhes Médicos", fg=PRIMARY, bg=CARD).grid(row=linha, columnspan=2)
            linha += 1
            self.criar_campo_extra("Sintomas Atuais", "sintomas", linha); linha += 1

    def criar_campo_extra(self, label, chave, row):
        tk.Label(self.frame_extra_oc, text=f"{label}:", bg=CARD).grid(row=row, column=0, sticky="w")
        ent = ttk.Entry(self.frame_extra_oc, width=33)
        ent.grid(row=row, column=1, pady=2, padx=10)
        self.inputs_extras_oc[chave] = ent

    def confirmar_ocorrencia(self):
        try:
            selecionados = [tipo for tipo, var in self.tipos_selecionados.items() if var.get()]
            if not selecionados:
                messagebox.showwarning("Aviso", "Selecione um tipo!")
                return

            dados = {k: v.get() for k, v in self.inputs_oc.items()}
            dados.update({k: v.get() for k, v in self.inputs_extras_oc.items()})
            
            # Perfil médico automático
            if "Médica" in selecionados:
                perfil = getattr(self.usuario_logado, 'perfil_medico', None)
                dados["perfilMedico"] = str(perfil) if perfil else "Não informado"
                id_principal = "2"
            else:
                id_principal = "1" # Simplificado para exemplo

            dados.update({
                "civil": self.usuario_logado,
                "dataHora": datetime.now().strftime("%d/%m %H:%M"),
                "status": "Aberta",
                "tipo": ", ".join(selecionados)
            })

            nova_oc = OcorrenciaFactory.criar(id_principal, **dados)
            self.db["ocorrencias"].append(nova_oc)
            messagebox.showinfo("Sucesso", "Ocorrência Enviada!")
            self.mostrar_dashboard()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    def confirmar_atualizacao(self):
        try:
            # Esta lógica funciona para todos, pois todos têm esses campos base
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

    def preparar_e_executar(self, comando):
        """Limpa apenas a área de conteúdo antes de carregar uma nova função"""
        for widget in self.area_conteudo.winfo_children():
            widget.destroy()
        comando(self.area_conteudo)
    
