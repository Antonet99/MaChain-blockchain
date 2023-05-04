import json
import re
import os
import solcx
from web3 import Web3
from support_functions import clear_terminal
from config_params import ConfigParams

'''
Classe per effettuare il bootstrap del programma

Passi del bootstrap:

1) Leggere il file config.json che contiene tutte le impostazioni del programma
1.1) Termina l'esecuzione se il file config.json non è presente o se ci sono errori di lettura
1.2) Verifica l'integrità del file di configurazione, se non rispetta le specifiche termina il programma

2) Stabilire le connessioni alle 4 shard utilizzate dal programma
2.1) Se non si riesce a stabilire anche una sola delle connessioni, chiede all'utente se intende riprovare a connettersi
2.2) Se l'utente risponde di no, terminare l'esecuzione
2.3) Se l'utente risponde di si, riprovare a connettersi
2.4) Salvare le variabili provider di web3

3) Leggere il file delle abi dello smart contract on-chain manager
3.1) Se non è presente il file terminare l'esecuzione
3.2) Se il file è vuoto, avvisare l'utente che manca l'on-chain manager
3.3) Deployare l'on-chain manager con un account di default? oppure aspettare che l'utente faccia il login e deployarlo
     con il suo account? La funzione implementata attualmente utilizza il primo account di default
3.4) Se la lettura va a buon fine estrarre l'address e le abi dell'on-chain manager
3.5) Creare l'oggetto contratto dell'on-chain manager sulla shard 0

4) Provare a contattare l'on-chain manager richiamandone una funzione (get_shard_where_deploy)
4.1) Se l'on-chain manager non risponde, avvisare l'utente che sarà necessario deployarne uno nuovo dato che quello
     salvato non esiste più (magari perchè il container di ganache è stato riavviato)
4.2) Se risponde tutto ok e salvarsi in una variabile della classe l'oggetto contratto dell'on-chain manager

5) Se tutto è andato a buon fine, salvare nel main le variabili relative a:
    - dizionario config che contiene le variabili di configurazione
    - variabili provider delle 4 shard
    - variabile contratto dell'on-chain manager

NB: Capire se, nel caso si verificasse un eccezione durante il bootstrap relativa alla presenza dell'on-chain manager,
    deployarlo con un account di default oppure aspettare che l'utente faccia il login e deployarlo con il suo account.
    
Alternative flow:
5) Se si verifica un'eccezione e bisogna deployare nuovamente o come prima volta l'on-chain manager, 
   chiedere all'utente conferma
5.1) Se l'utente conferma, deployare l'on-chain manager, salvarne indirizzo e abi e svuotare i file delle abi delle 
     shard 1, 2 e 3
'''


class Bootstrap:

    """
    Costruttore della classe
    Legge il file di configurazione 'config.json' e salva le variabili di configurazione nella variabile json_config
    Ottiene le connessioni alle quattro shard utilizzate dal programma
    Legge o effettua il deploy dell'on-chain manager
    """

    def __init__(self):

        self.__config_path = "../Config/config.json"
        self.__config_params = ConfigParams(self.__config_path)

        solcx.install_solc(
            self.__config_params.get_pragma_solidity_on_chain_manager())

        self.__connections = self.__get_connections()
        self.__on_chain_manager_contract = self.__get_on_chain_manager_contract()

    # AGGIUNGERE FUNZIONE PER CONTROLLARE INTEGRITà FILE ABIS? si potrebbe controllare se il json.loads()
    # non solleva eccezioni, non posso controllare comunque se le abi sono giuste

    """
    FUNZIONE PER CONTROLLARE L'INTEGRITà DEL FILE CONFIG.JSON
    Se non sono presenti tutti i parametri richiesti termina l'esecuzione del programma
    :param: dizionario estratto dal file config.json
    """
    def __check_config_integrity(self, json_config):
        required_parameters = ["url_shard_0", "url_shard_1", "url_shard_2", "url_shard_3", "path_abis_shard_0",
                               "path_abis_shard_1", "path_abis_shard_2", "path_abis_shard_3",
                               "path_smart_contract_on_chain_manager", "pragma_solidity_on_chain_manager",
                               "name_on_chain_manager_contract"]
        for parameter in required_parameters:
            if parameter not in json_config.keys():
                print("Errore: \n"
                      + "File di configurazione non conforme alle specifiche \n"
                      + "Parametro mancante: " + parameter
                      + "Interruzione programma")
                exit(1)

        self.check_url(json_config["url_shard_0"])
        self.check_url(json_config["url_shard_1"])
        self.check_url(json_config["url_shard_2"])
        self.check_url(json_config["url_shard_3"])
        self.check_path(json_config["path_abis_shard_0"])
        self.check_path(json_config["path_abis_shard_1"])
        self.check_path(json_config["path_abis_shard_2"])
        self.check_path(json_config["path_abis_shard_3"])
        self.check_path(json_config["path_smart_contract_on_chain_manager"])

    """
    Funzione per verificare che un URL sia contenga la regex 'http://'
    Termina il programma se l'URL non soddisfa questa condizione
    :param: url da controllare
    """
    def check_url(self, url):
        reg_ex_urls = "http://.*"
        if re.search(reg_ex_urls, url) is None:
            print("Errore: \n"
                  + "Il parametro '" + url + "' non è un URL che che rispetta le specifiche \n"
                  + "Interruzione del programma")
            exit(1)

    """
    Funzione per controllare se una path esiste
    Se la path non esiste termina l'esecuzione del programma
    :param: path da controllare
    """
    def check_path(self, path):
        if not os.path.exists(path):
            print("Errore: \n"
                  + "La path '" + path + "' non esiste \n"
                  + "Interruzione del programma")
            exit(1)
    """
    Funzione per leggere il JSONObject dal file config.json
    Nel file config.json andranno inserite le variabili da utilizzare per il programma
    :return: dizionario contenente le variabili di configurazione
    """
    def __read_config(self):
        try:
            with open(self.__config_path, 'r') as file_config:
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

    '''
    Funzione per ottenere la connessione alle quattro shard utilizzate
    :return: un vettore contenente le connessioni alle quattro shard
    :return: False se la connessione non è riuscita
    '''

    def __try_connections(self):
        try:
            shard_0 = Web3(Web3.HTTPProvider(
                self.__config_params.get_url_shard_0()))  # on-chain
            shard_1 = Web3(Web3.HTTPProvider(
                self.__config_params.get_url_shard_1()))  # shard 1
            shard_2 = Web3(Web3.HTTPProvider(
                self.__config_params.get_url_shard_2()))  # shard 2
            shard_3 = Web3(Web3.HTTPProvider(
                self.__config_params.get_url_shard_3()))  # shard 3
        except Exception as e:
            clear_terminal()
            print("Errore:")
            print(e)
            return False

        if (not shard_0.isConnected()) or (not shard_1.isConnected()) or (not shard_2.isConnected()) \
                or (not shard_3.isConnected()):
            clear_terminal()
            print(
                "Errore: \n"
                + "Non è stato possibile effettuare la connessione a una o più shard"
            )
            return False
        return [shard_0, shard_1, shard_2, shard_3]

    """
    Funzione che richiama try_connections e in caso di fallimento della connessione chiede all'utente se voglia
    tentare nuovamente a connettersi, altrimenti esce dal programma
    :return: vettore delle connessioni alle quattro shard
    """

    def __get_connections(self):
        connections = self.__try_connections()
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
                connections = self.__try_connections()
        return connections

    """
    Funzione per controllare se siano salvate le ABI dell'onchain manager sul file
    :return: False se non sono salvate alcune ABI sul file 'onchain.json'
    :return: oggetto contratto dell'on-chain manager
    """

    def __read_and_try_on_chain_manager(self):
        try:
            with open(self.__config_params.get_path_abis_shard_0(), 'r') as file_abi:
                text_abi = file_abi.read()
                json_abi = json.loads(text_abi)
        except Exception as e:
            clear_terminal()
            print(
                "Errore nella lettura del file contenente le ABI dell'on-chain manager \n"
                + "Interruzione del programma"
            )
            exit(1)

        if len(json_abi.keys()) != 1:
            print(
                "Non è presente alcun on-chain manager salvato"
            )
            return False
        else:
            address = list(json_abi.keys())[0]
            abi = json_abi[address]
            return self.__try_on_chain_manager(address, abi)

    """
    Funzione per provare a chiamare una funzione dell'on chain manager registrato
    :return: False se lo smart contract dell'on-chain manager non risponde o risponde in maniera errata
    :return: oggetto contratto dell'on-chain manager
    """

    def __try_on_chain_manager(self, address_on_chain_manager, abi_on_chain_manager):
        on_chain_manager_contract = self.__connections[0].eth.contract(
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
        if prova in [1, 2, 3]:
            return on_chain_manager_contract
        else:
            return False
    """
    Funzione che utilizza le due sopra per controllare l'esistenza dell'on-chain manager
    In caso non esistesse chiede all'utente se vuole effettuarne il deploy
    Esce dal programma nel caso l'utente non voglia effettuare il deploy dell'on-chan manager
    :return: il contratto dell'on-chain manager
    """

    def __get_on_chain_manager_contract(self):
        on_chain_manager_contract = self.__read_and_try_on_chain_manager()
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
                return self.__deploy_on_chain_manager_with_default_account()
        else:
            return on_chain_manager_contract
    """
    Funzione per effettuare il deploy dell'on-chain manger con un account di default
    :return: oggetto contratto dell'on-chain manager
    """

    def __deploy_on_chain_manager_with_default_account(self):
        # Account di default numero 0
        self.__connections[0].eth.default_account = self.__connections[0].eth.accounts[0]

        try:
            # Installazione della versione del compilatore in base al pragma impostato nel file config.json
            solcx.install_solc(
                self.__config_params.get_pragma_solidity_on_chain_manager())
            solcx.set_solc_version(
                self.__config_params.get_pragma_solidity_on_chain_manager())
        except Exception as e:
            print("Errore durante l'installazione di solc \n"
                  + "Controllare che il pragma di solidity nel file config.json sia scritto in mnodo corretto \n"
                  + "Interruzione del programma")
            exit(1)

        # Compilazione dello smart contract dell'on-chain manager
        try:
            # Compilazione dell'on-chain manager
            compiled_solidity = solcx.compile_files(
                [self.__config_params.get_path_smart_contract_on_chain_manager()])
            # Estrazione delle abi e del bytecode dal compilato
            key = self.__config_params.get_path_smart_contract_on_chain_manager()\
                + ':' + self.__config_params.get_name_on_chain_manager_contract()
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

        contratto = self.__connections[0].eth.contract(
            abi=abi, bytecode=bytecode)

        # esecuzione della transazione di deploy dello smart contract
        try:
            tx_hash = contratto.constructor().transact()
            tx_receipt = self.__connections[0].eth.wait_for_transaction_receipt(
                tx_hash)
        except Exception as exception:
            print("Errore: \n")
            print(exception)
            print(
                "La transazione di deploy dello smart contract non è andata a buon fine")
            print("Interruzione del programma")
            exit(1)

        # creazione dell'oggetto contratto per interagirci
        on_chain_manager_contract = self.__connections[0].eth.contract(
            address=tx_receipt.contractAddress,
            abi=abi
        )

        # salvataggio abi su file
        self.__save_on_chain_manager_abi(tx_receipt.contractAddress, abi)

        print("On-chain manager pubblicato a questo indirizzo: " +
              tx_receipt.contractAddress)

        return on_chain_manager_contract

    """
    Funzione per salvare su file le abi dello smart contract dell'on-chain manager
    Inoltre resetta anche i file delle abi delle varie shard
    """

    def __save_on_chain_manager_abi(self, address, abi):
        result = {address: abi}
        f = open(self.__config_params.get_path_abis_shard_0(), 'w+')
        f.write(json.dumps(result))
        f.close()

        f = open(self.__config_params.get_path_abis_shard_1(), 'w+')
        f.write(json.dumps({}))
        f.close()

        f = open(self.__config_params.get_path_abis_shard_2(), 'w+')
        f.write(json.dumps({}))
        f.close()

        f = open(self.__config_params.get_path_abis_shard_3(), 'w+')
        f.write(json.dumps({}))
        f.close()

    """
    Funzione da utilizzare nel main per ottenere le variabili da utilizzare nel programma
    :return: variabili da utilizzare nel programma, ossia il dizionario delle impostazioni di configurazione, il vettore
    delle connessioni alle quattro shard e l'oggetto contratto dell'on-chain manager
    """

    def get_program_variables(self):
        return self.__config_params, self.__connections, self.__on_chain_manager_contract
