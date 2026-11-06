import tkinter as tk
from tkinter import ttk, messagebox


# ============ 1) LES DONNÉES (plus tard : la base de Reda) ============

# code du client -> [raison sociale, adresse, téléphone]
clients = {
    "C0001": ["Maison du Confort SARL", "12, bd de la Résistance - Casablanca", "05 22 40 11 20"],
    "C0002": ["Résidence Les Palmiers", "Route d'Azemmour - Casablanca", "05 22 39 87 45"],
    "C0003": ["Café-Restaurant Le Central", "45, av. Hassan II - Rabat", "05 37 70 25 61"],
    "C0004": ["Clinique Al Amal", "8, rue Ibn Sina - Mohammedia", "05 23 31 44 09"],
    "C0005": ["Hôtel Oasis Marrakech", "Zone hôtelière - Marrakech", "05 24 43 18 77"],
}

# Ces clients ont des livraisons : on n'a pas le droit de les supprimer
clients_avec_livraisons = ["C0001", "C0003"]


# ============ 2) PETITS OUTILS ============

def ecrire(champ, texte):
    """Remplace le texte d'un champ de saisie."""
    champ.delete(0, "end")
    champ.insert(0, texte)


def ecrire_code(texte):
    """Le champ Code est grisé : on le débloque, on écrit, on le rebloque."""
    e_code.state(["!readonly"])
    ecrire(e_code, texte)
    e_code.state(["readonly"])


def prochain_code():
    """Cherche le plus grand code et ajoute 1 : C0005 -> C0006."""
    plus_grand = 0
    for code in clients:
        numero = int(code[1:])            # "C0005" -> 5
        if numero > plus_grand:
            plus_grand = numero
    return "C" + str(plus_grand + 1).zfill(4)   # 6 -> "0006" -> "C0006"


# ============ 3) LES ACTIONS ============

def afficher():
    """Vide le tableau puis le remplit avec les clients qui correspondent à la recherche."""
    for ligne in tableau.get_children():
        tableau.delete(ligne)

    texte = e_recherche.get().lower()
    nombre = 0
    for code in sorted(clients):
        nom, adresse, tel = clients[code]
        if texte in (code + nom + adresse).lower():
            tableau.insert("", "end", iid=code, values=(code, nom, adresse, tel))
            nombre = nombre + 1

    l_compteur.config(text=str(nombre) + " élément(s)")


def quand_on_tape(event):
    afficher()


def ligne_choisie(event):
    """On clique sur un client : on recopie ses informations dans la fiche."""
    if not tableau.selection():
        return
    code = tableau.selection()[0]
    nom, adresse, tel = clients[code]

    ecrire_code(code)
    ecrire(e_nom, nom)
    ecrire(e_adresse, adresse)
    ecrire(e_tel, tel)
    l_mode.config(text="Modification : " + code)


def nouveau():
    """Fiche vide + nouveau code proposé."""
    tableau.selection_remove(tableau.selection())
    ecrire_code(prochain_code())
    ecrire(e_nom, "")
    ecrire(e_adresse, "")
    ecrire(e_tel, "")
    l_mode.config(text="Nouveau client")


def enregistrer():
    code = e_code.get()
    nom = e_nom.get().strip()
    adresse = e_adresse.get().strip()
    tel = e_tel.get().strip()

    # Contrôle 1 : la raison sociale est obligatoire
    if nom == "":
        messagebox.showwarning("Attention", "La raison sociale est obligatoire.")
        return

    # Contrôle 2 : si le téléphone est rempli, il faut 10 chiffres
    chiffres = tel.replace(" ", "")
    if tel != "" and (len(chiffres) != 10 or not chiffres.isdigit()):
        messagebox.showwarning("Attention", "Le téléphone doit avoir 10 chiffres.")
        return

    # Ajoute le client s'il est nouveau, le remplace s'il existe déjà
    clients[code] = [nom, adresse, tel]
    afficher()
    if tableau.exists(code):
        tableau.selection_set(code)       # resélectionne la ligne enregistrée


def supprimer():
    if not tableau.selection():
        messagebox.showwarning("Attention", "Choisissez un client.")
        return
    code = tableau.selection()[0]

    if not messagebox.askyesno("Confirmation", "Supprimer le client " + code + " ?"):
        return

    if code in clients_avec_livraisons:
        messagebox.showerror("Refusé", "Le client " + code + " a des livraisons.")
        return

    del clients[code]
    afficher()
    nouveau()


# ============ 4) LA FENÊTRE ============

fenetre = tk.Tk()
fenetre.title("Gestion Stock - Clients")
fenetre.geometry("1050x450")

# --- Barre d'état (tout en bas) ---
ttk.Label(fenetre, text="Connecté à la base commerce", relief="sunken").pack(side="bottom", fill="x")

# --- Zone du haut : recherche + compteur ---
haut = ttk.Frame(fenetre)
haut.pack(fill="x", padx=10, pady=10)

ttk.Label(haut, text="Rechercher :").pack(side="left")
e_recherche = ttk.Entry(haut, width=40)
e_recherche.pack(side="left", padx=5)
e_recherche.bind("<KeyRelease>", quand_on_tape)

l_compteur = ttk.Label(haut)
l_compteur.pack(side="right")

# --- Fiche client (à droite) ---
fiche = ttk.LabelFrame(fenetre, text="Fiche client", padding=10)
fiche.pack(side="right", fill="y", padx=10, pady=(0, 10))

ttk.Label(fiche, text="Code client *").grid(row=0, column=0, sticky="w", pady=4)
e_code = ttk.Entry(fiche, width=30)
e_code.grid(row=0, column=1)
e_code.state(["readonly"])

ttk.Label(fiche, text="Raison sociale *").grid(row=1, column=0, sticky="w", pady=4)
e_nom = ttk.Entry(fiche, width=30)
e_nom.grid(row=1, column=1)

ttk.Label(fiche, text="Adresse").grid(row=2, column=0, sticky="w", pady=4)
e_adresse = ttk.Entry(fiche, width=30)
e_adresse.grid(row=2, column=1)

ttk.Label(fiche, text="Téléphone").grid(row=3, column=0, sticky="w", pady=4)
e_tel = ttk.Entry(fiche, width=30)
e_tel.grid(row=3, column=1)

ttk.Button(fiche, text="Nouveau", command=nouveau).grid(row=4, column=0, pady=10)
ttk.Button(fiche, text="Enregistrer", command=enregistrer).grid(row=4, column=1, sticky="w")
ttk.Button(fiche, text="Supprimer", command=supprimer).grid(row=4, column=1, sticky="e")

l_mode = ttk.Label(fiche)
l_mode.grid(row=5, column=0, columnspan=2, sticky="w")

# --- Tableau des clients (à gauche) + barre de défilement ---
barre = ttk.Scrollbar(fenetre)
barre.pack(side="right", fill="y", pady=(0, 10))

tableau = ttk.Treeview(fenetre, columns=("code", "nom", "adresse", "tel"), show="headings")
tableau.heading("code", text="Code client")
tableau.heading("nom", text="Raison sociale")
tableau.heading("adresse", text="Adresse")
tableau.heading("tel", text="Téléphone")
tableau.column("code", width=90)
tableau.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(0, 10))
tableau.bind("<<TreeviewSelect>>", ligne_choisie)

barre.config(command=tableau.yview)       # la barre fait défiler le tableau
tableau.config(yscrollcommand=barre.set)  # le tableau fait bouger la barre

# --- Démarrage ---
afficher()
nouveau()
fenetre.mainloop()
