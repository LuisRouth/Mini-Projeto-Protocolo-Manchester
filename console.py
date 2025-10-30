import os
from sistema import SistemaTriagem
from paciente import Paciente

class ConsoleInterface:
    def __init__(self):
        self.sistema = SistemaTriagem()

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def run(self):
        while True:
            self.limpar_tela()
            print("=== SISTEMA DE TRIAGEM (TERMINAL) ===")
            print("1 - Cadastrar paciente")
            print("2 - Chamar paciente")
            print("3 - Mostrar status das filas")
            print("4 - Ver log de atendimentos")
            print("0 - Sair")
            escolha = input("Escolha: ")

            if escolha == '1':
                self.cadastrar_paciente()
            elif escolha == '2':
                self.chamar_paciente()
            elif escolha == '3':
                self.mostrar_status()
            elif escolha == '4':
                self.ver_log()
            elif escolha == '0':
                break

    def cadastrar_paciente(self):
        self.limpar_tela()
        print("--- Cadastro de Paciente ---")
        
        while True:
            nome = input("Nome do paciente: ").strip()
            if nome and not any(c.isdigit() for c in nome): break
            print("Erro: Nome inválido. Não pode ser vazio ou conter números.")
        print("\nSelecione a queixa principal do paciente:")
        for i, queixa in enumerate(self.sistema.lista_queixas):
            print(f"{i + 1} - {queixa}")
        
        while True:
            try:
                escolha = int(input("Escolha o número do fluxograma: ")) - 1
                if 0 <= escolha < len(self.sistema.lista_queixas):
                    queixa_escolhida = self.sistema.lista_queixas[escolha]
                    arvore_selecionada = self.sistema.arvores_triagem[queixa_escolhida]
                    break
                else:
                    print("Número inválido.")
            except ValueError:
                print("Por favor, digite um número.")

        # PASSO 2: PERCORRER A ÁRVORE SELECIONADA
        print("\n--- Iniciando Triagem ---")
        nodo_atual = arvore_selecionada
        while nodo_atual.sim:
            resposta = input(f"{nodo_atual.valor} (s/n): ").lower()
            if resposta == 's':
                nodo_atual = nodo_atual.sim
            elif resposta == 'n':
                nodo_atual = nodo_atual.nao
        
        cor = nodo_atual.valor
        self.sistema.adicionar_paciente_fila(Paciente(nome), cor)
        print(f"\nPaciente {nome} classificado como {cor} e adicionado à fila.")
        input("\nPressione Enter para continuar...")

    def chamar_paciente(self):
        self.limpar_tela()
        print("--- Chamada de Paciente ---")
        cor, paciente = self.sistema.chamar_proximo_paciente()
        if paciente:
            print(f"Chamando paciente da fila {cor}: {paciente}")
        else:
            print("Todas as filas estão vazias.")
        input("\nPressione Enter para continuar...")

    def mostrar_status(self):
        self.limpar_tela()
        print("--- Status Atual das Filas ---")
        print(self.sistema.get_status_filas())
        input("\nPressione Enter para continuar...")

    def ver_log(self):
        self.limpar_tela()
        print("--- Log de Atendimentos ---")
        print(self.sistema.get_log())
        input("\nPressione Enter para continuar...")