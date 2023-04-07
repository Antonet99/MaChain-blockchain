import json

import solcx
from web3 import Web3
from clear_terminal import clear_terminal

'''
Classe per effettuare il bootstrap del programma

Passi del bootstrap:

1) Leggere il file config.json che contiene tutte le impostazioni del programma
1.1) Termina l'esecuzione se il file config.json non è presente o se ci sono errori di lettura

2) Stabilire le connessioni alle 4 shard utilizzate dal programma
2.1) Se non si riesce a stabilire anche una sola delle connessioni, chiedere all'utente se intende riprovare a connettersi
2.2) Se l'utente risponde di no, terminare l'esecuzione
2.3) Se l'utente risponde di si, riprovare a connettersi
2.4) Salvare le variabili provider di web3

3) Leggere il file delle abi dello smart contract on-chain manager
3.1) Se non è presente il file terminare l'esecuzione
3.2) Se il file è vuoto, avvisare l'utente che manca l'on-chain manager
3.3) Deployare l'on-chain manager con un account di default? oppure aspettare che l'utente faccia il login e deployarlo con il suo account?
3.4) Se la lettura va a buon fine estrarre l'address e le abi dell'on-chain manager
3.5) Creare l'oggetto contratto dell'on-chain manager sulla shard 0

4) Provare a contattare l'on-chain manager richiamandone una funzione (get_shard_where_deploy)
4.1) Se l'on-chain manager non risponde, avvisare l'utente che sarà necessario deployarne uno nuovo dato che quello salvato non esiste più (magari perchè il container di ganache è stato riavviato)
4.2) Se risponde tutto ok e salvarsi in una variabile della classe l'oggetto contratto dell'on-chain manager

5) Se tutto è andato a buon fine, salvare nel main le variabili relative a:
    - dizionario config che contiene le variabili di configurazione
    - variabili provider delle 4 shard
    - variabile contratto dell'on-chain manager

NB: Capire se, nel caso si verificasse un eccezione durante il bootstrap relativa alla presenza dell'on-chain manager,
    deployarlo con un account di default oppure aspettare che l'utente faccia il login e deployarlo con il suo account.
    
Alternative flow:
5) Se si verifica un'eccezione e bisogna deployare nuovamente o come prima volta l'on-chain manager, chiedere all'utente conferma
5.1) Se l'utente conferma, deployare l'on-chain manager, salvarne indirizzo e abi e svuotare i file delle abi delle shard 1,2 e 3
'''


class Bootstrap:

    def __init__(self):
        self.config_path = "../Config/config.json"
        self.json_config = self.read_config()
        self.connections = self.get_connections()
        self.on_chain_manager_contract = self.get_on_chain_manager_contract()

    # Funzione per ottenere il dizionario contenente le impostazioni di configurazione
    def get_json_config(self):
        return self.json_config

    # Funzione per leggere il JSONObject dal file config.json
    # Nel file config.json andranno inserite le variabili da utilizzare per il programma
    def read_config(self):
        try:
            with open(self.config_path, 'r') as file_config:
                text_file = file_config.read()
                json_config = json.loads(text_file)
        except Exception as e:
            clear_terminal()
            print(
                "Errore: \n"
                + "Non è stato possibile leggere il file config.json contenente le impostazioni \n"
                + "Interruzione del programma"
            )
            exit(1)

        return json_config

    # Funzione per ottenere la connessione alle quattro shard utilizzate
    # Ritorna un vettore contenente le connessioni alle quattro shards
    # Ritorna False se la connessione non è riuscita
    def try_connections(self):
        try:
            shard_0 = Web3(Web3.HTTPProvider(self.json_config["url_shard_0"]))  # on-chain
            shard_1 = Web3(Web3.HTTPProvider(self.json_config["url_shard_1"]))  # shard 1
            shard_2 = Web3(Web3.HTTPProvider(self.json_config["url_shard_2"]))  # shard 2
            shard_3 = Web3(Web3.HTTPProvider(self.json_config["url_shard_3"]))  # shard 3
        except Exception as e:
            clear_terminal()
            print("Errore:")
            print(e)
            return False

        if (not shard_0.is_connected()) or (not shard_1.is_connected()) or (not shard_2.is_connected()) or (not shard_3.is_connected()):
            clear_terminal()
            print(
                "Errore: \n"
                + "Non è stato possibile effettuare la connessione a una o più shard"
            )
            return False
        return [shard_0, shard_1, shard_2, shard_3]

    # Funzione che richiama try_connections e in caso di fallimento della connessione chide all'utente se voglia
    # tentare nuovamente a connettersi, altrimenti esce dal programma
    def get_connections(self):
        connections = self.try_connections()
        while not connections:
            print("Vuoi ritentare la connessione alle shard? [s/n]")
            selezione = input()
            while selezione != 's' and selezione != 'n':
                print("Inserisci solo 's' oppure 'n'")
                selezione = input()
            if selezione == 'n':
                print("Interruzione del programma")
                exit(1)
            else:
                connections = self.try_connections()
        return connections

    # Funzione per controllare se siano salvate le ABI dell'onchain manager sul file
    def read_and_try_on_chain_manager(self):
        try:
            with open(self.json_config["path_abis_shard_0"], 'r') as file_abi:
                text_abi = file_abi.read()
                json_abi = json.loads(text_abi)
        except:
            clear_terminal()
            print(
                "Errore nella lettura del file contenente le ABI dell'on-chain manager \n"
                + "Interruzione del programma"
            )
            exit(1)

        if len(json_abi.keys()) != 1:
            print(
                "Non è presente alcun on-chain manager salvato"
                # Se non è presente l'onchain manager che si fa? si depolya ora con un account di default oppure si aspetta che l'utente faccia il login?
            )
            return False
        else:
            address = list(json_abi.keys())[0]
            abi = json_abi[address]
            return self.try_on_chain_manager(address, abi)

    # Funzione per provare a chiamare una funzione dell'on chain manager registrato
    def try_on_chain_manager(self, address_on_chain_manager, abi_on_chain_manager):
        on_chain_manager_contract = self.connections[0].eth.contract(
            address=address_on_chain_manager,
            abi=abi_on_chain_manager
        )
        try:
            prova = on_chain_manager_contract.functions.get_shard_where_deploy().call()
        except Exception as e:
            print(
                "Errore: \n"
                + "Lo smart contract dell'on-chain manager non risponde"
            )
            print('"' + str(e) + '"')
            return False
        if prova in [1,2,3]:
            return on_chain_manager_contract
        else:
            return False

    # Funzione che utilizza le due sopra per controllare l'esistenza dell'on-chain manager
    # In caso non esistesse chiede all'utente se vuole effettuarne il deploy
    # Restituisce il contratto dell'on-chain manager oppure esce dal programma
    def get_on_chain_manager_contract(self):
        on_chain_manager_contract = self.read_and_try_on_chain_manager()
        if not on_chain_manager_contract:
            print(
                "Sarà necessario effettuare il deploy di un nuovo smart contract dell'on-chain manager \n"
                + "Vuoi procedere con il deploy? [s/n]"
            )
            selezione = input()
            while selezione not in ['s', 'n']:
                print("Inserire solo 's' oppure 'n'")
                selezione = input()
            if selezione == 'n':
                print("Interruzione del programma")
                exit(1)
            else:
                return self.deploy_on_chain_manager_with_default_account()
        else:
            return on_chain_manager_contract

    # Funzione per effettuare il deploy dell'on-chain manger con un account di default
    def deploy_on_chain_manager_with_default_account(self):
        self.connections[0].eth.default_account = self.connections[0].eth.accounts[0] # Account di default numero 0

        solcx.install_solc(self.json_config["pragma_solidity_on_chain_manager"]) # Installazione della versione del compilatore in base al pragma impostato nel file config.json
        solcx.set_solc_version(self.json_config["pragma_solidity_on_chain_manager"])

        # Compilazione dello smart contract dell'on-chain manager
        try:
            compiled_solidity = solcx.compile_files([self.json_config["path_smart_contract_on_chain_manager"]]) # Compilazione dell'on-chain manager

            key = self.json_config["path_smart_contract_on_chain_manager"]+':'+self.json_config["name_on_chain_manager_contract"]
            bytecode = compiled_solidity[key]['bin']
            abi = json.loads(json.dumps(compiled_solidity[key]))['abi']
        except Exception as exception:
            jsonError = json.loads(json.dumps(exception.__dict__))
            print("Attenzione! E' stato generato il seguente errore durante la compilazione: \n" + jsonError[
                "stderr_data"]
                  + "In " + "\"" + jsonError["command"][1] + "\"" +
                  ", con return code: " + str(jsonError["return_code"]) + ".")
            print("Non è stato possibile compilare lo smart contract dell'on-chain manager \n"
                  + "Interruzione del programma")
            exit(1)

        contratto = self.connections[0].eth.contract(abi=abi, bytecode=bytecode)

        # esecuzione della transazione di deploy dello smart contract
        try:
            tx_hash = contratto.constructor().transact()
            tx_receipt = self.connections[0].eth.wait_for_transaction_receipt(tx_hash)
        except Exception as exception:
            print("Errore: \n")
            print(exception)
            print("La transazione di deploy dello smart contract non è andata a buon fine")
            print("Interruzione del programma")
            exit(1)

        # creazione dell'oggetto contratto per interagirci
        on_chain_manager_contract = self.connections[0].eth.contract(
            address=tx_receipt.contractAddress,
            abi=abi
        )

        # salvataggio abi su file
        self.save_on_chain_manager_abi(tx_receipt.contractAddress, abi)

        return on_chain_manager_contract

    # Funzione per salvare su file le abi dello smart contract dell'on-chain manager
    # Inoltre resetta anche i file delle abi delle varie shard
    def save_on_chain_manager_abi(self, address, abi):
        result = {address: abi}
        f = open(self.json_config["path_abis_shard_0"], 'w+')
        f.write(json.dumps(result))
        f.close()

        f = open(self.json_config["path_abis_shard_1"], 'w+')
        f.write(json.dumps({}))
        f.close()

        f = open(self.json_config["path_abis_shard_2"], 'w+')
        f.write(json.dumps({}))
        f.close()

        f = open(self.json_config["path_abis_shard_3"], 'w+')
        f.write(json.dumps({}))
        f.close()

    # Funzione da utilizzare nel main per ottenere le variabili da utilizzare nel programma
    def get_program_variables(self):
        return self.json_config, self.connections, self.on_chain_manager_contract
