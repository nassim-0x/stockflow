import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import articles_db
import fournisseurs_db
import mouvements_db

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
def ouvrir_popup(numero=None):
    popup = tk.Toplevel(window)
    popup.title("Nouvelle réception")
    popup.geometry("950x760")

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
        values=fournisseurs_db.pour_reception(),
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
        values=articles_db.pour_reception(),
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

    # les lignes de la réception : référence -> [quantité, prix]
    lignes = {}

    def afficher_lignes():
        for ligne in table_lignes.get_children():
            table_lignes.delete(ligne)
        total = 0
        for ref in lignes:
            quantite, prix = lignes[ref]
            nom = articles_db.article(ref)["ANAME"]
            table_lignes.insert("", "end", iid=ref, values=(ref, nom, quantite, "U", prix, quantite * prix))
            total = total + quantite * prix
        total_label.config(text=f"{total:.2f} DH")

    def article_choisi(event):
        """On propose le prix d'achat de la fiche article."""
        article = articles_db.article(article_combo.get().split(" - ")[0])
        if article is not None:
            ecrire(prix_entry, article["PRIX_ACHAT"])
            ecrire(unite_entry, "U")

    def ligne_choisie(event):
        """On clique sur une ligne : elle est recopiée dans les champs."""
        if table_lignes.selection():
            ref = table_lignes.selection()[0]
            article_combo.set(ref + " - " + articles_db.article(ref)["ANAME"])
            ecrire(quantite_entry, lignes[ref][0])
            ecrire(prix_entry, lignes[ref][1])

    def ajouter_ligne():
        """Ajoute la ligne, ou la remplace si l'article est déjà dans la réception."""
        ref = article_combo.get().split(" - ")[0].strip()
        if articles_db.article(ref) is None:
            messagebox.showwarning("Attention", "Choisissez un article de la liste.", parent=popup)
            return
        try:
            quantite = int(quantite_entry.get())
            prix = float(prix_entry.get())
        except ValueError:
            messagebox.showwarning("Attention", "Quantité et prix doivent être des nombres.", parent=popup)
            return
        if quantite <= 0 or prix < 0:
            messagebox.showwarning("Attention", "La quantité doit être positive.", parent=popup)
            return
        lignes[ref] = [quantite, prix]
        afficher_lignes()

    def supprimer_ligne():
        if not table_lignes.selection():
            messagebox.showwarning("Attention", "Choisissez une ligne.", parent=popup)
            return
        del lignes[table_lignes.selection()[0]]
        afficher_lignes()

    def enregistrer():
        numero = numero_entry.get()
        date = date_entry.get()
        fournisseur = fournisseur_combo.get()
        if date == "" or fournisseur == "" or len(lignes) == 0:
            messagebox.showwarning("Attention", "Il faut une date, un fournisseur et au moins une ligne.", parent=popup)
            return
        try:
            datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            messagebox.showwarning("Attention", "La date doit être au format JJ/MM/AAAA.", parent=popup)
            return

        # un article n'a qu'un seul fournisseur (association FOURNIR)
        code = fournisseur.split(" | ")[0]
        for ref in lignes:
            article = articles_db.article(ref)
            if article is None or article["FCODE"] not in (None, code):
                messagebox.showerror("Refusé", "L'article " + ref + " est fourni par un autre fournisseur.", parent=popup)
                return

        anciennes = {}
        if numero in receptions:
            anciennes = receptions[numero][2]
        ref = mouvements_db.stock_negatif(anciennes, lignes)
        if ref != "":
            messagebox.showerror("Refusé", "Le stock de " + ref + " a déjà été livré.", parent=popup)
            return

        mouvements_db.annuler_reception(anciennes)
        mouvements_db.receptionner(lignes, code)
        receptions[numero] = [date, fournisseur, dict(lignes)]
        afficher_receptions()
        popup.destroy()

    article_combo.bind("<<ComboboxSelected>>", article_choisi)
    table_lignes.bind("<<TreeviewSelect>>", ligne_choisie)

    # buttons to add, edit or delete a ligne in the table
    # they dont do anything yet, the functions will be added later
    lignes_buttons = ttk.Frame(popup)
    lignes_buttons.pack(fill="x", padx=15, pady=10)

    ttk.Button(
        lignes_buttons,
        text="Ajouter ligne",
        command=ajouter_ligne
    ).pack(side="left", padx=5)

    ttk.Button(
        lignes_buttons,
        text="Modifier ligne",
        command=ajouter_ligne
    ).pack(side="left", padx=5)

    ttk.Button(
        lignes_buttons,
        text="Supprimer ligne",
        command=supprimer_ligne
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
        text="Enregistrer",
        command=enregistrer
    )
    btn_save.pack(side="right", padx=5)

    # annuler button just close the popup
    btn_cancel = ttk.Button(
        bottom_frame,
        text="Annuler",
        command=popup.destroy
    )
    btn_cancel.pack(side="right", padx=5)

    if numero is None:
        numero = prochain_numero()
        ecrire(date_entry, datetime.now().strftime("%d/%m/%Y"))
    else:
        date, fournisseur, anciennes_lignes = receptions[numero]
        ecrire(date_entry, date)
        fournisseur_combo.set(fournisseur)
        fournisseur_combo.config(state="disabled")
        lignes.update(anciennes_lignes)
        popup.title("Modifier la réception " + numero)
    ecrire(numero_entry, numero)
    numero_entry.config(state="readonly")
    afficher_lignes()


# les réceptions : numéro -> [date, fournisseur, lignes]
# (avec 3 tables, la base garde seulement le stock, pas la liste des bons)
receptions = {}


def ecrire(champ, texte):
    champ.delete(0, "end")
    champ.insert(0, texte)


def prochain_numero():
    plus_grand = 0
    for numero in receptions:
        if int(numero[2:]) > plus_grand:
            plus_grand = int(numero[2:])
    return "BR" + str(plus_grand + 1).zfill(6)


def afficher_receptions():
    for ligne in table.get_children():
        table.delete(ligne)
    texte = search_entry.get().lower()
    for numero in sorted(receptions, reverse=True):
        date, fournisseur, lignes = receptions[numero]
        if texte in (numero + fournisseur).lower():
            total = 0
            for ref in lignes:
                total = total + lignes[ref][0] * lignes[ref][1]
            table.insert("", "end", iid=numero, values=(numero, date, fournisseur, len(lignes), f"{total:.2f}"))


def quand_on_tape(event):
    afficher_receptions()


def modifier_reception():
    if not table.selection():
        messagebox.showwarning("Attention", "Choisissez une réception.")
        return
    ouvrir_popup(table.selection()[0])


def double_clic(event):
    modifier_reception()


def supprimer_reception():
    if not table.selection():
        messagebox.showwarning("Attention", "Choisissez une réception.")
        return
    numero = table.selection()[0]
    lignes = receptions[numero][2]
    ref = mouvements_db.stock_negatif(lignes, {})
    if ref != "":
        messagebox.showerror("Refusé", "Le stock de " + ref + " a déjà été livré.")
        return
    if messagebox.askyesno("Confirmation", "Supprimer " + numero + " ?\nLes quantités seront retirées du stock."):
        mouvements_db.annuler_reception(lignes)
        del receptions[numero]
        afficher_receptions()


##############WINDOW DESIGN##########################

# frame for the buttons and the search bar at the top
buttons_frame = ttk.Frame(frame)
buttons_frame.pack(fill="x", pady=10)

# nouvelle reception open the popup when we click it
# modifier and supprimer dont have a function yet
btn_new = ttk.Button(buttons_frame, text="Nouvelle réception",    command=ouvrir_popup)
btn_new.pack(side="left", padx=5)

btn_edit = ttk.Button(buttons_frame, text="Modifier", command=modifier_reception)
btn_edit.pack(side="left", padx=5)

btn_delete = ttk.Button(buttons_frame, text="Supprimer", command=supprimer_reception)
btn_delete.pack(side="left", padx=5)

# search bar next to the buttons
search_label = ttk.Label(buttons_frame, text="Rechercher :")
search_label.pack(side="left", padx=10)

search_entry = ttk.Entry(buttons_frame, width=25)
search_entry.pack(side="left")
search_entry.bind("<KeyRelease>", quand_on_tape)


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

# les réceptions viennent maintenant de afficher_receptions
table.pack(fill="both", expand=True)
table.bind("<Double-1>", double_clic)
afficher_receptions()

# start the app
window.mainloop()
