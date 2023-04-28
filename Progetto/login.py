import json
import getpass
import hashlib
from support_functions import load_accounts
from encryption import Encryption


class Login:

    def login(self):
        """
        Funzione per il login dell'utente, che controlla se l'username e la password inseriti corrispondono a quelli salvati nel database.
        Il controllo della password viene fatto tramite l'hash della password inserita dall'utente, che viene confrontato con l'hash salvato nel database.
        """

        accounts = load_accounts()
        logged_in = False

        while not logged_in:

            username = input("Inserisci il tuo username: ")
            hashed_username = hashlib.sha256(
                username.encode('utf-8')).hexdigest()

            password = getpass.getpass(
                "Inserisci la tua password: ")
            hashed_password = hashlib.sha256(
                password.encode('utf-8')).hexdigest()

            # Verifica se username e hash della password inserita dall'utente corrisponda
            # a quella salvata nel database in fase di register.

            for account in accounts["accounts"]:
                if hashed_username == account["hashed_username"] and hashed_password == account["hashed_password"]:
                    print("Login effettuato con successo.")
                    logged_in = True
                    break
            if not logged_in:
                print("Username e/o password errati, riprova.")


Login().login()
