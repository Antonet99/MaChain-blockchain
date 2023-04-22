import os
from web3 import Web3
import json

# funzione che restituisce la lista degli smart contract disponibili
def get_available_smart_contracts():
    available_addresses = {}
    for shard in range(1,4):
        file_path = "ABIs/shard_"+str(shard)+".json"
        if os.path.exists(file_path):
            with open(file_path) as json_file:
                data = json.load(json_file)
                for item in data:
                    available_addresses[item] = data[item]
    return available_addresses

# funzione che stampa gli smart contract disponibili e permette all'utente di scegliere con quale
# smart contract lavorare, restituendo i dati ad esso relativi.
# N.B. si è evitato di accedere più volta in lettura sul file salvando i dati prima su un dizionario 
# (per restituire in maniera semplice il risultato finale), poi convertendo il dizionario in lista
# (così da poter utilizzare gli indici invece dell'address per accedere allo smart contract)
def choose_smart_contract():
    smart_contracts_dict = get_available_smart_contracts()
    smart_contracts_list = list(smart_contracts_dict)
    print("La lista degli smart contract presenti nel sistema è la seguente:")
    for index in range(0, len(smart_contracts_list)):
        print( str(index+1) +") " + smart_contracts_list[index])
    chosen_index = input("Per favore, inserisci il numero corrispondente allo smart contract dediserato: ")
    # controllo che l'indice sia effettivamente un numero e che rientri nel range possibile
    while(not chosen_index.isnumeric() or int(chosen_index) not in range(1, len(smart_contracts_list)+1)):
        chosen_index = input("Per favore, inserire un numero valido: ")
    chosen_index = int(chosen_index)
    # l'indice di accesso viene decrementato perchè all'utente viene stampata la lista partendo da 1
    address = smart_contracts_list[chosen_index-1]
    abi = smart_contracts_dict[address]
    #transact(key, value)
    

    choose_smart_contract_function(abi, address)
    transact(address, abi)

# Se lo SC non ha funzioni?? Può succedere??
def choose_smart_contract_function(abi, address):
    # Filtro le sole funzioni dall'abi e le salvo in una lista 
    functions = []
    for item in abi:
        if item["type"] == "function":
            functions.append(item)

    print("Le funzioni disponibili sullo smart contract selezionato sono le seguenti:")
    for fun in functions:
        index = 1 
        print(str(index)+ ") " + fun["name"])
        index += 1

    index = input("\n" + "Selezionare funzione da voler utilizzare: ")
    while (not index.isnumeric or int(index) not in range(1, len(functions)+1)):
            index = input("Per favore, selezionare un numero corretto. ")
    index = int(index) - 1
    function_parameters = functions[index]["inputs"]

    if len(function_parameters) == 0 :
        print("\n" + "La funzione non richiede parametri.")
    else:
        print("\n" + "La funzione richiede "+ str(len(function_parameters))+ " parametri.")
        print("In particolare, i parametri richiesti sono i seguenti: ")
        for param in function_parameters :
            print("- \"" + param["name"] + "\"" + ", di tipo " + param["type"])
        for param in function_parameters :
            input("Inserire parametro" + param["name"] + "("+ param["type"] + "):")
            # manca il check dei paramtri: come fare a controllare ad esempio l'address?
            # quanti tipi di parametri possono esserci? (uint8, address e poi?)

    # una volta fatti i controlli e so che è tutto ok, chiedo conferma all'utente e provo 
    # a fare la transazione
    smart_contract = Web3.eth.contract(
    address=address,
    abi= abi)
    signature = function[index]
    function_to_call = smart_contract.get_function_by_signature(signature)


    # https://docs.soliditylang.org/en/v0.8.19/contracts.html  per vedere tipi di funzioni
    # https://ethereum.stackexchange.com/questions/134720/execute-a-contract-function-from-web3-py 
    # qui dice che posso usare .call per funzioni di tipo view o pure
    # per le altre devo costruire una transazione

