# 🐍 Projet Python, LPASSR, 2022-2023 🚀

Ce script permet de verifier si les mots de passe d'une base de donnees sont presents dans la base de donnees de HIBP.

##  Auteurs : 

    Thibault BECHARD
    Nicolas DAWIDOWICZ
    Florian DOPP

##  Date : 
22/02/2023

## Pré-requis : 

    Python 3.6 ou version ultérieure
    Bibliothèques Python :
        pathlib
        configparser
        sys
        requests
        hashlib
        sqlite3
        argparse

## Utilisation :

    python3 verify_password.py [-h] [-c CONFIG_FILE] [-d DB_FILE] [-a API_URL]

### Options :

    -h, --help : affiche l'aide du script
    -c CONFIG_FILE, --config CONFIG_FILE : chemin vers le fichier de configuration
    -d DB_FILE, --db DB_FILE : chemin vers le fichier de base de données
    -a API_URL, --api API_URL : URL de l'API HIBP

## Format des fichiers :

### Fichier de configuration : 

Le fichier de configuration doit être au format INI et contenir les sections suivantes :

    [db]
    path = chemin/vers/la/base/de/donnees
    
    [api]
    url = URL_de_l_API_HIBP

## Base de données :

Le script prend en charge les bases de données au format CSV et SQLite3.

### CSV :

Le fichier CSV doit contenir deux colonnes, séparées par un point-virgule (;) : login et password. La première ligne du fichier doit être un en-tête et ne sera pas lue.

### Exemple :

    login;password
    john_doe;password1
    jane_doe;password2

### SQLite3 :

La base de données SQLite3 doit contenir une table user avec deux colonnes : login et password.
Description du script

Le script vérifie si les mots de passe d'une base de données sont présents dans la base de données de HIBP (Have I Been Pwned). Il utilise l'API HIBP pour rechercher les mots de passe compromis.

Le script prend en charge les fichiers de base de données au format CSV et SQLite3.

### Fonctions : 

    parse_args(): analyse les arguments de ligne de commande
    load_config(config_path: str = "") -> dict: charge le fichier de configuration
    load_db(db_path: str) -> list: charge la base de données
    check_if_pwned(api_url: str, passwd: str) -> int: vérifie si un mot de passe est compromis en utilisant l'API HIBP
    main(): fonction principale du script

### Options de ligne de commande : 

    -c, --config: chemin vers le fichier de configuration
    -d, --db: chemin vers le fichier de base de données
    -a, --api: URL de l'API HIBP

### Exemple d'utilisation : 

    python3 verify_password.py -c config.ini -d data.csv -a https://api.pwne
