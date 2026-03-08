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
from application.vitimaFactory import VitimaFactory
from infrastructure.api.screens.authScreen import AuthScreen
from infrastructure.api.screens.civilSreen import CivilScreen
from infrastructure.api.screens.atendenteScreen import AtendenteScreen
from infrastructure.api.screens.agenteScreen import AgenteScreen
from infrastructure.repositories.repositoryContainer import get_repositories

PRIMARY = "#c53030"  
BG = "#f4f7fb"
CARD = "#ffffff"
TEXT = "#243444"
MUTED = "#6b7280"

class LifeAlertGUI:
    def __init__(self, root):
        self.root = root
        # Injetar repositórios centralizados
        repos = get_repositories()
        self.usuario_repo = repos.usuario
        self.ocorrencia_repo = repos.ocorrencia
        self.alerta_repo = repos.alerta
        self.atendimento_repo = repos.atendimento
        self.equipe_repo = repos.equipe
        self.vitima_repo = repos.vitima
        self.resgate_repo = repos.resgate
        # Manter compatibilidade com dicionário em memória para dados locais
        self.db = {
            "usuarios": [],
            "ocorrencias": [],
            "alertas": [],
            "equipes": [],
            "atendimentos": [],
            "vitimas": []
        }
        self.usuario_logado = None

        self.root.title("Life Alert")
        self.root.geometry("1000x700")
        self.root.configure(bg=BG)

        self.font_header = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.font_sub = tkfont.Font(family="Segoe UI", size=10)

        self.main_container = tk.Frame(self.root, bg=BG)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        AuthScreen.render_login(self)

    # Remove todos os widgets presentes no container principal
    def limpar_tela(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    # Reseta o estado do usuário e renderiza a tela de login
    def mostrar_tela_login(self):
        self.usuario_logado = None
        AuthScreen.render_login(self)

    # Limpa a área de conteúdo dinâmico e executa o comando da nova tela
    def preparar_e_executar(self, comando):
        for widget in self.area_conteudo.winfo_children():
            widget.destroy()
        comando(self.area_conteudo)

    # Valida as credenciais e redireciona o usuário para o dashboard
    def executar_login(self):
        email = self.ent_login_email.get().strip()
        senha = self.ent_login_senha.get().strip()
        
        # validação simples de campos
        if not email or not senha:
            messagebox.showwarning("Aviso", "Por favor, informe e-mail e senha.")
            return
        
        # Buscar usuário no banco de dados via repositório
        usuario = self.usuario_repo.buscarPorCredenciais(email, senha)

        if usuario:
            self.usuario_logado = usuario
            messagebox.showinfo("Sucesso", f"Bem-vindo, {usuario.nome}!")
            self.mostrar_dashboard()
        else:
            messagebox.showerror("Erro", "E-mail ou senha incorretos.")

    # Processa os dados do formulário e cria um novo usuário via Factory
    def executar_cadastro(self):
        try:
            dados = {k.lower(): v.get().strip() for k, v in self.cad_inputs.items()}
            dados["num"] = dados.pop("número")
            
            # validação de campos obrigatórios
            obrigatorios = ["nome","cpf","email","senha","cidade","bairro","rua","num","estado"]
            for campo in obrigatorios:
                if not dados.get(campo):
                    raise ValueError(f"O campo '{campo}' é obrigatório.")

            if self.tipo_selecionado == "2":
                turno_val = self.ent_extra.get().strip()
                if not turno_val:
                    raise ValueError("Turno é obrigatório para atendentes.")
                dados["turno"] = turno_val
            elif self.tipo_selecionado == "3":
                cargo_val = self.ent_extra.get().strip()
                if not cargo_val:
                    raise ValueError("Cargo é obrigatório para agentes.")
                dados["cargo"] = cargo_val
                dados["status"] = True

            novo_usuario = UsuarioFactory.criar(self.tipo_selecionado, **dados)
            # Salvar no banco de dados via repositório
            self.usuario_repo.salvar(novo_usuario)
            
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.mostrar_tela_login()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cadastrar: {e}")

    # Renderiza a estrutura principal com sidebar e área de alertas do usuário
    def mostrar_dashboard(self):
        self.limpar_tela()
        
        sidebar = tk.Frame(self.main_container, bg=CARD, width=250)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        self.area_conteudo = tk.Frame(self.main_container, bg=BG)
        self.area_conteudo.pack(side="right", fill="both", expand=True)
        header_frame = tk.Frame(self.area_conteudo, bg=BG)
        header_frame.pack(fill=tk.X, pady=30, padx=40)

        tk.Label(header_frame, text=f"Bem-vindo, {self.usuario_logado.nome}", 
                 font=self.font_header, bg=BG, fg=TEXT, anchor="w").pack(fill=tk.X)
        tk.Label(header_frame, text=f"Resumo de alertas para {self.usuario_logado.bairro}, {self.usuario_logado.cidade}:", 
                 font=("Segoe UI", 10), bg=BG, fg=MUTED, anchor="w").pack(fill=tk.X)

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

    # Renderiza a lista de alertas ativos na tela do cidadão
    def tela_central_alertas(self, container):
        CivilScreen.render_lista_alertas(self,container)

    # Renderiza o formulário para abertura de novas ocorrências
    def tela_criar_ocorrencia(self, container):
        CivilScreen.render_criar_ocorrencia(self, container)

    # Renderiza o histórico de ocorrências registradas pelo usuário
    def tela_listar_ocorrencias(self, container):
        CivilScreen.render_listar_ocorrencias(self, container)

    # Renderiza o formulário de informações médicas do cidadão
    def tela_perfil_medico(self, container):
        CivilScreen.render_perfil_medico(self, container)

    # Renderiza a tela de edição de informações do perfil logado
    def tela_atualizar_dados(self, container):
        CivilScreen.render_atualizar_dados(self, container)

    # Renderiza a confirmação de encerramento definitivo da conta
    def tela_excluir_conta(self, container):
        CivilScreen.render_excluir_conta(self, container)

    # Renderiza a lista de ocorrências pendentes para o atendente
    def tela_gerenciar_atendimentos(self, container):
        AtendenteScreen.render_gerenciar_atendimentos(self, container)

    # Renderiza o painel de disparo de alertas de emergência
    def tela_painel_alertas(self, container):
        AtendenteScreen.render_painel_alertas(self, container)
    
    # Renderiza a gestão de vítimas para o agente de campo
    def tela_gerenciar_vitimas(self, container):
        AgenteScreen.render_gerenciar_vitimas(self, container)

    # Renderiza o formulário de cadastro de nova vítima em um resgate
    def tela_cadastrar_vitima(self, container):
        AgenteScreen.render_cadastrar_vitima(self, container)

    # Renderiza a criação de novas equipes de resposta
    def tela_criar_equipe(self, container):
        AgenteScreen.render_criar_equipe(self, container)

    # Renderiza o menu de gestão de equipes existentes
    def tela_menu_equipe(self, container):
        AgenteScreen.render_menu_equipes(self, container)

    # Renderiza a tela de visualização de relatórios e estatísticas
    def tela_relatorios(self, container):
        AgenteScreen.render_relatorios(self, container)
    
    # Renderiza o painel de controle de ocorrências em tempo real para o agente
    def tela_painel_operacional(self, container):
        AgenteScreen.render_painel_operacional(self, container)

    # Gera campos dinâmicos no formulário baseados no tipo de ocorrência selecionado
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

    # Cria um par de label e entrada para o formulário de ocorrências
    def criar_campo_extra(self, label, chave, row):
        tk.Label(self.frame_extra_oc, text=f"{label}:", bg="#ffffff").grid(row=row, column=0, sticky="w", pady=2)
        ent = ttk.Entry(self.frame_extra_oc, width=33)
        ent.grid(row=row, column=1, pady=2, padx=10)
        self.inputs_extras_oc[chave] = ent

    # Valida, cria a ocorrência e designa um atendente automaticamente
    def confirmar_ocorrencia(self):
        selecionados = [tipo for tipo, var in self.tipos_selecionados.items() if var.get()]
        
        if not selecionados:
            messagebox.showwarning("Aviso", "Selecione pelo menos um tipo de ocorrência!")
            return

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
            dados = {k: v.get() for k, v in self.inputs_oc.items()}
            dados.update({k: v.get() for k, v in self.inputs_extras_oc.items()})
            
            mapa_map = {"Policial": "1", "Médica": "2", "Incêndio": "3", "Enchente": "4", "Outros": "5"}
            id_tipo_principal = "2" if "Médica" in selecionados else mapa_map[selecionados[0]]

            # 4. Preparação dos dados para a Factory
            dados.update({
                "civil": self.usuario_logado,
                "dataHora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "Aberta",
                "tipo": ", ".join(selecionados),
                "perfilMedico": dados_perfil,
                "atendente": None, 
                "agente": None,
                "equipe": None,
            })

            nova_oc = OcorrenciaFactory.criar(id_tipo_principal, **dados)
            self.ocorrencia_repo.salvar(nova_oc)

            from application.atendimentoService import AtendimentoService
            atendentes = self.usuario_repo.listarTodos()
            atendente_escolhido = AtendimentoService.designarAtendente(
                nova_oc, 
                atendentes, 
                self.atendimento_repo.listarTodos()
            )

            if atendente_escolhido:
                novo_atendimento = Atendimento(
                    atendente=atendente_escolhido,
                    ocorrencia=nova_oc,
                    horaInicio=dados["dataHora"]
                )
                self.atendimento_repo.salvar(novo_atendimento)
                
                nova_oc.status = "Em Atendimento"
                nova_oc.atendente = atendente_escolhido
                self.ocorrencia_repo.salvar(nova_oc)
                
                msg_sucesso = f"Ocorrência registrada!\nAtendente {atendente_escolhido.nome} foi designado."
            else:
                msg_sucesso = "Ocorrência registrada! Aguardando atendente disponível."

            messagebox.showinfo("Sucesso", msg_sucesso)
            self.mostrar_dashboard()

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao registrar ocorrência: {e}")

    # Coleta os novos dados da interface e atualiza o objeto do usuário logado
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
            # Salvar alterações no banco de dados
            self.usuario_repo.salvar(self.usuario_logado)
            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
            self.mostrar_dashboard()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar: {e}")

    # Remove o usuário do banco de dados e retorna à tela de login
    def confirmar_exclusao(self):
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir sua conta permanentemente?"):
            sucesso = self.usuario_repo.excluir(self.usuario_logado.cpf)
            if sucesso:
                messagebox.showinfo("Encerrado", "Conta excluída com sucesso.")
                self.mostrar_tela_login()
            else:
                messagebox.showerror("Erro", "Não foi possível excluir a conta.")
                
    # Localiza uma ocorrência selecionada e exibe todos os seus atributos detalhados
    def exibir_detalhes_oc_selecionada(self, tabela, lista_ocs):
            item_selecionado = tabela.selection()
            if not item_selecionado:
                messagebox.showwarning("Aviso", "Selecione uma ocorrência na lista primeiro!")
                return

            valores = tabela.item(item_selecionado)['values']
            id_oc = valores[0]
            oc = next((o for o in lista_ocs if o.id == id_oc), None)
            
            if oc:
                for widget in self.area_conteudo.winfo_children():
                    widget.destroy()

                header_frame = tk.Frame(self.area_conteudo, bg=BG)
                header_frame.pack(fill=tk.X, padx=20, pady=10)
                
                tk.Button(header_frame, text="← Voltar para Lista", bg=CARD, fg=PRIMARY, 
                        command=lambda: self.preparar_e_executar(self.usuario_logado.obter_funcionalidades()[4][1])).pack(side=tk.LEFT)
                
                tk.Label(self.area_conteudo, text=f"DETALHES DA OCORRÊNCIA #{oc.id}", 
                        font=self.font_header, bg=BG, fg=PRIMARY).pack(pady=10)

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

                if hasattr(oc, 'tipoCrime') and oc.tipoCrime:
                    info.append(("Tipo de Crime", oc.tipoCrime))
                if hasattr(oc, 'sintomas') and oc.sintomas:
                    info.append(("Sintomas", oc.sintomas))
                if hasattr(oc, 'perfilMedico') and oc.perfilMedico:
                    info.append(("Perfil Médico", oc.perfilMedico))

                for i, (label, valor) in enumerate(info):
                    tk.Label(card, text=f"{label}:", bg=CARD, font=("Segoe UI", 10, "bold")).grid(row=i, column=0, sticky="w", pady=5)
                    tk.Label(card, text=valor, bg=CARD, font=("Segoe UI", 10), wraplength=400, justify="left").grid(row=i, column=1, sticky="w", padx=10, pady=5)

                atendimento = next((a for a in self.db.get("atendimentos", []) if a.ocorrencia == oc), None)
                if atendimento:
                    tk.Frame(card, height=1, bg=BG).grid(row=len(info), columnspan=2, sticky="ew", pady=10)
                    tk.Label(card, text="INFORMAÇÕES DE ATENDIMENTO", bg=CARD, fg=MUTED, font=("Segoe UI", 9, "bold")).grid(row=len(info)+1, columnspan=2, sticky="w")
                    
                    at_info = [
                        ("Atendente", atendimento.atendente.nome),
                        ("Início", atendimento.horaInicio), 
                        ("Urgência", atendimento.grauUrgencia)
                    ]
                    
                    for i, (label, valor) in enumerate(at_info):
                        row = len(info) + 2 + i
                        tk.Label(card, text=f"{label}:", bg=CARD, font=("Segoe UI", 10, "bold")).grid(row=row, column=0, sticky="w", pady=5)
                        tk.Label(card, text=valor, bg=CARD).grid(row=row, column=1, sticky="w", padx=10)
    
    # Cria ou atualiza as informações de saúde vinculadas ao usuário logado
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
            # Salvar usuário atualizado no banco de dados
            self.usuario_repo.salvar(self.usuario_logado)
            
            messagebox.showinfo("Sucesso", "Perfil médico atualizado com sucesso!")
            self.mostrar_dashboard()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar o perfil: {e}")
    
    # Processa os dados da interface e gera um novo alerta público no banco
    def logica_emitir_alerta(self):
        try:
            idx_combo = self.combo_oc_alerta.current()
            if idx_combo == -1: raise Exception("Selecione uma ocorrência.")

            # Buscar ocorrência do banco de dados
            ocorrencias = self.ocorrencia_repo.listarTodos()
            if idx_combo >= len(ocorrencias):
                raise Exception("Ocorrência inválida.")
            
            oc_base = ocorrencias[idx_combo]
            
            dados = {
                "titulo": self.ent_titulo_alerta.get(),
                "mensagem": self.txt_msg_alerta.get("1.0", tk.END).strip(),
                "ocorrencia": oc_base,
                "escopo": self.combo_escopo.get(),
                "horario": datetime.now().strftime("%H:%M:%S")
            }

            novo_alerta = AlertaFactory.criar_alerta(**dados)
            # Salvar alerta no banco de dados
            self.alerta_repo.salvar(novo_alerta)
            messagebox.showinfo("Sucesso", "Alerta disparado para a população!")
            self.mostrar_dashboard()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def logica_cancelar_alerta(self, id_alerta):
        if messagebox.askyesno("Confirmar", "Deseja cancelar este alerta?"):
            # Remover alerta do banco de dados
            self.alerta_repo.excluir(id_alerta)
            self.mostrar_dashboard()

    # Altera propriedades de um atendimento selecionado ou encerra seu ciclo básico
    def logica_atualizar_atendimento(self, tabela, lista_atendimentos):
        item_selecionado = tabela.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um atendimento!")
            return

        valores = tabela.item(item_selecionado)['values']
        id_at = valores[0]
        at_obj = next((a for a in lista_atendimentos if a.id == id_at), None)

        if at_obj:
            novo_grau = "alta"
            at_obj.alterarUrgencia(novo_grau)
            at_obj.encerrarAtendimento()
            
            messagebox.showinfo("Sucesso", "Atendimento atualizado!")
            self.mostrar_dashboard()

    # Localiza o objeto de atendimento e chama a interface de análise técnica
    def preparar_analise_atendimento(self, tabela, lista_ats):
            item_selecionado = tabela.selection()
            if not item_selecionado:
                messagebox.showwarning("Aviso", "Selecione um atendimento na lista!")
                return

            valores = tabela.item(item_selecionado)['values']
            id_at = valores[0]
            
            atendimento = next((at for at in lista_ats if at.id == id_at), None)
            
            if atendimento:
                from infrastructure.api.screens.atendenteScreen import AtendenteScreen
                AtendenteScreen.render_analisar_atendimento(self, atendimento, self.area_conteudo)

    # Define urgência, vincula equipe e encerra a fase de triagem da ocorrência
    def processar_despacho_final(self, atendimento):
        try:
            urgencia = self.ent_urgencia.get()
            relatorio = self.txt_relatorio.get("1.0", tk.END).strip()
            idx_equipe = self.ent_equipe_resgate.current()

            if not urgencia or idx_equipe == -1:
                messagebox.showwarning("Aviso", "Preencha a urgência e selecione uma equipe!")
                return

            atendimento.grauUrgencia = urgencia
            atendimento.ocorrencia.complemento = relatorio
            
            equipes = self.equipe_repo.listarTodos()
            if idx_equipe >= len(equipes):
                raise Exception("Equipe inválida.")
            
            equipe_sel = equipes[idx_equipe]
            
            if hasattr(equipe_sel, 'agentes'):
                for agente in equipe_sel.agentes:
                    agente.status = "Em ocorrência"
            
            equipe_sel.status = "Em ocorrência"
            self.equipe_repo.salvar(equipe_sel)
            
            atendimento.ocorrencia.equipe = equipe_sel
            atendimento.ocorrencia.status = "Encaminhada para Resgate"
            self.ocorrencia_repo.salvar(atendimento.ocorrencia)

            atendimento.finalizarAtendimento([])
            self.atendimento_repo.salvar(atendimento)

            messagebox.showinfo("Sucesso", f"Ocorrência #{atendimento.ocorrencia.id} despachada com sucesso!")
            self.mostrar_dashboard()

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao processar despacho: {e}")

    # Atualiza o status da ocorrência e de sua equipe para o início das atividades de campo
    def logica_iniciar_resgate_direto(self, ocorrencia, container):
        try:
            ocorrencia.status = "Em Resgate"
            if ocorrencia.equipe:
                ocorrencia.equipe.status = "Em atendimento"
                for agente in ocorrencia.equipe.agentes:
                    agente.status = "Em ocorrência"
                self.equipe_repo.salvar(ocorrencia.equipe)
            
            # Salvar ocorrência atualizada
            self.ocorrencia_repo.salvar(ocorrencia)
            
            messagebox.showinfo("Sucesso", f"Resgate iniciado para a Ocorrência #{ocorrencia.id}")
            
            from infrastructure.api.screens.agenteScreen import AgenteScreen
            AgenteScreen.render_painel_operacional(self, container)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível iniciar o resgate: {e}")

    # Valida pendências, gera histórico e finaliza o ciclo de vida de uma ocorrência
    def logica_concluir_resgate_direto(self, ocorrencia, relato, total_vitimas):
        try:
            # 1. Validação de Vítimas Perdidas
            v_perdidas = self.vitima_repo.buscarPorSituacao("Perdido")
            v_perdidas = [v for v in v_perdidas if v.ocorrencia == ocorrencia.id]
            if v_perdidas:
                return messagebox.showerror("Erro", "Há vítimas com status 'Perdido'. Resolva antes de fechar.")
            
            agora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            
            novo_resgate = Resgate(
                ocorrencia=ocorrencia,
                dataInicio=ocorrencia.dataHora, 
                descricao=relato,
                dataFim=agora,
                qtdResgatados=total_vitimas
            )
            
            # Salvar resgate no banco de dados
            self.resgate_repo.salvar(novo_resgate)

            ocorrencia.status = "Finalizada"
            ocorrencia.hora_finalizado = agora 
            
            if ocorrencia.equipe:
                ocorrencia.equipe.status = "Disponível"
                for ag in ocorrencia.equipe.agentes:
                    ag.status = "Disponível"
                self.equipe_repo.salvar(ocorrencia.equipe)
            
            # Salvar ocorrência finalizada
            self.ocorrencia_repo.salvar(ocorrencia)

            messagebox.showinfo("Sucesso", "Resgate finalizado e histórico salvo!")
            self.mostrar_dashboard()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao fechar resgate: {e}")
            
    # Cria uma nova instância de vítima vinculada a uma ocorrência e salva no banco
    def logica_salvar_vitima(self, nome, situacao, oc_str):
        if not nome or not situacao or not oc_str:
            return messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
        
        try:
            id_oc = int(oc_str.split(" - ")[0])
            oc = next(o for o in self.db["ocorrencias"] if o.id == id_oc)
            
            
            messagebox.showinfo("Sucesso", f"Vítima {nome} vinculada à ocorrência #{id_oc}")
            self.mostrar_dashboard()
            
        except StopIteration:
            messagebox.showerror("Erro", "Ocorrência selecionada não foi encontrada no sistema.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar vítima: {str(e)}")