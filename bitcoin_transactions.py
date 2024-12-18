import requests
import pandas as pd
import time

def recuperer_transactions_adresse(address):
    """
    Recupere toutes les transactions associes a une adresse Bitcoin via l'API Blockchain.info

    Retourne:
    Une liste de transactions lies directement a l'adresse choisie
    """
    url = f"https://blockchain.info/rawaddr/{address}?format=json"
    try:
        print(f"Recuperation des transactions pour l'adresse : {address}")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        transactions = []
        for tx in data.get("txs", []):
            tx_hash = tx.get("hash")
            heure = tx.get("time")

            # Filtrer les entres et sorties liees uniquement a l'adresse choisie
            entrees = [
                {"Adresse": inp['prev_out'].get('addr', 'N/A'), "Valeur (BTC)": inp['prev_out'].get('value', 0) / 1e8}
                for inp in tx.get("inputs", []) if 'prev_out' in inp and inp['prev_out'].get('addr') == address
            ]
            sorties = [
                {"Adresse": out.get('addr', 'N/A'), "Valeur (BTC)": out.get('value', 0) / 1e8}
                for out in tx.get("out", []) if out.get('addr') == address
            ]

            # Ajouter la transaction uniquement si l'adresse choisie est impliquée
            if entrees or sorties:
                frais = tx.get("fee", 0) / 1e8
                transactions.append({
                    "Hachage": tx_hash,
                    "Heure": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(heure)) if heure else "N/A",
                    "Entrées": entrees,
                    "Sorties": sorties,
                    "Frais (BTC)": frais
                })

        return transactions

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la recuperation des transactions pour l'adresse {address} : {e}")
        return []

def main():
    """
    Programme principal pour recuperer les transactions associees à une adresse Bitcoin.
    """
    print("Debut de l'execution du programme")

    # Étape 1 : Demander l'adresse Bitcoin
    address = input("Entrez une adresse Bitcoin : ")

    # Étape 2 : Recuperer les transactions associes
    transactions = recuperer_transactions_adresse(address)
    if not transactions:
        print("Aucune transaction trouve ou une erreur s'est produite")
        return

    print(f"{len(transactions)} transactions recupere pour l'adresse {address}")

    # Étape 3 : Afficher et sauvegarder les resultats
    resultats = []
    for tx in transactions:
        for entree in tx["Entrées"]:
            resultats.append({
                "Hachage": tx["Hachage"],
                "Heure": tx["Heure"],
                "Type": "Entrée",
                "Adresse": entree["Adresse"],
                "Valeur (BTC)": entree["Valeur (BTC)"]
            })
        for sortie in tx["Sorties"]:
            resultats.append({
                "Hachage": tx["Hachage"],
                "Heure": tx["Heure"],
                "Type": "Sortie",
                "Adresse": sortie["Adresse"],
                "Valeur (BTC)": sortie["Valeur (BTC)"]
            })

    df = pd.DataFrame(resultats)
    print("\nTransactions associes à l'adresse Bitcoin :")
    print(df)

    # Sauvegarde dans un fichier CSV
    fichier_csv = f"transactions.csv"
    df.to_csv(fichier_csv, index=False)
    print(f"Les resultats ont ete sauvegardes dans '{fichier_csv}'")

if __name__ == "__main__":
    main()
