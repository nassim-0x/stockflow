import tkinter as tk
from tkinter import ttk

# create the main window
window = tk.Tk()
window.title("Gestion Stock - Réceptions")
window.geometry("1100x650")

# main frame, everything of the page go inside it
frame = ttk.Frame(window, padding=10)
frame.pack(fill="both", expand=True)

# title of the page
title = ttk.Label(
    frame,
    text="Réceptions",
    font=("Arial", 16, "bold")
)
title.pack(pady=10)


#############FUNCTIONS##########################

# when we click nouvelle reception it open a new window (popup)
# to write the informations of the new reception
def ouvrir_popup():
    popup = tk.Toplevel(window)
    popup.title("Nouvelle réception")
    popup.geometry("950x650")

    # entete part, the main infos of the reception
    entete = ttk.LabelFrame(popup, text="Entête", padding=15)
    entete.pack(fill="x", padx=15, pady=15)

    # numero de piece input
    # we use grid here because its easier to put things side by side
    ttk.Label(entete, text="N° pièce").grid(
        row=0, column=0, padx=10, pady=10
    )

    numero_entry = ttk.Entry(entete, width=20)
    numero_entry.grid(row=0, column=1, padx=10, pady=10)

    # date input, for now user write it by hand
    ttk.Label(entete, text="Date (JJ/MM/AAAA)").grid(
        row=0, column=2, padx=10, pady=10
    )

    date_entry = ttk.Entry(entete, width=20)
    date_entry.grid(row=0, column=3, padx=10, pady=10)

    # fournisseur is a combobox so user choose from the list
    ttk.Label(entete, text="Fournisseur").grid(
        row=1, column=0, padx=10, pady=10
    )

    # readonly so the user cant write a fournisseur that dont exist
    # the list is just for testing, later it will come from the database
    fournisseur_combo = ttk.Combobox(
        entete,
        values=[
            "F0001 | Distrib Électro Maroc",
            "F0002 | Froid Industrie SA",
            "F0003 | TechnoVision Import"
        ],
        width=45,
        state="readonly"
    )

    # columnspan so the combobox take the place of 3 columns
    fournisseur_combo.grid(
        row=1, column=1, columnspan=3,
        padx=10, pady=10, sticky="w"
    )

    # lignes de reception part, the articles we received
    lignes_frame = ttk.LabelFrame(
        popup,
        text="Lignes de réception",
        padding=10
    )
    lignes_frame.pack(fill="both", expand=True, padx=15, pady=10)

    # names of the columns of the lignes table
    columns_lignes = (
        "reference",
        "designation",
        "quantite",
        "unite",
        "prix",
        "montant"
    )

    # treeview is the table
    # headings remove the empty first column
    table_lignes = ttk.Treeview(
        lignes_frame,
        columns=columns_lignes,
        show="headings",
        height=8
    )

    # names displayed at the top of each column
    table_lignes.heading("reference", text="Référence")
    table_lignes.heading("designation", text="Désignation")
    table_lignes.heading("quantite", text="Quantité")
    table_lignes.heading("unite", text="Unité")
    table_lignes.heading("prix", text="Prix d'achat")
    table_lignes.heading("montant", text="Montant")

    # width and alignment for each column
    # e = right, center = middle
    table_lignes.column("reference", width=110)
    table_lignes.column("designation", width=250)
    table_lignes.column("quantite", width=90, anchor="center")
    table_lignes.column("unite", width=80, anchor="center")
    table_lignes.column("prix", width=120, anchor="e")
    table_lignes.column("montant", width=120, anchor="e")

    table_lignes.pack(fill="both", expand=True)

    # 2 test lignes just to see how the table look
    # montant = quantite * prix
    table_lignes.insert("", "end", values=(
        "ART001", "Réfrigérateur Samsung", 2, "U", "4500.00", "9000.00"
    ))

    table_lignes.insert("", "end", values=(
        "ART002", "Télévision LG", 3, "U", "3200.00", "9600.00"
    ))

    # here we choose the article and write its quantity and price
    article_frame = ttk.LabelFrame(
        popup,
        text="Détails de l'article",
        padding=10
    )
    article_frame.pack(fill="x", padx=15, pady=10)

    # article combobox, test list for now
    ttk.Label(article_frame, text="Article").grid(
        row=0, column=0, padx=5, pady=5
    )

    article_combo = ttk.Combobox(
        article_frame,
        values=[
            "ART001 - Réfrigérateur Samsung",
            "ART002 - Télévision LG",
            "ART003 - Machine à laver"
        ],
        width=35
    )
    article_combo.grid(row=0, column=1, padx=5, pady=5)

    # quantite input
    ttk.Label(article_frame, text="Quantité").grid(
        row=0, column=2, padx=5, pady=5
    )

    quantite_entry = ttk.Entry(article_frame, width=10)
    quantite_entry.grid(row=0, column=3, padx=5, pady=5)

    # unite input
    ttk.Label(article_frame, text="Unité").grid(
        row=1, column=0, padx=5, pady=5
    )

    unite_entry = ttk.Entry(article_frame, width=15)
    unite_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # prix d'achat input
    ttk.Label(article_frame, text="Prix d'achat").grid(
        row=1, column=2, padx=5, pady=5
    )

    prix_entry = ttk.Entry(article_frame, width=15)
    prix_entry.grid(row=1, column=3, padx=5, pady=5)

    # buttons to add, edit or delete a ligne in the table
    # they dont do anything yet, the functions will be added later
    lignes_buttons = ttk.Frame(popup)
    lignes_buttons.pack(fill="x", padx=15, pady=10)

    ttk.Button(
        lignes_buttons,
        text="Ajouter ligne"
    ).pack(side="left", padx=5)

    ttk.Button(
        lignes_buttons,
        text="Modifier ligne"
    ).pack(side="left", padx=5)

    ttk.Button(
        lignes_buttons,
        text="Supprimer ligne"
    ).pack(side="left", padx=5)

    # total of all the lignes, it stay 0 for now
    # we will calculate it when the buttons work
    total_frame = ttk.Frame(popup)
    total_frame.pack(fill="x", padx=20, pady=10)

    ttk.Label(
        total_frame,
        text="Total général :",
        font=("Arial", 12, "bold")
    ).pack(side="left")

    total_label = ttk.Label(
        total_frame,
        text="0.00 DH",
        font=("Arial", 12, "bold")
    )
    total_label.pack(side="left", padx=10)

    # buttons at the bottom of the popup
    bottom_frame = ttk.Frame(popup)
    bottom_frame.pack(fill="x", padx=20, pady=15)

    # enregistrer button, the save part will be added with the database
    btn_save = ttk.Button(
        bottom_frame,
        text="Enregistrer"
    )
    btn_save.pack(side="right", padx=5)

    # annuler button just close the popup
    btn_cancel = ttk.Button(
        bottom_frame,
        text="Annuler",
        command=popup.destroy
    )
    btn_cancel.pack(side="right", padx=5)


##############WINDOW DESIGN##########################

# frame for the buttons and the search bar at the top
buttons_frame = ttk.Frame(frame)
buttons_frame.pack(fill="x", pady=10)

# nouvelle reception open the popup when we click it
# modifier and supprimer dont have a function yet
btn_new = ttk.Button(buttons_frame, text="Nouvelle réception",    command=ouvrir_popup)
btn_new.pack(side="left", padx=5)

btn_edit = ttk.Button(buttons_frame, text="Modifier")
btn_edit.pack(side="left", padx=5)

btn_delete = ttk.Button(buttons_frame, text="Supprimer")
btn_delete.pack(side="left", padx=5)

# search bar next to the buttons
search_label = ttk.Label(buttons_frame, text="Rechercher :")
search_label.pack(side="left", padx=10)

search_entry = ttk.Entry(buttons_frame, width=25)
search_entry.pack(side="left")


##############RECEPTIONS TABLE##########################

# names of the columns of the receptions table
columns = ("numero", "date", "fournisseur", "lignes", "total")

table = ttk.Treeview(
    frame,
    columns=columns,
    show="headings"
)

# names displayed at the top of each column
table.heading("numero", text="N° pièce")
table.heading("date", text="Date")
table.heading("fournisseur", text="Fournisseur")
table.heading("lignes", text="Lignes")
table.heading("total", text="Total")

# width of each column
table.column("numero", width=130)
table.column("date", width=120)
table.column("fournisseur", width=350)
table.column("lignes", width=80, anchor="center")
table.column("total", width=130, anchor="e")


#############TEST DATA#################

# 3 fake receptions just for testing the table
table.insert("", "end", values=(
    "BR000003", "06/10/2026",
    "F0001 - Distrib Électro Maroc", 4, "84 000,00"
))

table.insert("", "end", values=(
    "BR000002", "03/10/2026",
    "F0002 - Froid Industrie SA", 2, "81 600,00"
))

table.insert("", "end", values=(
    "BR000001", "01/10/2026",
    "F0003 - TechnoVision Import", 4, "167 350,00"
))

table.pack(fill="both", expand=True)

# start the app
window.mainloop()
