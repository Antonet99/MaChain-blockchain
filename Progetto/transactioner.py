import os
import numpy as np
import web3
from web3 import Web3
import json
from eth_abi import encode, encode_abi


# funzione che restituisce la lista degli smart contract disponibili
def get_available_smart_contracts():
    available_addresses = {}
    for shard in range(1, 4):
        file_path = "../ABIs/shard_"+str(shard)+".json"
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
def choose_smart_contract(config_params, connections, on_chain_manager_contract):
    smart_contracts_dict = get_available_smart_contracts()
    smart_contracts_list = list(smart_contracts_dict)
    if len(smart_contracts_list) == 0:
        print("Non ci sono ancora Smart Contract con cui interagire. \n")
        return
    else:
        print("La lista degli smart contract presenti nel sistema è la seguente:")
        for index in range(0, len(smart_contracts_list)):
            print( str(index+1) + ") " + smart_contracts_list[index])
        chosen_index = input("Per favore, inserisci il numero corrispondente allo smart contract dediserato: ")
        # controllo che l'indice sia effettivamente un numero e che rientri nel range possibile
        while(not chosen_index.isnumeric() or int(chosen_index) not in range(1, len(smart_contracts_list)+1)):
            chosen_index = input("Per favore, inserire un numero valido: ")
        chosen_index = int(chosen_index)
        # l'indice di accesso viene decrementato perchè all'utente viene stampata la lista partendo da 1
        address = smart_contracts_list[chosen_index-1]
        abi = smart_contracts_dict[address]
        # transact(key, value)
        choose_smart_contract_function(abi, address, config_params, on_chain_manager_contract, connections)
        # transact(address, abi)

# Se lo SC non ha funzioni?? Può succedere??
def choose_smart_contract_function(abi, address, config_params, on_chain_manager_contract, connections):
    # Filtro le sole funzioni dall'abi e le salvo in una lista 
    functions = []
    for item in abi:
        if item["type"] == "function":
            functions.append(item)

    print("Le funzioni disponibili sullo smart contract selezionato sono le seguenti:")
    index = 1
    for fun in functions:
        print(str(index) + ") " + fun["name"])
        index += 1

    index = input("\n" + "Selezionare funzione da voler utilizzare: ")
    while (not index.isnumeric or int(index) not in range(1, len(functions) +1)):
            index = input("Per favore, selezionare un numero corretto. ")
    index = int(index) - 1
    function_name = functions[index]["name"]
    function_parameters = functions[index]["inputs"]
    function_type = functions[index]["stateMutability"]
    functon_arguments = []

    if len(function_parameters) == 0:
        print("\n" + "La funzione non richiede parametri.")
    else:
        #print(function_parameters)
        print("\n" + "La funzione richiede "+ str(len(function_parameters)) + " parametri.")
        print("In particolare, i parametri richiesti sono i seguenti: ")
        for param in function_parameters:
            print("- \"" + param["name"] + "\"" + ", di tipo " + param["type"])
        for param in function_parameters:
            passed_param = input("Inserire parametro " + param["name"] + "(" + param["type"] + "):")
            print("mao" + param["type"])
            if param["type"] == "uint256":
                passed_param = Web3.toInt(int(passed_param))
                print("maomao" + str(type(passed_param)))

            functon_arguments.append(passed_param)
    shard_number = on_chain_manager_contract.functions.get_shard_where_contract(address).call()
    shard_url = get_url_shard_where_sc_is(shard_number, connections)
    # smart_contract = create_smart_contract_instance(shard_url, address, abi)
    web3 = Web3(Web3.HTTPProvider(shard_url)) ## sostituire con connections
    smart_contract = web3.eth.contract(address=address,abi=abi)
    function_signature = get_function_signature(function_name, function_parameters)
    #encoded_arguments = encode_parameters(function_parameters, passed_param)
    call_function(web3, smart_contract, function_type, function_signature, functon_arguments, function_name, connections)

    '''
    if len(functon_arguments) == 0:
        contract_func = smart_contract.get_function_by_name(function)
        print(contract_func)
        contract_func().call()
    else:
        contract_func = smart_contract.get_function_by_signature(function)
        print(contract_func)
        contract_func(*functon_arguments).call()
    '''
            # manca il check dei paramtri: come fare a controllare ad esempio l'address?
            # quanti tipi di parametri possono esserci? (uint8, address e poi?)

    # una volta fatti i controlli e so che è tutto ok, chiedo conferma all'utente e provo 
    # a fare la transazione con la funzione su
    ## questa funzione deve restituire la stringa per chiamare get_function_by_signature

'''def check_argument(argument, type):
    if type == "address":
        return address(bytes20(bytes(argument)))
'''


def call_function(w3, smart_contract, function_type, function_signature, function_arguments, name, connections):
    if function_type == "pure" or function_type == "view":
        if len(function_arguments) == 0:
            contract_func = smart_contract.get_function_by_name(function_signature)
            print(contract_func)
            print(contract_func().call())
        else:
            contract_func = smart_contract.get_function_by_signature(function_signature)
            print(contract_func(*function_arguments).call())

    elif function_type == "nonpayable" or function_type == "payable":
        contract_func = smart_contract.get_function_by_signature(function_signature)
        tx_hash = contract_func(*function_arguments).transact()
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Transaction receipt mined:")
        print(dict(receipt))
        print("\nWas transaction successful?")
        print(receipt["status"])


# non si capisce se serve o meno, l'ho messa perchè senza dava errore di encoding
def encode_parameters(function_params, passed_params):
    function_types = []
    for item in function_params:
        function_types.append(item["type"])
    return encode_abi(function_types, passed_params)


def get_function_signature(function_name, provided_arguments):
    signature = function_name
    if len(provided_arguments) == 0:
        pass
    elif len(provided_arguments) == 1:
        signature += "(" + provided_arguments[0]["internalType"] + ")"
    else:
        for index, item in enumerate(provided_arguments):
            if index == 0:
                signature += "(" + item["internalType"]
            elif index == len(provided_arguments)-1:
                signature += "," + item["internalType"] + ")"
            else:
                signature += "," + item["internalType"]
    return signature


def create_smart_contract_instance(url, address, abi):
    web3 = Web3(Web3.HTTPProvider(url))
    return web3.eth.contract(address = address,
                             abi = abi)


def get_url_shard_where_sc_is(number, connections):
    if number == 1:
        return connections[1]
    elif number == 2:
        return connections[2]
    elif number == 3:
        return connections[3]
