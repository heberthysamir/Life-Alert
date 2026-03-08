import tkinter as tk
from infrastructure.api.interface import LifeAlertGUI
from infrastructure.database.setup import create_tables


def main():
    print("Iniciando Life Alert...")
    # Criar tabelas no banco de dados
    create_tables()
    
    # Inicializar a interface
    root = tk.Tk()
    app = LifeAlertGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()