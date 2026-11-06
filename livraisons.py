import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import articles_db
import clients_db
import mouvements_db




# référence de l'article -> [désignation, prix de vente, stock]
articles = articles_db.pour_livraison()

clients = clients_db.pour_livraison()

# numéro du BL -> [date, client, lignes]
# lignes = { référence de l'article : [quantité, prix] }
# (avec 3 tables, la base garde seulement le stock, pas la liste des bons)
livraisons = {}

# Les lignes du BL ouvert dans la fenêtre de saisie
lignes_en_cours = {}

def argent(x):
    """58170 -> '58170.00' (toujours 2 chiffres après la virgule)"""
    return f"{x:.2f}"

def calculer_total(lignes):
    total = 0
    for ref in lignes:
        quantite, prix = lignes[ref]
        total = total + quantite * prix
    return total


def vider_tableau(t):
    for ligne in t.get_children():
        t.delete(ligne)


def ecrire(champ, texte):
    champ.delete(0, "end")
    champ.insert(0, texte)


def prochain_numero():
    """BL000004 -> BL000005"""
    plus_grand = 0
    for numero in livraisons:
        n = int(numero[2:])                      
        if n > plus_grand:
            plus_grand = n
    return "BL" + str(plus_grand + 1).zfill(6)    

def afficher_liste():
    vider_tableau(tableau)
    texte = e_recherche.get().lower()
    nombre = 0
    total_general = 0

    for numero in sorted(livraisons, reverse=True):      
        date, client, lignes = livraisons[numero]
        if texte in (numero + client).lower():
            total = calculer_total(lignes)
            tableau.insert("", "end", iid=numero,
                           values=(numero, date, client, len(lignes), argent(total)))
            nombre = nombre + 1
            total_general = total_general + total

    l_resume.config(text=str(nombre) + " pièce(s)    Total : " + argent(total_general))


def quand_on_tape(event):
    afficher_liste()


def nouvelle():
    ouvrir_saisie(prochain_numero(), "", "", {})


def modifier():
    if not tableau.selection():
        messagebox.showwarning("Attention", "Choisissez une livraison.")
        return
    numero = tableau.selection()[0]
    date, client, lignes = livraisons[numero]
    ouvrir_saisie(numero, date, client, lignes)


def double_clic(event):
    modifier()


def supprimer():
    if not tableau.selection():
        messagebox.showwarning("Attention", "Choisissez une livraison.")
        return
    numero = tableau.selection()[0]
    if messagebox.askyesno("Confirmation", "Supprimer " + numero + " ?\n"
                           "Les quantités seront remises en stock."):
        mouvements_db.annuler_livraison(livraisons[numero][2])
        del livraisons[numero]
        afficher_liste()

def ouvrir_saisie(numero, date, client, lignes):
    saisie.title("Livraison " + numero)

    # on relit les articles (stock à jour) et les clients dans la base
    articles.clear()
    articles.update(articles_db.pour_livraison())
    choix_articles.clear()
    for ref in articles:
        choix_articles.append(ref + " | " + articles[ref][0])
    c_article.config(values=choix_articles)
    c_client.config(values=clients_db.pour_livraison())

    e_numero.state(["!readonly"])        
    ecrire(e_numero, numero)
    e_numero.state(["readonly"])

    ecrire(e_date, date)
    c_client.set(client)

    lignes_en_cours.clear()             
    lignes_en_cours.update(lignes)      

    afficher_lignes()
    vider_ligne()
    saisie.deiconify()                   


def fermer_saisie():
    saisie.withdraw()                    


def afficher_lignes():
    vider_tableau(t_lignes)
    for ref in lignes_en_cours:
        quantite, prix = lignes_en_cours[ref]
        designation = articles[ref][0]
        t_lignes.insert("", "end", iid=ref,
                        values=(ref, designation, quantite, "U", argent(prix), argent(quantite * prix)))
    total = calculer_total(lignes_en_cours)
    l_total.config(text="Total : " + argent(total) + "   (" + str(len(lignes_en_cours)) + " ligne(s))")


def article_choisi(event):
    """On choisit un article : on propose son prix et on affiche son stock."""
    ref = c_article.get().split(" | ")[0]          
    ecrire(e_prix, articles[ref][1])
    l_stock.config(text="Stock actuel : " + str(articles[ref][2]) + " U")


def ligne_choisie(event):
    """On clique sur une ligne : on la recopie dans la zone Ligne."""
    if not t_lignes.selection():
        return
    ref = t_lignes.selection()[0]
    quantite, prix = lignes_en_cours[ref]
    c_article.set(ref + " | " + articles[ref][0])
    l_stock.config(text="Stock actuel : " + str(articles[ref][2]) + " U")
    ecrire(e_qte, quantite)
    ecrire(e_prix, prix)


def mettre_a_jour_ligne():
    """Ajoute la ligne, ou la remplace si l'article est déjà dans le BL."""
    if c_article.get() == "":
        messagebox.showwarning("Attention", "Choisissez un article.", parent=saisie)
        return
    try:
        quantite = int(e_qte.get())
        prix = float(e_prix.get())
    except ValueError:
        messagebox.showwarning("Attention", "Quantité et prix doivent être des nombres.", parent=saisie)
        return
    if quantite <= 0:
        messagebox.showwarning("Attention", "La quantité doit être positive.", parent=saisie)
        return

    ref = c_article.get().split(" | ")[0]
    lignes_en_cours[ref] = [quantite, prix]
    afficher_lignes()
    vider_ligne()


def retirer_ligne():
    if not t_lignes.selection():
        messagebox.showwarning("Attention", "Choisissez une ligne.", parent=saisie)
        return
    del lignes_en_cours[t_lignes.selection()[0]]
    afficher_lignes()
    vider_ligne()


def vider_ligne():
    c_article.set("")
    ecrire(e_qte, "")
    ecrire(e_prix, "")
    l_stock.config(text="")


def enregistrer():
    numero = e_numero.get()
    date = e_date.get()
    client = c_client.get()

    if date == "" or client == "" or len(lignes_en_cours) == 0:
        messagebox.showwarning("Attention", "Il faut une date, un client et au moins une ligne.",
                               parent=saisie)
        return
    try:
        datetime.strptime(date, "%d/%m/%Y")
    except ValueError:
        messagebox.showwarning("Attention", "La date doit être au format JJ/MM/AAAA.", parent=saisie)
        return

    
    problemes = ""
    for ref in lignes_en_cours:
        quantite = lignes_en_cours[ref][0]
        stock = articles[ref][2]
        if numero in livraisons and ref in livraisons[numero][2]:
            stock = stock + livraisons[numero][2][ref][0]   # ce que l'ancien BL avait déjà sorti
        if quantite > stock:
            problemes = problemes + "\n - " + ref + " : disponible " + str(stock) + ", demandé " + str(quantite)

    if problemes != "":
        messagebox.showerror("Livraison refusée", "Stock insuffisant :" + problemes, parent=saisie)
        return                                   

    if numero in livraisons:
        mouvements_db.annuler_livraison(livraisons[numero][2])
    mouvements_db.livrer(lignes_en_cours)
    livraisons[numero] = [date, client, dict(lignes_en_cours)]
    afficher_liste()
    fermer_saisie()


fenetre = tk.Tk()
fenetre.title("Gestion Stock - Livraisons")
fenetre.geometry("1000x450")


haut = ttk.Frame(fenetre)
haut.pack(fill="x", padx=10, pady=10)
ttk.Button(haut, text="Nouvelle livraison", command=nouvelle).pack(side="left")
ttk.Button(haut, text="Modifier", command=modifier).pack(side="left", padx=5)
ttk.Button(haut, text="Supprimer", command=supprimer).pack(side="left")
ttk.Label(haut, text="Rechercher :").pack(side="left", padx=(20, 5))
e_recherche = ttk.Entry(haut, width=30)
e_recherche.pack(side="left")
e_recherche.bind("<KeyRelease>", quand_on_tape)
l_resume = ttk.Label(haut)
l_resume.pack(side="right")

barre = ttk.Scrollbar(fenetre)
barre.pack(side="right", fill="y", padx=(0, 10), pady=(0, 10))

tableau = ttk.Treeview(fenetre, columns=("num", "date", "client", "lignes", "total"), show="headings")
tableau.heading("num", text="N° pièce")
tableau.heading("date", text="Date")
tableau.heading("client", text="Client")
tableau.heading("lignes", text="Lignes")
tableau.heading("total", text="Total")
tableau.column("lignes", width=60, anchor="e")      
tableau.column("total", anchor="e")
tableau.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(0, 10))
tableau.bind("<Double-1>", double_clic)

barre.config(command=tableau.yview)
tableau.config(yscrollcommand=barre.set)


saisie = tk.Toplevel(fenetre)
saisie.withdraw()                                   
saisie.protocol("WM_DELETE_WINDOW", fermer_saisie)  

entete = ttk.LabelFrame(saisie, text="Entête", padding=10)
entete.pack(fill="x", padx=10, pady=5)

ttk.Label(entete, text="N° pièce").grid(row=0, column=0, sticky="w")
e_numero = ttk.Entry(entete, width=15)
e_numero.grid(row=0, column=1, sticky="w")
e_numero.state(["readonly"])

ttk.Label(entete, text="Date (JJ/MM/AAAA)").grid(row=0, column=2, padx=(30, 5))
e_date = ttk.Entry(entete, width=12)
e_date.grid(row=0, column=3)

ttk.Label(entete, text="Client").grid(row=1, column=0, sticky="w", pady=5)
c_client = ttk.Combobox(entete, values=clients, state="readonly", width=45)
c_client.grid(row=1, column=1, columnspan=3, sticky="w")


t_lignes = ttk.Treeview(saisie, columns=("ref", "des", "qte", "unite", "prix", "montant"),
                        show="headings", height=8)
t_lignes.heading("ref", text="Référence")
t_lignes.heading("des", text="Désignation")
t_lignes.heading("qte", text="Quantité")
t_lignes.heading("unite", text="Unité")
t_lignes.heading("prix", text="Prix de vente")
t_lignes.heading("montant", text="Montant")
t_lignes.column("qte", width=70, anchor="e")
t_lignes.column("unite", width=50)
t_lignes.column("prix", width=110, anchor="e")
t_lignes.column("montant", width=110, anchor="e")
t_lignes.pack(fill="both", expand=True, padx=10, pady=5)
t_lignes.bind("<<TreeviewSelect>>", ligne_choisie)


zone = ttk.LabelFrame(saisie, text="Ligne", padding=10)
zone.pack(fill="x", padx=10, pady=5)

choix_articles = []
for ref in articles:
    choix_articles.append(ref + " | " + articles[ref][0])

ttk.Label(zone, text="Article").grid(row=0, column=0)
c_article = ttk.Combobox(zone, values=choix_articles, state="readonly", width=35)
c_article.grid(row=0, column=1, padx=5)
c_article.bind("<<ComboboxSelected>>", article_choisi)

ttk.Label(zone, text="Quantité").grid(row=0, column=2)
e_qte = ttk.Entry(zone, width=8)
e_qte.grid(row=0, column=3, padx=5)

ttk.Label(zone, text="Prix de vente").grid(row=0, column=4)
e_prix = ttk.Entry(zone, width=10)
e_prix.grid(row=0, column=5, padx=5)

l_stock = ttk.Label(zone)
l_stock.grid(row=1, column=1, sticky="w", pady=5)

ttk.Button(zone, text="Mettre à jour la ligne", command=mettre_a_jour_ligne).grid(row=1, column=3)
ttk.Button(zone, text="Retirer la ligne", command=retirer_ligne).grid(row=1, column=4)
ttk.Button(zone, text="Vider", command=vider_ligne).grid(row=1, column=5)


bas = ttk.Frame(saisie)
bas.pack(fill="x", padx=10, pady=10)
l_total = ttk.Label(bas, font=("Arial", 12, "bold"))
l_total.pack(side="left")
ttk.Button(bas, text="Annuler", command=fermer_saisie).pack(side="right")
ttk.Button(bas, text="Enregistrer", command=enregistrer).pack(side="right", padx=5)



afficher_liste()
fenetre.mainloop()
