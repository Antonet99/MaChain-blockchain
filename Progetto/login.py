import json
import getpass
import hashlib
from support_functions import load_accounts
from register import Register
from encryption import Encryption
from eth_account import Account
from web3.middleware import construct_sign_and_send_raw_middleware


class Login:

    def __init__(self, connections, config_params):
        self.connections = connections
        self.config_params = config_params

    def logout(self, connections):
        """
        Funzione per il logout dell'utente, che elimina il middleware aggiunto in fase di login.
        """

        connections[0].middleware_onion.clear()
        connections[1].middleware_onion.clear()
        connections[2].middleware_onion.clear()
        connections[3].middleware_onion.clear()

        if len(connections[0].middleware_onion) == 0 and len(connections[1].middleware_onion) == 0 and len(connections[2].middleware_onion) == 0 and len(connections[3].middleware_onion) == 0:
            print("Logout effettuato con successo.")
        else:
            print("Logout non effettuato. Addio.")
            exit(1)

    def check_accounts(self, accounts, hashed_username, hashed_password):

        for account in accounts["accounts"]:
            if hashed_username == account["hashed_username"] and hashed_password == account["hashed_password"]:
                return True
            else:
                return False

    def login(self):
        """
        Funzione per il login dell'utente, che controlla se l'username e la password inseriti corrispondono a quelli salvati nel database.
        Il controllo della password viene fatto tramite l'hash della password inserita dall'utente, che viene confrontato con l'hash salvato nel database.
        """
        accounts = load_accounts(self.config_params.get_path_user())
        encryption = Encryption()
        counter = 0

        while True:

            counter += 1
            if counter == 4:
                print("Troppi tentativi di accesso. Interruzione del programma.")
                exit(1)

            if len(accounts["accounts"]) == 0:
                print("Non ci sono account registrati. Effettua la registrazione.")
                return
            else:
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

                        token_key00 = encryption.password_decrypt(
                            account["token_key00"].encode(), password).decode()
                        token_key01 = encryption.password_decrypt(
                            account["token_key01"].encode(), password).decode()
                        token_key02 = encryption.password_decrypt(
                            account["token_key02"].encode(), password).decode()
                        token_key03 = encryption.password_decrypt(
                            account["token_key03"].encode(), password).decode()

                        account00 = Account.from_key(token_key00)
                        account01 = Account.from_key(token_key01)
                        account02 = Account.from_key(token_key02)
                        account03 = Account.from_key(token_key03)

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

                        print("Login effettuato con successo.")
                        counter = 0
                        return True

                    else:
                        print("Username e/o password errati, riprova.")