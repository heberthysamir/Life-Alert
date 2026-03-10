import os
import sys

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if pkg_root not in sys.path:
    sys.path.insert(0, pkg_root)

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