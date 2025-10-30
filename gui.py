import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter.font import Font
from sistema import SistemaTriagem
from paciente import Paciente

class TriagemWindow(tk.Toplevel):
    def __init__(self, parent, sistema):
        super().__init__(parent)
        self.parent = parent
        self.sistema = sistema
        self.paciente = None
        self.arvore_selecionada = None
        self.nodo_atual = None
        
        self.title("Nova Triagem")
        self.geometry("400x350")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.style = ttk.Style(self)
        self.style.configure("TLabel", font=("Segoe UI", 10))
        self.style.configure("TButton", font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"))
        
        self.container = ttk.Frame(self, padding=15)
        self.container.pack(expand=True, fill=tk.BOTH)

        self.iniciar_etapa_nome()

    def _limpar_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def iniciar_etapa_nome(self):
        self._limpar_container()
        ttk.Label(self.container, text="Etapa 1: Identificação", style="Header.TLabel").pack(pady=(0, 10))
        
        ttk.Label(self.container, text="Nome do Paciente:").pack(anchor="w")
        self.entry_nome = ttk.Entry(self.container, font=("Segoe UI", 10))
        self.entry_nome.pack(fill=tk.X, pady=(0, 20))
        self.entry_nome.focus()
        
        ttk.Button(self.container, text="Próximo", command=self.validar_nome).pack()

    def validar_nome(self):
        nome = self.entry_nome.get().strip()
        if nome and not any(c.isdigit() for c in nome):
            self.paciente = Paciente(nome)
            self.iniciar_etapa_queixa()
        else:
            messagebox.showerror("Erro", "Nome inválido. Não pode ser vazio ou conter números.", parent=self)

    def iniciar_etapa_queixa(self):
        self._limpar_container()
        ttk.Label(self.container, text="Etapa 2: Queixa Principal", style="Header.TLabel").pack(pady=(0, 10))

        self.listbox_queixas = tk.Listbox(self.container, height=5, font=("Segoe UI", 10), relief=tk.GROOVE)
        for queixa in self.sistema.lista_queixas:
            self.listbox_queixas.insert(tk.END, queixa)
        self.listbox_queixas.pack(expand=True, fill=tk.BOTH, pady=(0, 20))
        
        ttk.Button(self.container, text="Iniciar Perguntas", command=self.selecionar_fluxograma).pack()
        
    def selecionar_fluxograma(self):
        selecionado = self.listbox_queixas.curselection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Por favor, selecione uma queixa principal.", parent=self)
            return
            
        queixa = self.listbox_queixas.get(selecionado[0])
        self.arvore_selecionada = self.sistema.arvores_triagem[queixa]
        self.nodo_atual = self.arvore_selecionada
        self.iniciar_etapa_perguntas()

    def iniciar_etapa_perguntas(self):
        self._limpar_container()
        if not self.nodo_atual.sim:
            cor_final = self.nodo_atual.valor
            self.sistema.adicionar_paciente_fila(self.paciente, cor_final)
            self.parent.atualizar_status_e_log(f"Paciente '{self.paciente.nome}' classificado como {cor_final}.")
            messagebox.showinfo("Triagem Finalizada", f"Paciente {self.paciente.nome} classificado como {cor_final}.", parent=self.parent)
            self.destroy()
            return

        ttk.Label(self.container, text="Etapa 3: Perguntas", style="Header.TLabel").pack(pady=(0, 20))
        
        pergunta_label = ttk.Label(self.container, text=self.nodo_atual.valor, wraplength=350, justify=tk.CENTER, font=("Segoe UI", 11))
        pergunta_label.pack(pady=(0, 30))

        botoes_frame = ttk.Frame(self.container)
        botoes_frame.pack()
        
        ttk.Button(botoes_frame, text="Sim", command=lambda: self.processar_resposta(True)).pack(side=tk.LEFT, padx=10)
        ttk.Button(botoes_frame, text="Não", command=lambda: self.processar_resposta(False)).pack(side=tk.LEFT, padx=10)

    def processar_resposta(self, resposta_sim):
        if resposta_sim:
            self.nodo_atual = self.nodo_atual.sim
        else:
            self.nodo_atual = self.nodo_atual.nao
        self.iniciar_etapa_perguntas()


class GuiApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.sistema = SistemaTriagem()
        
        self.title("Sistema de Triagem Manchester")
        self.geometry("800x500")
        
        self.style = ttk.Style(self)
        self.style.theme_use("vista")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", padding=6, relief="flat", font=("Segoe UI", 10))
        self.style.configure("Sidebar.TFrame", background="#e0e0e0")
        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), background="#f0f0f0")

        sidebar = ttk.Frame(self, width=200, style="Sidebar.TFrame")
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        main_frame = ttk.Frame(self, padding=20, style="TFrame")
        main_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        sidebar_content = ttk.Frame(sidebar, padding=20, style="Sidebar.TFrame")
        sidebar_content.pack(expand=True)
        
        ttk.Button(sidebar_content, text="Cadastrar Paciente", command=self.abrir_janela_triagem).pack(fill=tk.X, pady=8)
        ttk.Button(sidebar_content, text="Chamar Próximo", command=self.chamar_paciente).pack(fill=tk.X, pady=8)
        ttk.Button(sidebar_content, text="Atualizar Status", command=lambda: self.atualizar_status_e_log()).pack(fill=tk.X, pady=8)
        ttk.Button(sidebar_content, text="Ver Log", command=self.ver_log).pack(fill=tk.X, pady=8)

        self.header_label = ttk.Label(main_frame, text="Status das Filas", style="Header.TLabel")
        self.header_label.pack(anchor="w", pady=(0, 10))
        
        self.texto_display = scrolledtext.ScrolledText(main_frame, state=tk.DISABLED, wrap=tk.WORD, height=20, width=50, font=("Consolas", 10))
        self.texto_display.pack(expand=True, fill=tk.BOTH)

        self.status_bar = ttk.Label(main_frame, text="Bem-vindo!", relief=tk.SUNKEN, anchor="w", padding=5)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.atualizar_status_e_log()

    def _escrever_no_display(self, texto):
        self.texto_display.config(state=tk.NORMAL)
        self.texto_display.delete('1.0', tk.END)
        self.texto_display.insert(tk.END, texto)
        self.texto_display.config(state=tk.DISABLED)

    def atualizar_status_e_log(self, status_message=None):
        self.header_label.config(text="Status das Filas")
        status_filas = self.sistema.get_status_filas()
        self._escrever_no_display(status_filas)
        if status_message:
            self.status_bar.config(text=status_message)

    def chamar_paciente(self):
        cor, paciente = self.sistema.chamar_proximo_paciente()
        if paciente:
            messagebox.showinfo("Chamando Paciente", f"Paciente da Fila {cor}:\n\n{paciente}")
            self.atualizar_status_e_log(f"Paciente '{paciente.nome}' chamado da fila {cor}.")
        else:
            messagebox.showinfo("Filas Vazias", "Não há pacientes para chamar.")
            self.status_bar.config(text="Tentativa de chamada: filas vazias.")
        
    def ver_log(self):
        self.header_label.config(text="Log de Atendimentos")
        log_data = self.sistema.get_log()
        self._escrever_no_display(log_data)
        self.status_bar.config(text="Exibindo log de atendimentos.")
        
    def abrir_janela_triagem(self):

        TriagemWindow(self, self.sistema)