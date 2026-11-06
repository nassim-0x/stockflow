import articles_db
from database import executer

# lignes = { référence de l'article : [quantité, prix] }


def receptionner(lignes, fournisseur):
    """Réception : les quantités entrent en stock, le prix d'achat et le fournisseur sont mis à jour."""
    for ref in lignes:
        quantite, prix = lignes[ref]
        executer("update STOCK set ENTRE = ENTRE + ?, STOCK_REEL = STOCK_REEL + ?, PRIX_ACHAT = ?, FCODE = ? where REF = ?",
                 (quantite, quantite, prix, fournisseur, ref))


def annuler_reception(lignes):
    for ref in lignes:
        quantite = lignes[ref][0]
        executer("update STOCK set ENTRE = ENTRE - ?, STOCK_REEL = STOCK_REEL - ? where REF = ?",
                 (quantite, quantite, ref))


def livrer(lignes):
    """Livraison : les quantités sortent du stock."""
    for ref in lignes:
        quantite = lignes[ref][0]
        executer("update STOCK set SORTIE = SORTIE + ?, STOCK_REEL = STOCK_REEL - ? where REF = ?",
                 (quantite, quantite, ref))


def annuler_livraison(lignes):
    for ref in lignes:
        quantite = lignes[ref][0]
        executer("update STOCK set SORTIE = SORTIE - ?, STOCK_REEL = STOCK_REEL + ? where REF = ?",
                 (quantite, quantite, ref))


def stock_negatif(anciennes, nouvelles):
    """Si on remplace une réception par une autre, est-ce qu'un stock devient négatif ?
    Renvoie la référence de l'article qui pose problème, sinon ''."""
    for ref in anciennes:
        article = articles_db.article(ref)
        if article is None:
            continue
        reste = article["STOCK_REEL"] - anciennes[ref][0]
        if ref in nouvelles:
            reste = reste + nouvelles[ref][0]
        if reste < 0:
            return ref
    return ""
