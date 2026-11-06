import tkinter as tk
from tkinter import ttk, messagebox
import articles_db

# create the main window
window = tk.Tk()
window.title("Gestion Stock")
window.geometry("1100x650")

#############FUNCTIONS##########################

# when we click enregistrer we get the values from the inputs
# for now it just print, sql will be added later
def enregistrer_article():
    reference = ref_entry.get()
    designation = designation_entry.get()
    famille = famille_combo.get()

    reference = reference.strip().upper()
    if reference == "" or designation.strip() == "":
        messagebox.showwarning("Attention", "La référence et la désignation sont obligatoires.")
        return

    # convert the prices to float because entry give us string
    # if user type letters instead of numbers it show error
    try:
        prix_vente = float(vente_entry.get())
        prix_achat = float(achat_entry.get())
    except ValueError:
        messagebox.showerror(
            "Erreur",
            "expected float you typed string"
        )
        return

    if prix_vente < 0 or prix_achat < 0:
        messagebox.showwarning("Attention", "Les prix ne peuvent pas être négatifs.")
        return

    # la référence existe déjà -> modification, sinon -> nouvel article
    if articles_db.existe(reference):
        articles_db.modifier(reference, designation, famille, prix_vente, prix_achat)
    else:
        articles_db.ajouter(reference, designation, famille, prix_vente, prix_achat)
    charger_articles()


# delete button function, not finished yet
# my friend will do the sql part
def supprimer_article():
    if not articles_table.selection():
        messagebox.showwarning("Attention", "Choisissez un article.")
        return
    reference = articles_table.selection()[0]

    if int(articles_table.item(reference, "values")[5]) > 0:
        messagebox.showerror("Refusé", "L'article " + reference + " a des réceptions.")
        return
    if messagebox.askyesno("Confirmation", "Supprimer l'article " + reference + " ?"):
        articles_db.supprimer(reference)
        charger_articles()


# remplit le tableau avec les articles de la base
def charger_articles():
    global tous_les_articles
    for item_id in tous_les_articles:
        articles_table.delete(item_id)

    for article in articles_db.lister():
        couleur = ()
        if article["STOCK_REEL"] <= 0:
            couleur = ("rupture",)
        articles_table.insert("", "end", iid=article["REF"], tags=couleur, values=(
            article["REF"], article["ANAME"], article["FAMILLE"], article["PRIX_VENTE"],
            article["PRIX_ACHAT"], article["ENTRE"], article["SORTIE"], article["STOCK_REEL"]))

    tous_les_articles = list(articles_table.get_children())
    calculer_total_stock()


# when we click an article in the table
# it put the article informations in the right inputs
def afficher_selection(event):
    selected_items = articles_table.selection()

    if selected_items:
        # get the first selected row and its values
        item_id = selected_items[0]
        values = articles_table.item(item_id, "values")
        print(values)

        # delete old text first then insert the selected value
        ref_entry.delete(0, tk.END)
        ref_entry.insert(0, values[0])

        designation_entry.delete(0, tk.END)
        designation_entry.insert(0, values[1])

        famille_combo.set(values[2])

        vente_entry.delete(0, tk.END)
        vente_entry.insert(0, values[3])

        achat_entry.delete(0, tk.END)
        achat_entry.insert(0, values[4])


# nouveau button clear the inputs to write new article
def nouveau_article():
    ref_entry.delete(0, tk.END)
    designation_entry.delete(0, tk.END)
    famille_combo.current(0)
    unite_entry.delete(0, tk.END)
    vente_entry.delete(0, tk.END)
    achat_entry.delete(0, tk.END)


# calculate the total stock value from the articles in the table
# price achat * stock reel for each article
def calculer_total_stock():
    total = 0

    # get all the rows currently visible in the table
    for item_id in articles_table.get_children():
        values = articles_table.item(item_id, "values")

        # index 4 is prix achat and index 7 is stock reel
        prix_achat = float(values[4])
        stock_reel = int(values[7])

        total += prix_achat * stock_reel

    # update the label at the bottom
    total_label.config(
        text=f"Valeur totale du stock : {total:.2f} DH"
    )


# search article by reference or designation
# event because we use bind with keyboard
def rechercher_article(event):
    recherche = search_entry.get().lower().strip()

    # use the saved list because hidden rows are not in get_children
    for item_id in tous_les_articles:
        values = articles_table.item(item_id, "values")

        reference = values[0].lower()
        designation = values[1].lower()

        # if text match we show the row,else hide it
        if recherche in reference or recherche in designation:
            articles_table.reattach(item_id, "", "end")
        else:
            articles_table.detach(item_id)



##############WINDOW DESIGN##########################

# title of the page
title_label = ttk.Label(
    window,
    text="Articles / Stock",
    font=("Arial", 18)
)
title_label.pack(pady=20)


# total stock at bottom
# we pack it before the frames so it dont disappear
total_label = ttk.Label(
    window,
    text="Valeur totale du stock : 0 DH",
    font=("Arial", 12, "bold")
)
total_label.pack(side="bottom", pady=10)


# right frame for the article informations
right_frame = ttk.LabelFrame(
    window,
    text="Fiche article"
)
right_frame.pack(side="right", padx=10, pady=10, fill="y")


# reference input
ref_label = ttk.Label(right_frame, text="Référence")
ref_label.pack(pady=3)

ref_entry = ttk.Entry(right_frame)
ref_entry.pack(pady=3)


# designation input
designation_label = ttk.Label(right_frame, text="Désignation")
designation_label.pack(pady=5)

designation_entry = ttk.Entry(right_frame)
designation_entry.pack(pady=5)


# famille is a combobox so user can select from list
famille_label = ttk.Label(right_frame, text="Famille")
famille_label.pack(pady=5)

famille_combo = ttk.Combobox(
    right_frame,
    values=["Télévision", "Informatique", "Électroménager"],
)
famille_combo.pack(pady=5)

# select the first famille by default
famille_combo.current(0)


# prix de vente
vente_label = ttk.Label(right_frame, text="Prix de vente")
vente_label.pack(pady=5)

vente_entry = ttk.Entry(right_frame)
vente_entry.pack(pady=5)


# prix d'achat
achat_label = ttk.Label(right_frame, text="Prix d'achat")
achat_label.pack(pady=5)

achat_entry = ttk.Entry(right_frame)
achat_entry.pack(pady=5)


# unite input
unite_label = ttk.Label(right_frame, text="Stock minimal")
unite_label.pack(pady=5)

unite_entry = ttk.Entry(right_frame)
unite_entry.pack(pady=5)


# left frame contain the list of articles
left_frame = ttk.LabelFrame(
    window,
    text="Liste des articles"
)
left_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


# search bar at top of the table
search_label = ttk.Label(
    left_frame,
    text="Rechercher :"
)
search_label.pack(anchor="w", padx=10, pady=5)

search_entry = ttk.Entry(left_frame)
search_entry.pack(fill="x", padx=10, pady=5)

# every time we type it call rechercher_article
search_entry.bind("<KeyRelease>", rechercher_article)


##############BUTTONS##########################

# buttons are in the right frame
# command call the function when we click it
new_button = ttk.Button(
    right_frame,
    text="Nouveau",
    command=nouveau_article
)
new_button.pack(pady=3)

save_button = ttk.Button(
    right_frame,
    text="Enregistrer",
    command=enregistrer_article
)
save_button.pack(pady=3)

delete_button = ttk.Button(
    right_frame,
    text="Supprimer",
    command=supprimer_article
)
delete_button.pack(pady=3)


##############ARTICLES TABL##########################

# treeview is the table, we put all the column names here
# headings remove the empty first column
articles_table = ttk.Treeview(
    left_frame,
    columns=(
        "ref",
        "designation",
        "famille",
        "vente",
        "achat",
        "entree",
        "sortie",
        "stock_reel"
    ),
    show="headings"
)

# rupture tag make the row text red when we apply it
articles_table.tag_configure("rupture", foreground="red")


# vertical scrollbar for many articles
scrollbar = ttk.Scrollbar(
    left_frame,
    orient="vertical"
)
scrollbar.pack(side="right", fill="y")


# horizontal scrollbar because we have 8 columns
horizontal_scrollbar = ttk.Scrollbar(
    left_frame,
    orient="horizontal"
)
horizontal_scrollbar.pack(side="bottom", fill="x")

articles_table.pack(
    fill="both",
    expand=True
)


# names displayed at the top of each column
articles_table.heading("ref", text="REF")
articles_table.heading("designation", text="DÉSIGNATION")
articles_table.heading("famille", text="FAMILLE")
articles_table.heading("vente", text="PRIX VENTE")
articles_table.heading("achat", text="PRIX ACHAT")
articles_table.heading("entree", text="ENTRÉE")
articles_table.heading("sortie", text="SORTIE")
articles_table.heading("stock_reel", text="STOCK RÉEL")


# width and alignment for each column
# w = left, e = right, center = middle
articles_table.column("ref", width=100, anchor="w", stretch=False)
articles_table.column("designation", width=250, stretch=True)
articles_table.column("famille", width=150, stretch=False)
articles_table.column("vente", width=100, anchor="e")
articles_table.column("achat", width=100, anchor="e")
articles_table.column("entree", width=80, anchor="center")
articles_table.column("sortie", width=80, anchor="center")
articles_table.column("stock_reel", width=100, anchor="center")


# connect the scrollbars with the table
# yview is vertical and xview horizontal
scrollbar.config(command=articles_table.yview)
articles_table.configure(yscrollcommand=scrollbar.set)

horizontal_scrollbar.config(command=articles_table.xview)
articles_table.configure(xscrollcommand=horizontal_scrollbar.set)


#############TEST DATA#################

# les articles viennent maintenant de la base (voir charger_articles)


# save all row ids so search can hide and show them again
tous_les_articles = list(articles_table.get_children())


# when selecting a row call afficher_selection
articles_table.bind(
    "<<TreeviewSelect>>",
    afficher_selection
)


# calculate the total once after inserting the test articles
charger_articles()


window.mainloop()