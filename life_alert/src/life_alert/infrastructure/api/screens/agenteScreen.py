import tkinter as tk
from tkinter import ttk, messagebox
from application.equipeFactory import EquipeFactory
from application.vitimaFactory import VitimaFactory

class AgenteScreen:
    
    @staticmethod
    def render_menu_equipes(gui, container):
        """Lista as equipes e contém o botão para CRIAR nova equipe"""
        for w in container.winfo_children(): w.destroy()
        
        header_frame = tk.Frame(container, bg="#f4f7fb")
        header_frame.pack(fill=tk.X, pady=20, padx=50)

        tk.Label(header_frame, text="MINHAS EQUIPES", font=gui.font_header, bg="#f4f7fb", fg="#2b6cb0").pack(side=tk.LEFT)
        
        tk.Button(header_frame, text="+ Nova Equipe", bg="#2f855a", fg="white", font=("Segoe UI", 9, "bold"),
                  command=lambda: AgenteScreen.render_criar_equipe(gui, container)).pack(side=tk.RIGHT)
        
        equipes = [e for e in gui.db.get("equipes", []) if gui.usuario_logado in e.agentes]
        
        if not equipes:
            tk.Label(container, text="Você não está vinculado a nenhuma equipe.", bg="#f4f7fb", fg="#6b7280").pack(pady=50)
            return

        for eq in equipes:
            card = tk.Frame(container, bg="white", padx=15, pady=15, relief=tk.RAISED, borderwidth=1)
            card.pack(fill=tk.X, padx=50, pady=10)
            
            tk.Label(card, text=f"Equipe #{eq.id} - {eq.especialidade}", font=("Segoe UI", 11, "bold"), bg="white").pack(side=tk.LEFT)
            
            btn_frame = tk.Frame(card, bg="white")
            btn_frame.pack(side=tk.RIGHT)
            
            tk.Button(btn_frame, text="Status", command=lambda e=eq: AgenteScreen.exibir_membros(gui, e)).pack(side=tk.LEFT, padx=5)
            tk.Button(btn_frame, text="Membros", command=lambda e=eq: AgenteScreen.render_gerenciar_membros_equipe(gui, container, e)).pack(side=tk.LEFT, padx=5)
            tk.Button(btn_frame, text="Resgates", bg="#2b6cb0", fg="white", command=lambda e=eq: AgenteScreen.render_resgates_equipe(gui, container, e)).pack(side=tk.LEFT, padx=5)

    @staticmethod
    @staticmethod
    def render_gerenciar_membros_equipe(gui, container, equipe):
        """Tela para adicionar ou remover agentes da equipe (Filtrado por cidade)"""
        for w in container.winfo_children(): w.destroy()
        
        tk.Label(container, text=f"MEMBROS DA EQUIPE #{equipe.id}", font=gui.font_header, bg="#f4f7fb").pack(pady=20)
        
        # Informativo da Cidade do Agente Logado
        cidade_logado = gui.usuario_logado.cidade
        tk.Label(container, text=f"📍 Operando em: {cidade_logado}", font=("Segoe UI", 9, "bold"), 
                 bg="#f4f7fb", fg="#4a5568").pack()

        main_frame = tk.Frame(container, bg="#f4f7fb")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Lado Esquerdo: Membros Atuais
        left = tk.Frame(main_frame, bg="white", padx=15, pady=15, relief=tk.GROOVE, borderwidth=1)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        tk.Label(left, text="No Time", font=("Segoe UI", 10, "bold"), bg="white", fg="#c53030").pack(pady=5)
        
        for ag in equipe.agentes:
            f = tk.Frame(left, bg="white")
            f.pack(fill=tk.X, pady=2)
            tk.Label(f, text=f"{ag.nome}", bg="white").pack(side=tk.LEFT)
            tk.Button(f, text="Remover", fg="red", relief=tk.FLAT, font=("Segoe UI", 8),
                      command=lambda a=ag: AgenteScreen.acao_remover_agente(gui, container, equipe, a)).pack(side=tk.RIGHT)

        # Lado Direito: Disponíveis (FILTRADOS POR CIDADE)
        right = tk.Frame(main_frame, bg="white", padx=15, pady=15, relief=tk.GROOVE, borderwidth=1)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        tk.Label(right, text="Disponíveis na Região", font=("Segoe UI", 10, "bold"), bg="white", fg="#2f855a").pack(pady=5)

        # REGRA DE NEGÓCIO: Tipo deve ser Agente, não pode estar na equipe e a cidade deve ser IGUAL à do logado
        disponiveis = [
            u for u in gui.db.get("usuarios", []) 
            if u.tipo == "Agente" 
            and u not in equipe.agentes 
            and u.cidade.strip().lower() == cidade_logado.strip().lower()
        ]

        if not disponiveis:
            tk.Label(right, text="Nenhum agente disponível nesta cidade.", 
                     font=("Segoe UI", 8, "italic"), bg="white", fg="#94a3b8").pack(pady=10)

        for ag in disponiveis:
            f = tk.Frame(right, bg="white")
            f.pack(fill=tk.X, pady=2)
            tk.Label(f, text=f"{ag.nome} ({ag.bairro})", bg="white").pack(side=tk.LEFT)
            tk.Button(f, text="Adicionar", fg="green", relief=tk.FLAT, font=("Segoe UI", 8),
                      command=lambda a=ag: AgenteScreen.acao_adicionar_agente(gui, container, equipe, a)).pack(side=tk.RIGHT)

        tk.Button(container, text="Voltar", command=lambda: AgenteScreen.render_menu_equipes(gui, container)).pack(pady=20)
    
    @staticmethod
    def render_painel_operacional(gui, container):
        """Visão restrita ao Agente: Apenas visualiza equipes e gerencia chamados"""
        for w in container.winfo_children(): w.destroy()
        
        header_frame = tk.Frame(container, bg="#f4f7fb")
        header_frame.pack(fill=tk.X, pady=20, padx=50)

        tk.Label(header_frame, text="MEUS CHAMADOS E EQUIPES", font=gui.font_header, bg="#f4f7fb", fg="#c53030").pack(side=tk.LEFT)
        
        # Filtra equipes onde o agente logado está presente
        equipes_do_agente = [e for e in gui.db.get("equipes", []) if gui.usuario_logado in e.agentes]
        
        if not equipes_do_agente:
            tk.Label(container, text="Você não está vinculado a nenhuma equipe ativa.", 
                     bg="#f4f7fb", fg="#6b7280", font=("Segoe UI", 11)).pack(pady=50)
            return

        for eq in equipes_do_agente:
            # Card da Equipe (Sem botões de editar membros ou criar)
            card = tk.Frame(container, bg="white", padx=20, pady=20, relief=tk.FLAT, highlightbackground="#e2e8f0", highlightthickness=1)
            card.pack(fill=tk.X, padx=50, pady=10)
            
            # Cabeçalho do Card
            header_card = tk.Frame(card, bg="white")
            header_card.pack(fill=tk.X)
            
            tk.Label(header_card, text=f"EQUIPE: {eq.especialidade} (#{eq.id})", font=("Segoe UI", 10, "bold"), bg="white", fg="#4a5568").pack(side=tk.LEFT)
            
            status_cor = "#2f855a" if eq.status == "Disponível" else "#e53e3e"
            tk.Label(header_card, text=f" STATUS: {eq.status.upper()} ", font=("Segoe UI", 8, "bold"), bg=status_cor, fg="white").pack(side=tk.RIGHT)

            # --- NOTIFICAÇÕES DE RESGATE ATRIBUÍDOS ---
            chamados = [o for o in gui.db.get("ocorrencias", []) if o.equipe == eq and o.status in ["Encaminhada para Resgate", "Em Resgate"]]
            
            if chamados:
                tk.Label(card, text="🔔 NOVOS RESGATES ATRIBUÍDOS:", font=("Segoe UI", 9, "bold"), bg="white", fg="#c53030").pack(anchor="w", pady=(15, 5))
                
                for oc in chamados:
                    resgate_box = tk.Frame(card, bg="#fff5f5", padx=15, pady=15, highlightbackground="#feb2b2", highlightthickness=1)
                    resgate_box.pack(fill=tk.X, pady=5)
                    
                    # Informações cruciais do local
                    info_local = f"📍 LOCALIZAÇÃO: {oc.rua}, {oc.bairro} - {oc.cidade}\n"
                    info_local += f"🕒 TIPO: {oc.tipo} | GRAVIDADE: {oc.gravidade}\n"
                    info_local += f"📝 RELATO: {oc.descricao[:100]}..."
                    
                    tk.Label(resgate_box, text=info_local, font=("Segoe UI", 9), bg="#fff5f5", justify="left").pack(side=tk.LEFT)
                    
                    # Ações de Campo
                    if oc.status == "Encaminhada para Resgate":
                        tk.Button(resgate_box, text="INICIAR DESLOCAMENTO", bg="#2b6cb0", fg="white", font=("Segoe UI", 9, "bold"),
                                  command=lambda o=oc: gui.logica_iniciar_resgate_direto(o, container)).pack(side=tk.RIGHT, padx=5)
                    else:
                        tk.Button(resgate_box, text="FINALIZAR OCORRÊNCIA", bg="#2f855a", fg="white", font=("Segoe UI", 9, "bold"),
                        command=lambda o=oc: AgenteScreen.render_fechar_resgate(gui, container, o)).pack(side=tk.RIGHT, padx=5)
            else:
                tk.Label(card, text="Nenhum chamado pendente para esta equipe no momento.", font=("Segoe UI", 9, "italic"), bg="white", fg="#a0aec0").pack(anchor="w", pady=10)

            # Lista rápida de membros (apenas leitura para o agente saber com quem está trabalhando)
            membros_nomes = ", ".join([ag.nome for ag in eq.agentes])
            tk.Label(card, text=f"Integrantes: {membros_nomes}", font=("Segoe UI", 8), bg="white", fg="#718096").pack(anchor="w", pady=(10, 0))

    @staticmethod
    def acao_adicionar_agente(gui, container, equipe, agente):
        equipe.adicionar_membro(agente)
        messagebox.showinfo("Sucesso", f"{agente.nome} adicionado!")
        AgenteScreen.render_gerenciar_membros_equipe(gui, container, equipe)

    @staticmethod
    def acao_remover_agente(gui, container, equipe, agente):
        equipe.remover_membro(agente.id)
        messagebox.showinfo("Sucesso", f"{agente.nome} removido!")
        AgenteScreen.render_gerenciar_membros_equipe(gui, container, equipe)
    
    @staticmethod
    def render_cadastrar_vitima(gui, container):
        for w in container.winfo_children(): w.destroy()
        tk.Label(container, text="REGISTRAR VÍTIMA", font=gui.font_header, bg="#f4f7fb").pack(pady=20)
        card = tk.Frame(container, bg="white", padx=20, pady=20)
        card.pack()

        ocs_ativas = [o for o in gui.db.get("ocorrencias", []) if o.status in ["Em Atendimento", "Em Resgate"]]
        tk.Label(card, text="Ocorrência:", bg="white").pack(anchor="w")
        cb_ocs = ttk.Combobox(card, values=[f"{o.id} - {o.tipo}" for o in ocs_ativas], width=40, state="readonly")
        cb_ocs.pack(pady=5)
        
        tk.Label(card, text="Nome da Vítima:", bg="white").pack(anchor="w")
        ent_nome = tk.Entry(card, width=43); ent_nome.pack(pady=5)
        
        tk.Label(card, text="Situação:", bg="white").pack(anchor="w")
        # --- ATUALIZADO: OPÇÕES ESPECÍFICAS ---
        cb_sit = ttk.Combobox(card, values=["Ferimentos leves", "Situação grave", "Óbito", "Perdido","Bom estado"], width=40, state="readonly")
        cb_sit.pack(pady=5)

        def salvar():
            try:
                if not cb_ocs.get() or not cb_sit.get():
                    return messagebox.showwarning("Aviso", "Selecione a ocorrência e a situação!")
                
                id_oc = int(cb_ocs.get().split(" - ")[0])
                oc_sel = next(o for o in ocs_ativas if o.id == id_oc)
                nova_v = VitimaFactory.criar(ent_nome.get(), "N/A", cb_sit.get(), oc_sel)
                if "vitimas" not in gui.db: gui.db["vitimas"] = []
                gui.db["vitimas"].append(nova_v)
                messagebox.showinfo("Sucesso", "Vítima registrada!")
                AgenteScreen.render_gerenciar_vitimas(gui, container)
            except Exception as e: 
                messagebox.showerror("Erro", f"Falha ao registrar: {e}")

        tk.Button(card, text="SALVAR", bg="#2f855a", fg="white", command=salvar).pack(fill=tk.X, pady=10)
        tk.Button(container, text="Cancelar", command=lambda: AgenteScreen.render_gerenciar_vitimas(gui, container)).pack(pady=10)

    @staticmethod
    def render_gerenciar_vitimas(gui, container):
        for w in container.winfo_children(): w.destroy()
        header = tk.Frame(container, bg="#f4f7fb")
        header.pack(fill=tk.X, pady=20, padx=20)

        tk.Label(header, text="GERENCIAR VÍTIMAS", font=gui.font_header, bg="#f4f7fb", fg="#2b6cb0").pack(side=tk.LEFT)
        tk.Button(header, text="+ Registrar Vítima", bg="#2f855a", fg="white", command=lambda: AgenteScreen.render_cadastrar_vitima(gui, container)).pack(side=tk.RIGHT)
        
        vitimas = gui.db.get("vitimas", [])
        cols = ("id", "nome", "situacao", "ocorrencia")
        tabela = ttk.Treeview(container, columns=cols, show="headings")
        for c in cols: tabela.heading(c, text=c.capitalize())
        
        for i, v in enumerate(vitimas):
            tabela.insert("", tk.END, values=(i, v.nome, v.situacao, v.ocorrencia.tipo))
        
        tabela.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

        frame_act = tk.Frame(container, bg="#f4f7fb")
        frame_act.pack(pady=10)
        
        tk.Label(frame_act, text="Atualizar Situação:", bg="#f4f7fb").pack(side=tk.LEFT)
        # --- ATUALIZADO: SELECT PARA ATUALIZAÇÃO ---
        cb_nova_sit = ttk.Combobox(frame_act, values=["Ferimentos leves", "Situação grave", "Óbito", "Perdido","Bom estado"], state="readonly")
        cb_nova_sit.pack(side=tk.LEFT, padx=10)
        
        def atualizar():
            sel = tabela.selection()
            if not sel: return messagebox.showwarning("Aviso", "Selecione uma vítima!")
            
            idx = tabela.item(sel)['values'][0]
            nova_sit = cb_nova_sit.get()
            
            if not nova_sit: return
            
            if vitimas[idx].atualizar_situacao(nova_sit):
                messagebox.showinfo("Sucesso", "Situação da vítima atualizada!")
                AgenteScreen.render_gerenciar_vitimas(gui, container)

        tk.Button(frame_act, text="Salvar Alteração", bg="#2b6cb0", fg="white", command=atualizar).pack(side=tk.LEFT)

    @staticmethod
    def render_criar_equipe(gui, container):
        for w in container.winfo_children(): w.destroy()
        tk.Label(container, text="CADASTRAR EQUIPE", font=gui.font_header, bg="#f4f7fb").pack(pady=20)
        card = tk.Frame(container, bg="white", padx=30, pady=30, relief=tk.RAISED, borderwidth=1)
        card.pack()
        
        labels = ["Localidade da Base", "Setor", "Especialidade"]
        ents = []
        for l in labels:
            tk.Label(card, text=l, bg="white").pack(anchor="w")
            e = tk.Entry(card, width=40); e.pack(pady=(0,10)); ents.append(e)

        def salvar():
            try:
                eq = EquipeFactory.criar_equipe(gui.usuario_logado, ents[0].get(), ents[1].get(), ents[2].get())
                if "equipes" not in gui.db: gui.db["equipes"] = []
                gui.db["equipes"].append(eq)
                messagebox.showinfo("Sucesso", "Equipe criada!")
                AgenteScreen.render_menu_equipes(gui, container)
            except Exception as e: messagebox.showerror("Erro", str(e))

        tk.Button(card, text="CRIAR", bg="#2f855a", fg="white", command=salvar).pack(fill=tk.X)
        tk.Button(container, text="Cancelar", command=lambda: AgenteScreen.render_menu_equipes(gui, container)).pack(pady=10)

    @staticmethod
    def exibir_membros(gui, equipe):
        janela = tk.Toplevel()
        janela.title("Status da Equipe")
        for ag in equipe.agentes:
            tk.Label(janela, text=f"{ag.nome} ({ag.cargo}) - {ag.status}").pack(padx=20, pady=5)

    @staticmethod
    def render_resgates_equipe(gui, container, equipe):
        for w in container.winfo_children(): w.destroy()
        tk.Label(container, text=f"RESGATES - EQUIPE #{equipe.id}", font=gui.font_header).pack(pady=20)
        ocs = [o for o in gui.db.get("ocorrencias", []) if o.equipe == equipe]
        
        if not ocs:
            tk.Label(container, text="Nenhum resgate vinculado.").pack()
        else:
            for oc in ocs:
                f = tk.Frame(container, bg="white", pady=10, relief=tk.GROOVE, borderwidth=1)
                f.pack(fill=tk.X, padx=50, pady=5)
                tk.Label(f, text=f"#{oc.id} - {oc.tipo} ({oc.status})", bg="white").pack(side=tk.LEFT, padx=10) 
        tk.Button(container, text="Voltar", command=lambda: AgenteScreen.render_menu_equipes(gui, container)).pack(pady=20)

    @staticmethod
    @staticmethod
    def render_relatorios(gui, container):
        from application.relatorioService import RelatorioService
        
        for w in container.winfo_children(): w.destroy()
        
        tk.Label(container, text="RELATÓRIOS E ESTATÍSTICAS", font=gui.font_header, bg="#f4f7fb", fg="#2b6cb0").pack(pady=20)
        
        card_filtro = tk.Frame(container, bg="white", padx=20, pady=20, relief=tk.GROOVE, borderwidth=1)
        card_filtro.pack(pady=10)

        # Helper para máscara de data (00/00/0000)
        def formatar_data(event):
            text = event.widget.get().replace("/", "")[:8]
            new_text = ""
            for i, char in enumerate(text):
                if i in [2, 4]: new_text += "/"
                new_text += char
            event.widget.delete(0, tk.END)
            event.widget.insert(0, new_text)

        tk.Label(card_filtro, text="Data Inicial (DD/MM/AAAA):", bg="white").grid(row=0, column=0, padx=5, pady=5)
        ent_ini = tk.Entry(card_filtro, width=15)
        ent_ini.grid(row=0, column=1, padx=5, pady=5)
        ent_ini.bind("<KeyRelease>", formatar_data)

        tk.Label(card_filtro, text="Data Final (DD/MM/AAAA):", bg="white").grid(row=1, column=0, padx=5, pady=5)
        ent_fim = tk.Entry(card_filtro, width=15)
        ent_fim.grid(row=1, column=1, padx=5, pady=5)
        ent_fim.bind("<KeyRelease>", formatar_data)

        # Container para os resultados
        res_container = tk.Frame(container, bg="#f4f7fb")
        res_container.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)

        def executar_geracao():
            try:
                # Limpa resultados anteriores
                for w in res_container.winfo_children(): w.destroy()
                
                # Chama o serviço
                relatorio = RelatorioService.gerar_estatisticas(
                    gui.db.get("ocorrencias", []), 
                    ent_ini.get(), 
                    ent_fim.get()
                )
                
                # Exibe Resultados
                tk.Label(res_container, text=f"Resumo de {ent_ini.get()} a {ent_fim.get()}", font=("Segoe UI", 10, "bold"), bg="#f4f7fb").pack()
                
                res_card = tk.Frame(res_container, bg="white", padx=20, pady=20, relief=tk.RAISED, borderwidth=1)
                res_card.pack(fill=tk.X, pady=10)

                tk.Label(res_card, text=f"Total de Ocorrências: {relatorio.estatisticas['total']}", font=("Segoe UI", 11), bg="white").pack(anchor="w")
                tk.Label(res_card, text=f"Tempo Médio de Atendimento: {relatorio.estatisticas['media_atendimento']} min", font=("Segoe UI", 11), bg="white").pack(anchor="w")
                
                tk.Label(res_card, text="\nPor Tipo:", font=("Segoe UI", 10, "bold"), bg="white").pack(anchor="w")
                for tipo, qtd in relatorio.estatisticas['tipos'].items():
                    tk.Label(res_card, text=f"• {tipo}: {qtd}", bg="white", padx=10).pack(anchor="w")

            except ValueError:
                messagebox.showerror("Erro", "Formato de data inválido! Use DD/MM/AAAA")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao gerar: {e}")

        tk.Button(card_filtro, text="GERAR RELATÓRIO", bg="#2b6cb0", fg="white", font=("Segoe UI", 9, "bold"),
                  command=executar_geracao).grid(row=2, columnspan=2, pady=15, sticky="ew")

    @staticmethod
    def render_fechar_resgate(gui, container, ocorrencia):
        """Tela para o agente dar o relato final e confirmar dados"""
        for w in container.winfo_children(): w.destroy()
        
        # Busca vítimas vinculadas no banco para contar
        vitimas_vinculadas = [v for v in gui.db.get("vitimas", []) if v.ocorrencia.id == ocorrencia.id]
        total = len(vitimas_vinculadas)

        tk.Label(container, text="RELATÓRIO FINAL DE RESGATE", font=gui.font_header, bg="#f4f7fb").pack(pady=20)
        
        card = tk.Frame(container, bg="white", padx=20, pady=20, relief=tk.GROOVE, borderwidth=1)
        card.pack(pady=10)

        tk.Label(card, text=f"Ocorrência: {ocorrencia.tipo} (#{ocorrencia.id})", bg="white", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        tk.Label(card, text=f"Total de Vítimas Registradas: {total}", bg="white", fg="#2b6cb0").pack(anchor="w", pady=5)
        
        tk.Label(card, text="Relato Final das Atividades:", bg="white").pack(anchor="w", pady=(10,0))
        txt_relato = tk.Text(card, width=50, height=6, font=("Segoe UI", 9))
        txt_relato.pack(pady=5)

        def confirmar():
            relato = txt_relato.get("1.0", tk.END).strip()
            if len(relato) < 10:
                return messagebox.showwarning("Aviso", "Por favor, escreva um relato mais detalhado.")
            
            # Executa a lógica de encerramento enviando o relato e o total
            gui.logica_concluir_resgate_direto(ocorrencia, relato, total)

        tk.Button(card, text="CONCLUIR E LIBERAR EQUIPE", bg="#2f855a", fg="white", 
                  font=("Segoe UI", 10, "bold"), command=confirmar, pady=10).pack(fill=tk.X, pady=10)