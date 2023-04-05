import json
import getpass
import hashlib

path = "./Progetto/userpass.json"

"""
    Fare due classi diverse per login o registrazione.
"""


def load_accounts():
    with open(path, 'r') as file:
        return json.load(file)


def save_accounts(accounts):
    with open(path, 'w') as file:
        json.dump(accounts, file)


def register():

    accounts = load_accounts()

    # Input delle informazioni personali dell'utente
    # Verifica se l'username è già in uso
    username = input("Inserisci il tuo username: ")

    for account in accounts["accounts"]:
        if account["username"] == username:
            print("L'username inserito è già in uso. Usa un altro nome.")
            return register()

    else:

        print("Username disponibile")

        # encoding della password in utf-8 e stampa digest hash con sha256
        password = getpass.getpass(
            "Inserisci la tua password: ").encode('utf-8')
        hashed_password = hashlib.sha256(password).hexdigest()

        key01 = input("Inserisci la key01: ")
        key02 = input("Inserisci la key02: ")
        key03 = input("Inserisci la key03: ")
        key04 = input("Inserisci la key04: ")

        # Aggiunge l'account alla lista degli account
        accounts["accounts"].append({
            "username": username,
            # bisogna convertire in stringa per poterlo salvare nel file json
            "hash": hashed_password,
            "key01": key01,
            "key02": key02,
            "key03": key03,
            "key04": key04
        })

        save_accounts(accounts)
        print("Registrazione completata con successo.")


def login():
    """
    Funzione per il login dell'utente, che controlla se l'username e la password inseriti corrispondono a quelli salvati nel database.
    Il controllo della password viene fatto tramite l'hash della password inserita dall'utente, che viene confrontato con l'hash salvato nel database.
    """

    accounts = load_accounts()

    username = input("Inserisci il tuo username: ")

    # Per ogni account nel file json, controlla se l'username inserito dall'utente corrisponde
    # a quello salvato nel database in fase di register.
    for account in accounts["accounts"]:
        if account["username"] == username:
            # Se l'username è corretto, chiede la password e verifica se il digest
            # corrisponde a quello salvata nel database in fase di register.
            password = getpass.getpass(
                "Inserisci la tua password: ").encode('utf-8')

            # Verifica se l'hash della password inserita dall'utente corrisponda
            # a quella salvata nel database in fase di register.
            if hashlib.sha256(password).hexdigest() == account["hash"]:
                print("Login effettuato con successo.")
                return

            else:
                print("Password errata.")
                return login()

    print("Utente non esistente.")
    return login()


# Esempio di utilizzo delle funzioni
# register()
login()
