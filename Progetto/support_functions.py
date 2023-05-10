import os
import re
import json


def load_accounts(path):
    with open(path, 'r') as file:
        return json.load(file)


def save_accounts(accounts, path):
    with open(path, 'w') as file:
        json.dump(accounts, file)
        return True


def clear_terminal():
    if os.name == 'posix':
        os.system('clear')
    # else screen will be cleared for windows
    else:
        os.system('cls')


"""
Funzione per verificare che un URL sia contenga la regex 'http://'
Termina il programma se l'URL non soddisfa questa condizione
:param: url da controllare
"""


def check_url(url):
    reg_ex_urls = "http://.*"
    if re.search(reg_ex_urls, url) is None:
        print("Errore: \n"
              + "Il parametro '" + url + "' non è un URL che che rispetta le specifiche \n"
              + "Interruzione del programma")
        exit(1)


"""
Funzione per controllare se una path esiste
Se la path non esiste termina l'esecuzione del programma
:param: path da controllare
"""


def check_path(path):
    if not os.path.exists(path):
        print("Errore: \n"
              + "La path '" + path + "' non esiste \n"
              + "Interruzione del programma")
        exit(1)


def check_int(integer):
    if not isinstance(integer, int):
        print("Errore: \n"
              + " Il gas price deve essere un intero \n"
              + "Interruzione del programma")
        exit(1)


def check_str(string):
    if not isinstance(string, str):
        print("Errore: \n"
              + "Il nome dello smart contract deve essere una stringa \n"
              + "Interruzione del programma")
        exit(1)
