import json

path = "/Users/antoniobaio/Desktop/Progetti/ProgettoSSB/Progetto/userpass.json"


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
    for account in accounts["accounts"]:
        username = input("Inserisci il tuo username: ")
        if account["username"] == username:
            print("L'username inserito è già in uso.")
            return register()
        else:
            print("Username disponibile")
            break

    password = input("Inserisci la tua password: ")
    key01 = input("Inserisci la key01: ")
    key02 = input("Inserisci la key02: ")
    key03 = input("Inserisci la key03: ")
    key04 = input("Inserisci la key04: ")

    # Aggiunge l'account alla lista degli account
    accounts["accounts"].append({
        "username": username,
        "password": password,
        "key01": key01,
        "key02": key02,
        "key03": key03,
        "key04": key04
    })

    save_accounts(accounts)
    print("Registrazione completata con successo.")


def login():
    accounts = load_accounts()

    # Input delle informazioni di login dell'utente
    username = input("Inserisci il tuo username: ")
    password = input("Inserisci la tua password: ")

    # Verifica se l'username e la password sono corretti
    for account in accounts["accounts"]:
        if account["username"] == username and account["password"] == password:
            print("Login effettuato con successo.")
            return

    print("Username o password errati.")


# Esempio di utilizzo delle funzioni
# register()
login()
