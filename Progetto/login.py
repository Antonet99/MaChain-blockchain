import json
import getpass
import hashlib
from support_functions import load_accounts
from encryption import encrypt, decrypt


class Login:

    def login(self):
        """
        Funzione per il login dell'utente, che controlla se l'username e la password inseriti corrispondono a quelli salvati nel database.
        Il controllo della password viene fatto tramite l'hash della password inserita dall'utente, che viene confrontato con l'hash salvato nel database.
        """

        accounts = load_accounts()

        username = input("Inserisci il tuo username: ").encode('utf-8')
        password = getpass.getpass(
            "Inserisci la tua password: ").encode('utf-8')

        # Verifica se username e hash della password inserita dall'utente corrisponda
        # a quella salvata nel database in fase di register.
        for account in accounts["accounts"]:
            if hashlib.sha256(username).hexdigest() == account["hashed_username"] and hashlib.sha256(password).hexdigest() == account["hashed_password"]:

                print("Login effettuato con successo.")
                return

            else:
                print("Username e password errati, riprova.")
                return self.login()


Login().login()
