from database import executer, lire


def lister():
    """Dictionnaire : code du client -> [raison sociale, adresse, téléphone]."""
    clients = {}
    for client in lire("select * from CLIENT"):
        clients[client["CODE_CLIENT"]] = [client["CNAME"], client["ADDRESSE"], client["TELEPHONE"]]
    return clients


def enregistrer(code, nom, adresse, tel):
    # le code existe déjà -> modification, sinon -> nouveau client
    if len(lire("select * from CLIENT where CODE_CLIENT = ?", (code,))) > 0:
        return executer("update CLIENT set CNAME = ?, ADDRESSE = ?, TELEPHONE = ? where CODE_CLIENT = ?",
                        (nom, adresse, tel, code))
    return executer("insert into CLIENT values (?, ?, ?, ?)", (code, nom, adresse, tel))


def supprimer(code):
    return executer("delete from CLIENT where CODE_CLIENT = ?", (code,))


def pour_livraison():
    """Liste pour la combobox des livraisons : 'C0001 | raison sociale'."""
    liste = []
    for client in lire("select * from CLIENT order by CODE_CLIENT"):
        liste.append(client["CODE_CLIENT"] + " | " + client["CNAME"])
    return liste
