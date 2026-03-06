import tkinter as tk
from infrastructure.api.interface import LifeAlertGUI

def main():
    db = {
        "usuarios": [],
        "ocorrencias": [],
        "atendimentos": [],
        "equipes": [],
        "alertas": [],
        "vitimas": []
    }

    root = tk.Tk()
    app = LifeAlertGUI(root, db)
    root.mainloop()

if __name__ == "__main__":
    main()