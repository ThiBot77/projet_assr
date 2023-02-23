#!/usr/bin/env python3
# Projet Python, LPASSR, 2022-2023
# Auteurs: Thibault BECHARD, Nicolas DAWIDOWICZ, Florian DOPP
# Date: 22/02/2023
# Description: Ce script permet de verifier si les mots de passe d'une base
# de donnees sont presents dans la base de donnees de HIBP.

from pathlib import Path
import configparser
import sys
import requests
import hashlib
import sqlite3
import argparse

def parse_args():
    # On analyse les arguments de ligne de commande
    parser = argparse.ArgumentParser(description='Vérifie si les mots de passe d\'une base de données sont présents dans la base de données de HIBP')
    parser.add_argument('-c', '--config', metavar='CONFIG_FILE', type=str, help='chemin vers le fichier de configuration')
    parser.add_argument('-d', '--db', metavar='DB_FILE', type=str, help='chemin vers le fichier de base de données')
    parser.add_argument('-a', '--api', metavar='API_URL', type=str, help='URL de l\'API HIBP')
    return parser.parse_args()


def load_config(config_path: str = "") -> dict:
    config_dict = configparser.ConfigParser()
    # Si le fichier de configuration n'est pas specifie, on renvoie une erreur
    if config_path != "":
        try:
            config_dict.read(config_path)
        except Exception:
            print("Impossible de lire le fichier de configuration",
                  file=sys.stderr)
            print("Vérifier que le fichier de configuration est correct")
            sys.exit(1)
    return config_dict


def load_db(db_path: str) -> list:
    data = []
    db_path = Path(db_path)
    # Si le fichier de base de donnees est au format csv
    if db_path.suffix == ".csv":
        try:
            with open(db_path, "r") as f:
                next(f)  # Pour sauter la premiere ligne
                for line in f:
                    login, password = line.strip().split(";")
                    data.append({"login": login, "password": password})
        except Exception:
            print("Une erreur est survenue lors de la lecture")
            print("Vérifier que le fichier de configuration est correct")
            sys.exit(1)
    # Si le fichier de base de donnees est au format sqlite3
    elif db_path.suffix == ".sqlite3":
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("SELECT login, password FROM user")
            for row in c.fetchall():
                data.append({"login": row[0], "password": row[1]})
        except Exception:
            print("Une erreur est survenue lors de la lecture")
            print("Vérifier que le fichier de configuration est correct")
            sys.exit(1)
    # Si le fichier de base de donnees n'est pas supporte
    else:
        print("Le fichier de base de donnees n'est pas supporte")
        sys.exit(1)
    return data


def check_if_pwned(api_url: str, passwd: str) -> int:
    try:
        sha1 = passwd
        # On verifie si le mot de passe est deja hashe en SHA1
        if (len(passwd) == 40
                and all(c in "0123456789abcdefABCDEF/" for c in passwd)):
            sha1 = passwd
        else:
            sha1 = hashlib.sha1(passwd.encode("utf-8")).hexdigest().upper()
        prefix = sha1[:5]
        suffix = sha1[5:]
        response = requests.get(str(api_url) + "/" + str(prefix))
        # Si la requete a l'API HIBP n'a pas reussi
        if response.status_code != 200:
            print("Une erreur est survenue lors de la requete a l'API HIBP")
            sys.exit(1)
        pwned = 0
        # On parcourt les lignes de la reponse de l'API HIBP
        for line in response.text.splitlines():
            if line.split(':')[0] == suffix.upper():
                pwned = int(line.split(':')[1])
                break
        return pwned
    except Exception:
        print("L'URL de l'API est incorrecte le fichier de configuration")
        sys.exit(1)


def main():
    # On analyse les arguments de ligne de commande
    args = parse_args()

    # On charge le fichier de configuration et la base de données
    base_dir = Path(__file__).parent
    config_path = args.config or (base_dir / "config.ini")
    config = load_config(str(config_path))
    try:
        db_path = args.db or config["db"]["path"]
        users = load_db(db_path)
    except Exception:
        print("Une erreur est survenue lors du chargement")
        print("Vérifier que le fichier de configuration est correct")
        sys.exit(1)
    # On vérifie si l'argument -a ou --api a été spécifié, sinon on utilise l'URL de l'API dans le fichier de configuration
    api_url = args.api or config["api"]["url"]
    
    print("La base de donnees contient {} utilisateurs".format(len(users)))
    print("{:<15} {:<8} {:<8}".format("login", "pwned", "count"))
    print("{:-<15} {:-<8} {:-<8}".format("", "", ""))
    for user in users:
        # On affiche le resultat de la verification pour chaque utilisateur
        try:
            count = check_if_pwned(api_url, user["password"])
            if count > 0:
                print("{:<15} {:<8} {:<8}".format(user["login"], "True", count))
            else:
                print("{:<15} {:<8} {:<8}".format(user["login"], "False", count))
        except Exception:
            print("Une erreur est survenue lors de la verification ")
            print("Vérifier que le fichier de configuration est correct")
            sys.exit(1)


if __name__ == "__main__":
    main()
