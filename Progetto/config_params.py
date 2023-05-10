from support_functions import clear_terminal, check_path, check_url, check_int, check_str
import json


class ConfigParams:

    def __init__(self, config_path):
        self.__config_path = config_path
        self.__config_dict = self.__read_config()
        self.__check_config_integrity()

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
            print(e)
            print(
                "Errore: \n"
                + "Non è stato possibile leggere il file config.json contenente le impostazioni \n"
                + "Interruzione del programma"
            )
            exit(1)

        return json_config

    """
        FUNZIONE PER CONTROLLARE L'INTEGRITà DEL FILE CONFIG.JSON
        Se non sono presenti tutti i parametri richiesti termina l'esecuzione del programma
        :param: dizionario estratto dal file config.json
    """

    def __check_config_integrity(self):
        required_parameters = ["path_user", "url_shard_0", "url_shard_1", "url_shard_2", "url_shard_3", "path_abis_shard_0",
                               "path_abis_shard_1", "path_abis_shard_2", "path_abis_shard_3",
                               "path_smart_contract_on_chain_manager", "pragma_solidity_on_chain_manager",
                               "name_on_chain_manager_contract", "gas_price_onchain", "gas_price_shard"]
        for parameter in required_parameters:
            if parameter not in self.__config_dict.keys():
                print("Errore: \n"
                      + "File di configurazione non conforme alle specifiche \n"
                      + "Parametro mancante: " + parameter
                      + "Interruzione programma")
                exit(1)

        check_url(self.__config_dict["url_shard_0"])
        check_url(self.__config_dict["url_shard_1"])
        check_url(self.__config_dict["url_shard_2"])
        check_url(self.__config_dict["url_shard_3"])
        check_path(self.__config_dict["path_user"])
        check_path(self.__config_dict["path_abis_shard_0"])
        check_path(self.__config_dict["path_abis_shard_1"])
        check_path(self.__config_dict["path_abis_shard_2"])
        check_path(self.__config_dict["path_abis_shard_3"])
        check_path(self.__config_dict["path_smart_contract_on_chain_manager"])
        check_str(self.__config_dict["name_on_chain_manager_contract"])
        check_int(self.__config_dict["gas_price_onchain"])
        check_int(self.__config_dict["gas_price_shard"])

    def get_url_shard_0(self):
        return self.__config_dict["url_shard_0"]

    def get_url_shard_1(self):
        return self.__config_dict["url_shard_1"]

    def get_url_shard_2(self):
        return self.__config_dict["url_shard_2"]

    def get_url_shard_3(self):
        return self.__config_dict["url_shard_3"]

    def get_path_user(self):
        return self.__config_dict["path_user"]

    def get_path_abis_shard_0(self):
        return self.__config_dict["path_abis_shard_0"]

    def get_path_abis_shard_1(self):
        return self.__config_dict["path_abis_shard_1"]

    def get_path_abis_shard_2(self):
        return self.__config_dict["path_abis_shard_2"]

    def get_path_abis_shard_3(self):
        return self.__config_dict["path_abis_shard_3"]

    def get_path_smart_contract_on_chain_manager(self):
        return self.__config_dict["path_smart_contract_on_chain_manager"]

    def get_pragma_solidity_on_chain_manager(self):
        return self.__config_dict["pragma_solidity_on_chain_manager"]

    def get_name_on_chain_manager_contract(self):
        return self.__config_dict["name_on_chain_manager_contract"]

    def get_gas_price_onchain(self):
        return self.__config_dict["gas_price_onchain"]

    def get_gas_price_shard(self):
        return self.__config_dict["gas_price_shard"]
