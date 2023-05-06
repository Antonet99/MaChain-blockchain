import re
import getpass
import hashlib
from eth_account import Account
from web3.middleware import construct_sign_and_send_raw_middleware

from encryption import Encryption
from support_functions import load_accounts, save_accounts


class Register:

    def __init__(self, connections, config_params):
        self.connections = connections
        self.config_params = config_params

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

        accounts = load_accounts(self.config_params.get_path_user())
        encryption = Encryption()


        username = input("Inserisci il tuo username: ").encode('utf-8')
        hashed_username = hashlib.sha256(username).hexdigest()

        if len(accounts["accounts"]) > 0:
            for account in accounts["accounts"]:
                if account["hashed_username"] == hashed_username:
                    print("L'username inserito è già in uso. Usa un altro nome.")
                    return self.register()
                else:
                    print("Username disponibile")
        else:
            print("Username disponibile")

        password = self.insert_password()

        if self.validate_password(password) == False:
            print("Password non valida")

        # password = password.encode('utf-8')
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        key00 = input("Inserisci la key00: ")
        key01 = input("Inserisci la key01: ")
        key02 = input("Inserisci la key02: ")
        key03 = input("Inserisci la key03: ")

        token_key00 = encryption.password_encrypt(
            key00.encode(), password).decode()
        token_key01 = encryption.password_encrypt(
            key01.encode(), password).decode()
        token_key02 = encryption.password_encrypt(
            key02.encode(), password).decode()
        token_key03 = encryption.password_encrypt(
            key03.encode(), password).decode()

        # Aggiunge l'account alla lista degli account
        accounts["accounts"].append({
            "hashed_username": hashed_username,
            "hashed_password": hashed_password,
            "token_key00": token_key00,
            "token_key01": token_key01,
            "token_key02": token_key02,
            "token_key03": token_key03
        })


        try:
            account00 = Account.from_key(key00)
            account01 = Account.from_key(key01)
            account02 = Account.from_key(key02)
            account03 = Account.from_key(key03)


            self.connections[0].eth.default_account = account00.address
            self.connections[0].middleware_onion.add(
                construct_sign_and_send_raw_middleware(account00))

            self.connections[1].eth.default_account = account01.address
            self.connections[1].middleware_onion.add(
                construct_sign_and_send_raw_middleware(account01))

            self.connections[2].eth.default_account = account02.address
            self.connections[2].middleware_onion.add(
                construct_sign_and_send_raw_middleware(account02))

            self.connections[3].eth.default_account = account03.address
            self.connections[3].middleware_onion.add(
                construct_sign_and_send_raw_middleware(account03))

            if save_accounts(accounts, self.config_params.get_path_user()) == True:
                print("Registrazione completata con successo.")

            return True
        except:
            print("Errore durante la registrazione dell'account. Chiavi errate")
            return False

