from database import executer, lire


def lister():
    return lire("select * from STOCK order by REF")


def article(ref):
    """La ligne de l'article dans la table STOCK, ou None s'il n'existe pas."""
    lignes = lire("select * from STOCK where REF = ?", (ref,))
    if len(lignes) == 0:
        return None
    return lignes[0]


def existe(ref):
    return article(ref) is not None


def ajouter(ref, nom, famille, prix_vente, prix_achat):
    # un nouvel article commence avec un stock à 0 et sans fournisseur
    return executer("insert into STOCK values (?, ?, ?, ?, ?, 0, 0, 0, null)",
                    (ref, nom, famille, prix_vente, prix_achat))


def modifier(ref, nom, famille, prix_vente, prix_achat):
    return executer("update STOCK set ANAME = ?, FAMILLE = ?, PRIX_VENTE = ?, PRIX_ACHAT = ? where REF = ?",
                    (nom, famille, prix_vente, prix_achat, ref))


def supprimer(ref):
    return executer("delete from STOCK where REF = ?", (ref,))


def pour_reception():
    """Liste pour la combobox des réceptions : 'REF - désignation'."""
    liste = []
    for article in lister():
        liste.append(article["REF"] + " - " + article["ANAME"])
    return liste


def pour_livraison():
    """Dictionnaire pour les livraisons : référence -> [désignation, prix de vente, stock]."""
    articles = {}
    for article in lister():
        articles[article["REF"]] = [article["ANAME"], article["PRIX_VENTE"], article["STOCK_REEL"]]
    return articles
