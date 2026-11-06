import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk

dossier = os.path.dirname(os.path.abspath(__file__))


def ouvrir(fichier):
    """Lance la fenêtre d'un camarade comme un programme à part."""
    subprocess.Popen([sys.executable, fichier], cwd=dossier)


fenetre = tk.Tk()
fenetre.title("Stockflow")
fenetre.geometry("350x380")

ttk.Label(fenetre, text="Gestion Stock", font=("Arial", 18)).pack(pady=20)
ttk.Button(fenetre, text="Articles / Stock", width=30, command=lambda: ouvrir("articles.py")).pack(pady=5)
ttk.Button(fenetre, text="Clients", width=30, command=lambda: ouvrir("clients.py")).pack(pady=5)
ttk.Button(fenetre, text="Fournisseurs", width=30, command=lambda: ouvrir("fournisseurs.py")).pack(pady=5)
ttk.Button(fenetre, text="Réceptions", width=30, command=lambda: ouvrir("reception.py")).pack(pady=5)
ttk.Button(fenetre, text="Livraisons", width=30, command=lambda: ouvrir("livraisons.py")).pack(pady=5)
ttk.Button(fenetre, text="Quitter", width=30, command=fenetre.destroy).pack(pady=20)

fenetre.mainloop()
