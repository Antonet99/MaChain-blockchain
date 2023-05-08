import os
import json


class Transactioner:
    def __init__(self, config_params, connections, on_chain_manager_contract):
        self.config_params = config_params
        self.connections = connections
        self.on_chain_manager_contract = on_chain_manager_contract
        self.smart_contracts = self.get_available_smart_contracts()

    # funzione che restituisce la lista degli smart contract disponibili

    def get_available_smart_contracts(self):
        available_addresses = {}
        for shard in range(1, 4):
            file_path = "../ABIs/shard_" + str(shard) + ".json"
            if os.path.exists(file_path):
                with open(file_path) as json_file:
                    data = json.load(json_file)
                    for item in data:
                        available_addresses[item] = data[item]
        return available_addresses

    # funzione che stampa gli smart contract disponibili e permette all'utente di scegliere con quale
    # smart contract lavorare

    def print_and_choose_smart_contract(self):

        if len(self.smart_contracts) == 0:
            print("Non ci sono ancora Smart Contract con cui interagire. \n")
            return

        else:
            print("La lista degli smart contract presenti nel sistema è la seguente:")
            for index, smart_contract in enumerate(self.smart_contracts):
                print(str(index + 1) + ") " + smart_contract)

            chosen_index = input("Per favore, inserisci il numero corrispondente allo smart contract dediserato: ")
            # controllo che l'indice sia effettivamente un numero e che rientri nel range possibile
            while not chosen_index.isnumeric() or int(chosen_index) not in range(1, len(self.smart_contracts) + 1):
                chosen_index = input("Per favore, inserire un numero valido: ")
            chosen_index = int(chosen_index)
            # l'indice di accesso viene decrementato perchè all'utente viene stampata la lista partendo da 1
            address = list(self.smart_contracts)[chosen_index - 1]
            abi = self.smart_contracts[address]
            self.print_and_choose_smart_contract_function(abi, address)

    def print_and_choose_smart_contract_function(self, abi, address):
        # Filtro le sole funzioni dall'abi e le salvo in una lista
        functions = []
        for item in abi:
            if item["type"] == "function":
                functions.append(item)

        print("Le funzioni disponibili sullo smart contract selezionato sono le seguenti:")
        for index, fun in enumerate(functions):
            print(str(index + 1) + ") " + fun["name"])

        index = input("\n" + "Selezionare funzione da voler utilizzare: ")
        while not index.isnumeric or int(index) not in range(1, len(functions) + 1):
            index = input("Per favore, selezionare un numero corretto. ")
        index = int(index) - 1
        function_name = functions[index]["name"]
        function_parameters = functions[index]["inputs"]
        function_type = functions[index]["stateMutability"]
        function_arguments = []

        if len(function_parameters) == 0:
            print("\n" + "La funzione non richiede parametri.")
        else:
            if len(function_parameters) == 1:
                print("\n" + "La funzione richiede 1 parametro.")
            else:
                print("\n" + "La funzione richiede " + str(len(function_parameters)) + " parametri.")

            print("In particolare, i parametri richiesti sono i seguenti: ")
            for param in function_parameters:
                print("- \"" + param["name"] + "\"" + ", di tipo " + param["type"])

            for param in function_parameters:
                passed_param = input("Inserire parametro " + param["name"] + "(" + param["type"] + "):")
                '''if param["type"] == "uint256":
                    passed_param = Web3.to_int(int(passed_param))
                '''
                casted_param = self.cast_parameters(passed_param, param["type"])
                function_arguments.append(casted_param)

        shard_number = self.on_chain_manager_contract.functions.get_shard_where_contract(address).call()
        shard_connection = self.connections[shard_number]
        smart_contract = shard_connection.eth.contract(address=address, abi=abi)
        function_signature = self.get_function_signature(function_name, function_parameters)

        self.call_function(shard_connection, smart_contract, function_type, function_signature, function_arguments)

    def call_function(self, shard_connection, smart_contract, function_type, function_signature, function_arguments):
        if function_type == "pure" or function_type == "view":
            if len(function_arguments) == 0:
                contract_func = smart_contract.get_function_by_name(function_signature)
                print(contract_func().call())
            else:
                contract_func = smart_contract.get_function_by_signature(function_signature)
                print(contract_func(*function_arguments).call())

        elif function_type == "nonpayable" or function_type == "payable":
            contract_func = smart_contract.get_function_by_signature(function_signature)
            tx_hash = contract_func(*function_arguments).transact()
            receipt = shard_connection.eth.wait_for_transaction_receipt(tx_hash)

    def get_function_signature(self, function_name, provided_arguments):
        # N.B. con l'onchain funzionava con ["InternalType"]
        signature = function_name
        if len(provided_arguments) == 0:
            pass
        elif len(provided_arguments) == 1:
            signature += "(" + provided_arguments[0]["type"] + ")"
        else:
            for index, item in enumerate(provided_arguments):
                if index == 0:
                    signature += "(" + item["type"]
                elif index == len(provided_arguments) - 1:
                    signature += "," + item["type"] + ")"
                else:
                    signature += "," + item["type"]
        return signature

    def get_url_shard_where_sc_is(self, number, connections):
        if number == 1:
            return connections[1]
        elif number == 2:
            return connections[2]
        elif number == 3:
            return connections[3]

    def cast_parameters(self, function_argument, function_type):
        if "int" in function_type:
            return int(function_argument)
        elif function_type == "bool":
            return bool(function_argument)
        else:
            return function_argument

