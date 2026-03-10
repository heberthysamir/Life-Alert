import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Permitir execução como script direto (para debug)
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    life_alert_root = os.path.join(current_dir, '../../..')
    if life_alert_root not in sys.path:
        sys.path.insert(0, life_alert_root)

from application.equipeFactory import EquipeFactory
from application.vitimaFactory import VitimaFactory

# Constantes de Estilo para consistência visual
PRIMARY = "#c53030"    
SECONDARY = "#2b6cb0"  
SUCCESS = "#2f855a"    
BG = "#f4f7fb"         
CARD = "#ffffff"       
TEXT = "#243444"     
MUTED = "#6b7280"      
BORDER = "#e2e8f0"     

class AgenteScreen:
    
    @staticmethod
    def render_menu_equipes(gui, container):
        """Lista as equipes onde o agente logado está vinculado"""
        for w in container.winfo_children(): w.destroy()
        
        header_frame = tk.Frame(container, bg=BG)
        header_frame.pack(fill=tk.X, pady=20, padx=50)

        tk.Label(header_frame, text="MINHAS EQUIPES", font=gui.font_header, bg=BG, fg=SECONDARY).pack(side=tk.LEFT)
        
        tk.Button(header_frame, text="+ Nova Equipe", bg=SUCCESS, fg="white", font=("Segoe UI", 9, "bold"),
                  command=lambda: AgenteScreen.render_criar_equipe(gui, container), cursor="hand2").pack(side=tk.RIGHT)
        
        # 1. Busca todas as equipes do banco via Repositório
        todas_equipes = gui.equipe_repo.listarTodos()
        
        # 2. Filtragem CORRIGIDA
        id_logado = gui.usuario_logado.id
        equipes_vinculadas = [
            eq for eq in todas_equipes 
            if any(str(ag.id) == str(id_logado) for ag in eq.agentes if hasattr(ag, 'id'))
        ]

        # 3. Renderização da UI
        if not equipes_vinculadas:
            tk.Label(container, text="Você não está vinculado a nenhuma equipe no banco de dados.", 
                     bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack(pady=50)
            tk.Button(container, text="🔄 Atualizar Lista", bg=BORDER, 
                      command=lambda: AgenteScreen.render_menu_equipes(gui, container)).pack()
            return

        # 2. Filtragem única e robusta
        for eq in todas_equipes:
            # Extraímos IDs garantindo que o agente existe e convertendo para string
            ids_agentes = []
            for ag in eq.agentes:
                if ag and hasattr(ag, 'id'):
                    ids_agentes.append(str(ag.id))
        
        # 3. Renderização da UI
        if not equipes_vinculadas:
            tk.Label(container, text="Você não está vinculado a nenhuma equipe no banco de dados.", 
                     bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack(pady=50)
            # Botão de auxílio caso o banco esteja vazio mas o usuário queira recarregar
            tk.Button(container, text="Atualizar Lista", command=lambda: AgenteScreen.render_menu_equipes(gui, container)).pack()
            return

        for eq in equipes_vinculadas:
            card = tk.Frame(container, bg=CARD, padx=15, pady=15, relief=tk.RAISED, borderwidth=1)
            card.pack(fill=tk.X, padx=50, pady=10)
            
            tk.Label(card, text=f"Equipe #{eq.id} - {eq.especialidade}", 
                     font=("Segoe UI", 11, "bold"), bg=CARD, fg=TEXT).pack(side=tk.LEFT)
            
            btn_frame = tk.Frame(card, bg=CARD)
            btn_frame.pack(side=tk.RIGHT)
            
            tk.Button(btn_frame, text="Status", command=lambda e=eq: AgenteScreen.exibir_membros(gui, e)).pack(side=tk.LEFT, padx=5)
            tk.Button(btn_frame, text="Membros", command=lambda e=eq: AgenteScreen.render_gerenciar_membros_equipe(gui, container, e)).pack(side=tk.LEFT, padx=5)
            tk.Button(btn_frame, text="Resgates", bg=SECONDARY, fg="white", command=lambda e=eq: AgenteScreen.render_resgates_equipe(gui, container, e)).pack(side=tk.LEFT, padx=5)
            
    @staticmethod
    def render_gerenciar_membros_equipe(gui, container, equipe):
        """
        Interface para gestão de integrantes da equipe. 
        Aplica regra de negócio: apenas agentes da mesma cidade do usuário logado podem ser adicionados.
        """
        for w in container.winfo_children(): w.destroy()
        
        tk.Label(container, text=f"MEMBROS DA EQUIPE #{equipe.id}", font=gui.font_header, bg=BG).pack(pady=20)
        
        cidade_logado = gui.usuario_logado.cidade
        tk.Label(container, text=f"📍 Operando em: {cidade_logado}", font=("Segoe UI", 9, "bold"), 
                 bg=BG, fg="#4a5568").pack()

        main_frame = tk.Frame(container, bg=BG)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # PAINEL ESQUERDA: Agentes que já estão na equipe
        left = tk.Frame(main_frame, bg=CARD, padx=15, pady=15, relief=tk.GROOVE, borderwidth=1)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        tk.Label(left, text="No Time", font=("Segoe UI", 10, "bold"), bg=CARD, fg=PRIMARY).pack(pady=5)
        
        # Guardamos os IDs dos membros atuais para filtrar a lista da direita
        ids_no_time = [str(ag.id) for ag in equipe.agentes if hasattr(ag, 'id')]

        for ag in equipe.agentes:
            f = tk.Frame(left, bg=CARD)
            f.pack(fill=tk.X, pady=2)
            tk.Label(f, text=f"{ag.nome}", bg=CARD, fg=TEXT).pack(side=tk.LEFT)
            tk.Button(f, text="Remover", fg=PRIMARY, relief=tk.FLAT, font=("Segoe UI", 8),
                      command=lambda a=ag: AgenteScreen.acao_remover_agente(gui, container, equipe, a)).pack(side=tk.RIGHT)

        # PAINEL DIREITA: Agentes disponíveis no banco para a mesma cidade
        right = tk.Frame(main_frame, bg=CARD, padx=15, pady=15, relief=tk.GROOVE, borderwidth=1)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        tk.Label(right, text="Disponíveis na Região", font=("Segoe UI", 10, "bold"), bg=CARD, fg=SUCCESS).pack(pady=5)

        # --- CORREÇÃO: Busca via Repositório e Filtro de Cidade Robusto ---
        todos_usuarios = gui.usuario_repo.listarTodos()
        
        disponiveis = [
            u for u in todos_usuarios 
            if u.tipo == "Agente" 
            and str(u.id) not in ids_no_time 
            and str(u.cidade).strip().lower() == str(cidade_logado).strip().lower()
        ]

        if not disponiveis:
            tk.Label(right, text="Nenhum agente disponível nesta cidade.", 
                     font=("Segoe UI", 8, "italic"), bg=CARD, fg=MUTED).pack(pady=10)

        for ag in disponiveis:
            f = tk.Frame(right, bg=CARD)
            f.pack(fill=tk.X, pady=2)
            # Exibe bairro se disponível, senão apenas o nome
            txt_agente = f"{ag.nome} ({ag.bairro})" if hasattr(ag, 'bairro') and ag.bairro else ag.nome
            tk.Label(f, text=txt_agente, bg=CARD, fg=TEXT).pack(side=tk.LEFT)
            tk.Button(f, text="Adicionar", fg=SUCCESS, relief=tk.FLAT, font=("Segoe UI", 8),
                      command=lambda a=ag: AgenteScreen.acao_adicionar_agente(gui, container, equipe, a)).pack(side=tk.RIGHT)

        tk.Button(container, text="Voltar", command=lambda: AgenteScreen.render_menu_equipes(gui, container)).pack(pady=20)
    
    @staticmethod
    def render_painel_operacional(gui, container):
        """Visão tática com dados vindos do repositório."""
        for w in container.winfo_children(): w.destroy()
        
        header_frame = tk.Frame(container, bg=BG)
        header_frame.pack(fill=tk.X, pady=20, padx=50)

        tk.Label(header_frame, text="MEUS CHAMADOS E EQUIPES", font=gui.font_header, bg=BG, fg=PRIMARY).pack(side=tk.LEFT)
        
        # BUSCA NO BANCO E COMPARA PELO ID
        todas_equipes = gui.equipe_repo.listarTodos()
        equipes_do_agente = [
            e for e in todas_equipes 
            if any(ag.id == gui.usuario_logado.id for ag in e.agentes)
        ]
        
        if not equipes_do_agente:
            tk.Label(container, text="Você não está vinculado a nenhuma equipe ativa.", 
                     bg=BG, fg=MUTED, font=("Segoe UI", 11)).pack(pady=50)
            return

        for eq in equipes_do_agente:
            card = tk.Frame(container, bg=CARD, padx=20, pady=20, relief=tk.FLAT, highlightbackground=BORDER, highlightthickness=1)
            card.pack(fill=tk.X, padx=50, pady=10)
            
            header_card = tk.Frame(card, bg=CARD)
            header_card.pack(fill=tk.X)
            
            tk.Label(header_card, text=f"EQUIPE: {eq.especialidade} (#{eq.id})", font=("Segoe UI", 10, "bold"), bg=CARD, fg="#4a5568").pack(side=tk.LEFT)
            
            status_cor = SUCCESS if eq.status == "Disponível" else PRIMARY
            tk.Label(header_card, text=f" STATUS: {eq.status.upper()} ", font=("Segoe UI", 8, "bold"), bg=status_cor, fg="white").pack(side=tk.RIGHT)

            todas_ocs_banco = gui.ocorrencia_repo.listarTodos()

            # 2. Filtre usando IDs para garantir a precisão
            chamados = [
                o for o in todas_ocs_banco 
                if o.equipe is not None 
                and str(o.equipe.id) == str(eq.id) 
                and o.status in ["Encaminhada para Resgate", "Em Resgate"]
            ]
            
            if chamados:
                tk.Label(card, text="🔔 NOVOS RESGATES ATRIBUÍDOS:", font=("Segoe UI", 9, "bold"), bg=CARD, fg=PRIMARY).pack(anchor="w", pady=(15, 5))
                
                for oc in chamados:
                    resgate_box = tk.Frame(card, bg="#fff5f5", padx=15, pady=15, highlightbackground="#feb2b2", highlightthickness=1)
                    resgate_box.pack(fill=tk.X, pady=5)
                    
                    info_local = f"📍 LOCALIZAÇÃO: {oc.rua}, {oc.bairro} - {oc.cidade}\n"
                    info_local += f"🕒 TIPO: {oc.tipo} | GRAVIDADE: {oc.gravidade}\n"
                    info_local += f"📝 RELATO: {oc.descricao[:100]}..."
                    
                    tk.Label(resgate_box, text=info_local, font=("Segoe UI", 9), bg="#fff5f5", justify="left").pack(side=tk.LEFT)
                    
                    if oc.status == "Encaminhada para Resgate":
                        tk.Button(resgate_box, text="INICIAR DESLOCAMENTO", bg=SECONDARY, fg="white", font=("Segoe UI", 9, "bold"),
                                  command=lambda o=oc: gui.logica_iniciar_resgate_direto(o, container)).pack(side=tk.RIGHT, padx=5)
                    else:
                        tk.Button(resgate_box, text="FINALIZAR OCORRÊNCIA", bg=SUCCESS, fg="white", font=("Segoe UI", 9, "bold"),
                        command=lambda o=oc: AgenteScreen.render_fechar_resgate(gui, container, o)).pack(side=tk.RIGHT, padx=5)
            else:
                tk.Label(card, text="Nenhum chamado pendente para esta equipe no momento.", font=("Segoe UI", 9, "italic"), bg=CARD, fg="#a0aec0").pack(anchor="w", pady=10)

            membros_nomes = ", ".join([ag.nome for ag in eq.agentes])
            tk.Label(card, text=f"Integrantes: {membros_nomes}", font=("Segoe UI", 8), bg=CARD, fg="#718096").pack(anchor="w", pady=(10, 0))

    @staticmethod
    def acao_adicionar_agente(gui, container, equipe, agente):
        sucesso = gui.equipe_repo.adicionarAgente(equipe.id, agente.id)
        if sucesso:
            ja_esta_no_time = any(str(ag.id) == str(agente.id) for ag in equipe.agentes)
            
            if not ja_esta_no_time:
                equipe.agentes.append(agente)
            
            messagebox.showinfo("Sucesso", f"{agente.nome} adicionado!")
            AgenteScreen.render_gerenciar_membros_equipe(gui, container, equipe)
        else:
            messagebox.showerror("Erro", "Não foi possível adicionar o agente no banco.")

    @staticmethod
    def acao_remover_agente(gui, container, equipe, agente):
        sucesso = gui.equipe_repo.removerAgente(equipe.id, agente.id)
        if sucesso:
            # Remove do objeto em memória
            equipe.agentes = [a for a in equipe.agentes if a.id != agente.id]
            messagebox.showinfo("Sucesso", f"{agente.nome} removido!")
        
        AgenteScreen.render_gerenciar_membros_equipe(gui, container, equipe)
    
    @staticmethod
    def render_cadastrar_vitima(gui, container):
        for w in container.winfo_children(): w.destroy()
        tk.Label(container, text="REGISTRAR VÍTIMA", font=gui.font_header, bg=BG).pack(pady=20)
        card = tk.Frame(container, bg=CARD, padx=20, pady=20)
        card.pack()

        # --- BUSCA USANDO O REPOSITÓRIO (Sincronizado com o Banco) ---
        todas_ocs = gui.ocorrencia_repo.listarTodos()
        
        # Filtramos as ocorrências que estão em campo (Atendimento ou Resgate)
        ocs_ativas = [o for o in todas_ocs if o.status in ["Em Atendimento", "Em Resgate", "Encaminhada para Resgate"]]

        tk.Label(card, text="Ocorrência:", bg=CARD, fg=TEXT).pack(anchor="w")
        
        # Criamos as strings para o Combobox
        valores_cb = [f"{o.id} - {o.tipo}" for o in ocs_ativas]
        
        cb_ocs = ttk.Combobox(card, values=valores_cb, width=40, state="readonly")
        cb_ocs.pack(pady=5)
        
        if not ocs_ativas:
            cb_ocs.set("Nenhuma ocorrência ativa encontrada")

        tk.Label(card, text="Nome da Vítima:", bg=CARD, fg=TEXT).pack(anchor="w")
        ent_nome = tk.Entry(card, width=43)
        ent_nome.pack(pady=5)
        
        tk.Label(card, text="Situação:", bg=CARD, fg=TEXT).pack(anchor="w")
        cb_sit = ttk.Combobox(card, values=["Ferimentos leves", "Situação grave", "Óbito", "Perdido", "Bom estado"], width=40, state="readonly")
        cb_sit.pack(pady=5)

        def salvar():
            try:
                if not cb_ocs.get() or not cb_sit.get():
                    return messagebox.showwarning("Aviso", "Selecione a ocorrência e a situação!")
                
                # Pega o ID da string "12 - Médica" -> 12
                id_oc = int(cb_ocs.get().split(" - ")[0])
                oc_sel = next(o for o in ocs_ativas if o.id == id_oc)
                
                # IMPORTANTE: Enviamos 0 em vez de "N/A" para evitar o erro de conversão de int
                nova_v = VitimaFactory.criar(ent_nome.get(), 0, cb_sit.get(), oc_sel)
                
                # Salva no repositório de vítimas
                gui.vitima_repo.salvar(nova_v)
                
                messagebox.showinfo("Sucesso", "Vítima registrada no banco de dados!")
                AgenteScreen.render_gerenciar_vitimas(gui, container)
                
            except Exception as e: 
                messagebox.showerror("Erro", f"Falha ao registrar: {e}")

        # Use gui.PRIMARY ou uma cor hexadecimal se SUCCESS não estiver definido
        btn_cor = "#38a169" # Verde Sucesso
        tk.Button(card, text="SALVAR", bg=btn_cor, fg="white", command=salvar, pady=8, cursor="hand2").pack(fill=tk.X, pady=10)
        tk.Button(container, text="Cancelar", command=lambda: AgenteScreen.render_gerenciar_vitimas(gui, container)).pack(pady=10)

    @staticmethod
    def render_gerenciar_vitimas(gui, container):
        """Exibe listagem de vítimas registradas via Repositório."""
        for w in container.winfo_children(): w.destroy()
        
        header = tk.Frame(container, bg=BG)
        header.pack(fill=tk.X, pady=20, padx=20)

        tk.Label(header, text="GERENCIAR VÍTIMAS", font=gui.font_header, bg=BG, fg=SECONDARY).pack(side=tk.LEFT)
        tk.Button(header, text="+ Registrar Vítima", bg=SUCCESS, fg="white", 
                  command=lambda: AgenteScreen.render_cadastrar_vitima(gui, container), 
                  font=("Segoe UI", 9, "bold"), cursor="hand2").pack(side=tk.RIGHT)
        
        # --- BUSCA DO REPOSITÓRIO (Correção da persistência) ---
        if hasattr(gui, 'vitima_repo'):
            vitimas = gui.vitima_repo.listarTodos()
        else:
            vitimas = gui.db.get("vitimas", [])
        
        # Ajuste de colunas para mostrar o Resgate vinculado
        cols = ("id", "nome", "situacao", "resgate_id", "tipo_ocorrencia")
        tabela = ttk.Treeview(container, columns=cols, show="headings")
        
        tabela.heading("id", text="ID")
        tabela.heading("nome", text="Nome")
        tabela.heading("situacao", text="Situação")
        tabela.heading("resgate_id", text="Resgate #")
        tabela.heading("tipo_ocorrencia", text="Ocorrência")

        # Ajuste de largura das colunas
        tabela.column("id", width=40, anchor="center")
        tabela.column("resgate_id", width=80, anchor="center")
        lista_vitimas = gui.vitima_repo.listarTodos()

        for v in lista_vitimas:
            # O seu repositório coloca o ID no stub dentro de v.ocorrencia
            id_exibicao = v.ocorrencia.id if v.ocorrencia else "N/A"
            
            tabela.insert("", "end", values=(
                v.id, 
                v.nome, 
                v.situacao, 
                id_exibicao, # Coluna Resgate #
                id_exibicao  # Coluna Ocorrência
            ))
        
        tabela.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

        # --- AÇÕES DE ATUALIZAÇÃO ---
        frame_act = tk.Frame(container, bg=BG)
        frame_act.pack(pady=20)
        
        tk.Label(frame_act, text="Atualizar Situação da Vítima Selecionada:", bg=BG, fg=TEXT, font=("Segoe UI", 9)).pack(side=tk.LEFT)
        cb_nova_sit = ttk.Combobox(frame_act, values=["Ferimentos leves", "Situação grave", "Óbito", "Perdido", "Bom estado"], state="readonly")
        cb_nova_sit.pack(side=tk.LEFT, padx=10)
        
        def atualizar():
            sel = tabela.selection()
            if not sel: 
                return messagebox.showwarning("Aviso", "Selecione uma vítima na tabela abaixo!")
            
            # Recupera o objeto vítima original pelo ID
            item_id = tabela.item(sel)['values'][0]
            vitima_sel = next((v for v in vitimas if v.id == item_id), None)
            
            nova_sit = cb_nova_sit.get()
            if not nova_sit or not vitima_sel: return
            
            try:
                # Atualiza no objeto (domínio)
                vitima_sel.situacao = nova_sit 
                
                # Persiste no Banco via Repositório
                if hasattr(gui, 'vitima_repo'):
                    gui.vitima_repo.salvar(vitima_sel)
                
                messagebox.showinfo("Sucesso", f"Situação de {vitima_sel.nome} atualizada para {nova_sit}!")
                AgenteScreen.render_gerenciar_vitimas(gui, container)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível atualizar: {e}")

        tk.Button(frame_act, text="Salvar Alteração", bg=SECONDARY, fg="white", 
                  command=atualizar, padx=10).pack(side=tk.LEFT)
        
        tk.Button(container, text="Voltar ao Painel", 
                  command=lambda: AgenteScreen.render_painel_operacional(gui, container), 
                  relief=tk.FLAT).pack(pady=10)

    @staticmethod
    def render_criar_equipe(gui, container):
        """Interface para criação de novas equipes persistidas no banco."""
        for w in container.winfo_children(): w.destroy()
        tk.Label(container, text="CADASTRAR EQUIPE", font=gui.font_header, bg=BG).pack(pady=20)
        card = tk.Frame(container, bg=CARD, padx=30, pady=30, relief=tk.RAISED, borderwidth=1)
        card.pack()
        
        labels = ["Localidade da Base", "Setor", "Especialidade"]
        ents = []
        for l in labels:
            tk.Label(card, text=l, bg=CARD, fg=TEXT).pack(anchor="w")
            e = tk.Entry(card, width=40)
            e.pack(pady=(0,10))
            ents.append(e)

        def salvar():
            try:
                local = ents[0].get()
                setor = ents[1].get()
                espec = ents[2].get()
                
                if not all([local, setor, espec]):
                    return messagebox.showwarning("Aviso", "Preencha todos os campos!")

                # 1. Cria o objeto inicial
                nova_eq = EquipeFactory.criar_equipe(gui.usuario_logado, local, setor, espec)
                
                # 2. Garante que o agente criador está na lista (Factory deveria fazer isso, mas vamos garantir)
                if gui.usuario_logado not in nova_eq.agentes:
                    nova_eq.agentes.append(gui.usuario_logado)
                
                # 3. SALVA NO REPOSITÓRIO (BANCO)
                gui.equipe_repo.salvar(nova_eq)
                
                messagebox.showinfo("Sucesso", "Equipe criada e salva no banco de dados!")
                AgenteScreen.render_menu_equipes(gui, container)
            except Exception as e: 
                messagebox.showerror("Erro ao salvar no banco", str(e))
        
        tk.Button(card, text="CRIAR", bg=SUCCESS, fg="white", command=salvar, pady=8, font=("Segoe UI", 10, "bold")).pack(fill=tk.X)
        tk.Button(container, text="Cancelar", command=lambda: AgenteScreen.render_menu_equipes(gui, container)).pack(pady=10)

    @staticmethod
    def exibir_membros(gui, equipe):
        """Abre uma janela flutuante com o status atualizado de cada membro da equipe."""
        janela = tk.Toplevel()
        janela.title("Status da Equipe")
        janela.config(bg=BG)
        for ag in equipe.agentes:
            tk.Label(janela, text=f"{ag.nome} ({ag.cargo}) - {ag.status}", bg=BG, fg=TEXT, pady=5, padx=20).pack()

    @staticmethod
    def render_resgates_equipe(gui, container, equipe):
        """Lista o histórico de todas as ocorrências atendidas por uma equipe específica."""
        for w in container.winfo_children(): w.destroy()
        tk.Label(container, text=f"RESGATES - EQUIPE #{equipe.id}", font=gui.font_header, bg=BG).pack(pady=20)
        todas_ocs = gui.ocorrencia_repo.listarTodos()
        ocs = [
            o for o in todas_ocs 
            if o.equipe is not None and str(o.equipe.id) == str(equipe.id)
        ]
        if not ocs:
            tk.Label(container, text="Nenhum resgate vinculado.", bg=BG, fg=MUTED).pack()
        else:
            for oc in ocs:
                f = tk.Frame(container, bg=CARD, pady=10, relief=tk.GROOVE, borderwidth=1)
                f.pack(fill=tk.X, padx=50, pady=5)
                tk.Label(f, text=f"#{oc.id} - {oc.tipo} ({oc.status})", bg=CARD, fg=TEXT).pack(side=tk.LEFT, padx=10) 
        tk.Button(container, text="Voltar", command=lambda: AgenteScreen.render_menu_equipes(gui, container)).pack(pady=20)

    @staticmethod
    def render_relatorios(gui, container):
        """
        Gera visualização de estatísticas operacionais baseada em um intervalo de datas.
        Inclui tempo médio de atendimento e distribuição por tipo de ocorrência.
        """
        from application.relatorioService import RelatorioService
        
        for w in container.winfo_children(): w.destroy()
        
        tk.Label(container, text="RELATÓRIOS E ESTATÍSTICAS", font=gui.font_header, bg=BG, fg=SECONDARY).pack(pady=20)
        
        card_filtro = tk.Frame(container, bg=CARD, padx=20, pady=20, relief=tk.GROOVE, borderwidth=1)
        card_filtro.pack(pady=10)

        def formatar_data(event):
            text = event.widget.get().replace("/", "")[:8]
            new_text = ""
            for i, char in enumerate(text):
                if i in [2, 4]: new_text += "/"
                new_text += char
            event.widget.delete(0, tk.END)
            event.widget.insert(0, new_text)

        tk.Label(card_filtro, text="Data Inicial (DD/MM/AAAA):", bg=CARD, fg=TEXT).grid(row=0, column=0, padx=5, pady=5)
        ent_ini = tk.Entry(card_filtro, width=15)
        ent_ini.grid(row=0, column=1, padx=5, pady=5)
        ent_ini.bind("<KeyRelease>", formatar_data)

        tk.Label(card_filtro, text="Data Final (DD/MM/AAAA):", bg=CARD, fg=TEXT).grid(row=1, column=0, padx=5, pady=5)
        ent_fim = tk.Entry(card_filtro, width=15)
        ent_fim.grid(row=1, column=1, padx=5, pady=5)
        ent_fim.bind("<KeyRelease>", formatar_data)

        res_container = tk.Frame(container, bg=BG)
        res_container.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)

        def executar_geracao():
            try:
                for w in res_container.winfo_children(): w.destroy()
                todas_ocorrencias = gui.ocorrencia_repo.listarTodos()
                
                relatorio = RelatorioService.gerar_estatisticas(
                    todas_ocorrencias, 
                    ent_ini.get(), 
                    ent_fim.get()
                )
                # -------------------------------------------------------
                
                tk.Label(res_container, text=f"Resumo de {ent_ini.get()} a {ent_fim.get()}", 
                         font=("Segoe UI", 10, "bold"), bg=BG, fg=TEXT).pack()
                
                res_card = tk.Frame(res_container, bg=CARD, padx=20, pady=20, relief=tk.RAISED, borderwidth=1)
                res_card.pack(fill=tk.X, pady=10)

                tk.Label(res_card, text=f"Total de Ocorrências: {relatorio.estatisticas['total']}", 
                         font=("Segoe UI", 11), bg=CARD, fg=TEXT).pack(anchor="w")
                
                tk.Label(res_card, text=f"Tempo Médio de Atendimento: {relatorio.estatisticas['media_atendimento']} min", 
                         font=("Segoe UI", 11), bg=CARD, fg=TEXT).pack(anchor="w")
                
                tk.Label(res_card, text="\nPor Tipo:", font=("Segoe UI", 10, "bold"), bg=CARD, fg=TEXT).pack(anchor="w")
                
                if not relatorio.estatisticas['tipos']:
                    tk.Label(res_card, text="Nenhum dado por tipo disponível.", bg=CARD, fg=MUTED, padx=10).pack(anchor="w")
                else:
                    for tipo, qtd in relatorio.estatisticas['tipos'].items():
                        tk.Label(res_card, text=f"• {tipo}: {qtd}", bg=CARD, fg=TEXT, padx=10).pack(anchor="w")

            except ValueError:
                messagebox.showerror("Erro", "Formato de data inválido! Use DD/MM/AAAA")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao gerar: {e}")

        tk.Button(card_filtro, text="GERAR RELATÓRIO", bg=SECONDARY, fg="white", font=("Segoe UI", 9, "bold"),
                  command=executar_geracao, cursor="hand2").grid(row=2, columnspan=2, pady=15, sticky="ew")

    @staticmethod
    def render_fechar_resgate(gui, container, ocorrencia):
        for w in container.winfo_children(): w.destroy()
        
        # 1. Busca no banco via repositório
        todas_vitimas = gui.vitima_repo.listarTodos()
        
        # 2. Filtra vítimas da ocorrência atual
        vitimas_vinculadas = [
            v for v in todas_vitimas 
            if int(v.ocorrencia.id) == int(ocorrencia.id)
        ]
        total = len(vitimas_vinculadas)

        tk.Label(container, text="RELATÓRIO FINAL DE RESGATE", font=gui.font_header, bg=BG).pack(pady=20)
        
        card = tk.Frame(container, bg=CARD, padx=20, pady=20, relief=tk.GROOVE, borderwidth=1)
        card.pack(pady=10)

        tk.Label(card, text=f"Ocorrência: {ocorrencia.tipo} (#{ocorrencia.id})", 
                 bg=CARD, font=("Segoe UI", 10, "bold"), fg=TEXT).pack(anchor="w")
        tk.Label(card, text=f"Total de Vítimas Registradas: {total}", 
                 bg=CARD, fg=SECONDARY).pack(anchor="w", pady=5)
        
        # Listagem visual rápida das vítimas para o agente conferir
        if total > 0:
            v_frame = tk.Frame(card, bg="#f8fafc", pady=5)
            v_frame.pack(fill=tk.X, pady=5)
            for v in vitimas_vinculadas:
                cor_status = PRIMARY if v.situacao == "Perdido" else TEXT
                tk.Label(v_frame, text=f"• {v.nome}: {v.situacao}", 
                         bg="#f8fafc", fg=cor_status, font=("Segoe UI", 8)).pack(anchor="w")

        tk.Label(card, text="Relato Final das Atividades:", bg=CARD, fg=TEXT).pack(anchor="w", pady=(10,0))
        txt_relato = tk.Text(card, width=50, height=6, font=("Segoe UI", 9))
        txt_relato.pack(pady=5)

        def confirmar():
            relato = txt_relato.get("1.0", tk.END).strip()
            
            # --- LÓGICA DE BLOQUEIO: VÍTIMA PERDIDA ---
            # Verifica se alguma vítima vinculada ainda tem o status "Perdido"
            vitimas_perdidas = [v.nome for v in vitimas_vinculadas if v.situacao == "Perdido"]
            
            if vitimas_perdidas:
                nomes = ", ".join(vitimas_perdidas)
                return messagebox.showerror(
                    "RESGATE INCOMPLETO", 
                    f"Não é possível concluir o resgate!\n\nAs seguintes vítimas ainda constam como PERDIDAS:\n{nomes}\n\nAtualize o status delas antes de liberar a equipe."
                )
            # ------------------------------------------

            if len(relato) < 10:
                return messagebox.showwarning("Aviso", "Por favor, escreva um relato mais detalhado.")
            
            gui.logica_concluir_resgate_direto(ocorrencia, relato, total)

        tk.Button(card, text="CONCLUIR E LIBERAR EQUIPE", bg=SUCCESS, fg="white", 
                font=("Segoe UI", 10, "bold"), command=confirmar, pady=10, cursor="hand2").pack(fill=tk.X, pady=10)
        
        tk.Button(container, text="Voltar", command=lambda: AgenteScreen.render_painel_operacional(gui, container),
                  relief=tk.FLAT).pack(pady=10)
