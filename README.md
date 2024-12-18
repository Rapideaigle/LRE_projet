# LRE_projet



Projet Python : Analyse des Transactions Bitcoin



Ce projet vise a analyser les transactions associe a une adresse Bitcoin en utilisant l'api blockchain.info
Le script permet de filtrer et de sauvegarde les transactions d'une adresse precise a specifier lors du lancement du programme, avec des information sur le hash les entres, sortie, ...

Fonctionnalites principales :

-> Recuperation des transactions d'une adresse bitcoin
-> Extraction de donnees 
-> Sauvegarde des resultat sous format csv

Prerequis : 

-> python3
-> bibliotheque : requests pandas 

Pour intaller on entre dans le shell "pip install requests pandas"


Pour executer el programme on entre dans le shell on entre dans le shell "python3 bitcoin_transactions.py"

Puis on entre une adresse bitcoin de https://www.blockchain.com/fr/explorer
Si l'adresse est valide alors il sauvegardera les resultats dans un fichier CSV

Fonctionnement 

Le script envoie une requete a l'api blockchain.info pour recupere les transaction d'ubne adresse 
Les transactions sont filtres pour inclure seulement l'adresse que l'ont a entre 





