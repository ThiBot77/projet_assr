🐍 Projet Python, LPASSR, 2022-2023 🚀

Ce script permet de vérifier si les mots de passe d'une base de données sont présents dans la base de données de HIBP.
Auteurs

    Thibault BECHARD 🧑‍💻
    Nicolas DAWIDOWICZ 🧑‍💻
    Florian DOPP 🧑‍💻

Fonctionnalités

    Lecture d'une base de données (CSV ou SQLite3)
    Vérification des mots de passe présents dans la base de données avec l'API HIBP
    Affichage des résultats

Prérequis

    Python 3.x
    Packages Python : requests

Utilisation

bash

python3 script.py -c config.ini -d data.csv -a https://api.hibp.com

    -c / --config : Chemin vers le fichier de configuration (par défaut : config.ini)
    -d / --db : Chemin vers le fichier de base de données (obligatoire)
    -a / --api : URL de l'API HIBP (par défaut : URL dans le fichier de configuration)

Configuration

Le fichier de configuration config.ini contient les informations suivantes :

ini

[db]
path = chemin/vers/la/base/de/donnees

[api]
url = https://api.hibp.com

Exemple de résultats

yaml

La base de donnees contient 10 utilisateurs
login          pwned    count   
-------------- -------- --------
john           1        54       
paul           0        0        
george         1        2013     
ringo          0        0        
mick           1        2875     
keith          1        2013     
ronnie         1        2875     
charlie        1        2875     
bill           1        2013     
mickjagger     1        2875     

Avertissement

Il est important de noter que ce script peut envoyer des requêtes à l'API HIBP qui peut contenir des données sensibles. Il est donc recommandé de l'utiliser uniquement dans un environnement de test et de ne pas le distribuer avec des données réelles.
Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
