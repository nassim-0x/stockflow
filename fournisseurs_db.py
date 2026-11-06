from tkinter import messagebox
from database import executer, lire


def lister():
    """Dictionnaire : code du fournisseur -> [raison sociale, adresse, téléphone]."""
    fournisseurs = {}
    for f in lire("select * from FOURNISSEUR"):
        fournisseurs[f["FCODE"]] = [f["FNAME"], f["ADDRESSE"], f["TELEPHONE"]]
    return fournisseurs


def avec_articles():
    """Les fournisseurs qui fournissent des articles (association FOURNIR)."""
    liste = []
    for ligne in lire("select distinct FCODE from STOCK where FCODE is not null"):
        liste.append(ligne["FCODE"])
    return liste


def enregistrer(code, nom, adresse, tel):
    if len(lire("select * from FOURNISSEUR where FCODE = ?", (code,))) > 0:
        return executer("update FOURNISSEUR set FNAME = ?, ADDRESSE = ?, TELEPHONE = ? where FCODE = ?",
                        (nom, adresse, tel, code))
    return executer("insert into FOURNISSEUR values (?, ?, ?, ?)", (code, nom, adresse, tel))


def supprimer(code):
    # on vérifie dans la base au moment de supprimer
    if code in avec_articles():
        messagebox.showerror("Refusé", "Le fournisseur " + code + " fournit des articles.")
        return False
    return executer("delete from FOURNISSEUR where FCODE = ?", (code,))


def pour_reception():
    """Liste pour la combobox des réceptions : 'F0001 | raison sociale'."""
    liste = []
    for f in lire("select * from FOURNISSEUR order by FCODE"):
        liste.append(f["FCODE"] + " | " + f["FNAME"])
    return liste
