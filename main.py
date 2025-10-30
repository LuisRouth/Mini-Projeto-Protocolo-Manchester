from console import ConsoleInterface
from gui import GuiApplication

def main():
    while True:
        print("\nEscolha a interface para o sistema:")
        print("1. Terminal (baseado em texto)")
        print("2. Interface Gráfica (GUI)")
        print("0. Sair")
        
        escolha = input("Digite sua escolha: ")

        if escolha == '1':
            app = ConsoleInterface()
            app.run()
            break
        elif escolha == '2':
            try:
                app = GuiApplication()
                app.mainloop()
            except Exception as e:
                print(f"Não foi possível iniciar a interface gráfica: {e}")
                print("Verifique se você está em um ambiente com suporte a janelas.")
            break
        elif escolha == '0':
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()