import os
import sqlite3
from tkinter import messagebox

chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stockflow.db")
db = sqlite3.connect(chemin)
db.row_factory = sqlite3.Row

#Code pour la creation de la table avec les contraintes du mcd

def creer_tables():
    db.execute("""create table if not exists FOURNISSEUR (
                    FCODE text primary key,
                    FNAME text not null,
                    ADDRESSE text,
                    TELEPHONE text)""")
    db.execute("""create table if not exists CLIENT (
                    CODE_CLIENT text primary key,
                    CNAME text not null,
                    ADDRESSE text,
                    TELEPHONE text)""")
    db.execute("""create table if not exists STOCK (
                    REF text primary key,
                    ANAME text not null,
                    FAMILLE text,
                    PRIX_VENTE real,
                    PRIX_ACHAT real,
                    ENTRE integer,
                    SORTIE integer,
                    STOCK_REEL integer,
                    FCODE text references FOURNISSEUR(FCODE))""")
    db.commit()

#Code pour gestion d'erreur à chaque commande faite

def executer(requete, valeurs=()):
    """insert, update ou delete. Renvoie True si tout s'est bien passé."""
    try:
        db.execute(requete, valeurs)
        db.commit()
        return True
    except sqlite3.Error as erreur:
        messagebox.showerror("Erreur base de données", str(erreur))
        return False


def lire(requete, valeurs=()):
    """select. Renvoie la liste des lignes trouvées."""
    try:
        return db.execute(requete, valeurs).fetchall()
    except sqlite3.Error as erreur:
        messagebox.showerror("Erreur base de données", str(erreur))
        return []


creer_tables()
