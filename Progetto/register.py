import json
import getpass
import hashlib
from support_functions import load_accounts, save_accounts
from encryption import encrypt, decrypt


class Register:

    def register(self):

        accounts = load_accounts()

        # Input delle informazioni personali dell'utente
        # Verifica se l'username è già in uso
        username = input("Inserisci il tuo username: ").encode('utf-8')
        hashed_username = hashlib.sha256(username).hexdigest()

        for account in accounts["accounts"]:
            if account["hashed_username"] == hashed_username:
                print("L'username inserito è già in uso. Usa un altro nome.")
                return self.register()

        else:

            print("Username disponibile")

            # aggiungere controllo per la password di almeno tot caratteri

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
                "hashed_username": hashed_username,
                # bisogna convertire in stringa per poterlo salvare nel file json
                "hashed_password": hashed_password,
                "key01": key01,
                "key02": key02,
                "key03": key03,
                "key04": key04
            })

            if save_accounts(accounts) == True:
                print("Registrazione completata con successo.")


Register().register()
