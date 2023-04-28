import re
import getpass
import hashlib
from encryption import Encryption
from support_functions import load_accounts, save_accounts


class Register:

    def validate_password(self, password):

        val = True

        while True:
            if len(password) < 8:
                print("La password deve contenere almeno 8 caratteri")
                val = False
            elif re.search('[0-9]', password) is None:
                print("La password deve contenere almeno un carattere numerico")
                val = False
            elif re.search('[A-Z]', password) is None:
                print("La password deve contenere almeno una lettera maiuscola")
                val = False
            elif re.search('[^a-zA-Z0-9]', password) is None:
                print("La password deve contenere almeno un carattere speciale")
                val = False
            else:
                print("Password valida")
                return val

            password = self.insert_password()

    def insert_password(self):
        password = getpass.getpass(
            "Inserisci la tua password: ")
        return password

    def register(self):

        accounts = load_accounts()
        encryption = Encryption()

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

        password = self.insert_password()

        if self.validate_password(password) == False:
            print("Password non valida")

        # password = password.encode('utf-8')
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        key01 = input("Inserisci la key01: ")
        key02 = input("Inserisci la key02: ")
        key03 = input("Inserisci la key03: ")
        key04 = input("Inserisci la key04: ")

        token_key01 = encryption.password_encrypt(
            key01.encode(), password).decode()
        token_key02 = encryption.password_encrypt(
            key02.encode(), password).decode()
        token_key03 = encryption.password_encrypt(
            key03.encode(), password).decode()
        token_key04 = encryption.password_encrypt(
            key04.encode(), password).decode()

        # Aggiunge l'account alla lista degli account
        accounts["accounts"].append({
            "hashed_username": hashed_username,
            "hashed_password": hashed_password,
            "token_key01": token_key01,
            "token_key02": token_key02,
            "token_key03": token_key03,
            "token_key04": token_key04
        })

        if save_accounts(accounts) == True:
            print("Registrazione completata con successo.")


Register().register()
