import json
import os

from compiler import Compiler
from support_functions import clear_terminal


class Deployer:

    def __init__(self, config_params):
        self.__config_params = config_params

    def shard_where_deploy(self, connections, on_chain_manager_contract):

        try:
            number_shard_where_deploy = on_chain_manager_contract.functions.get_shard_where_deploy().call()
        except:
            print("OnChain Manager non disponibile, deploy non riuscito! \n")
            return None, None

        if number_shard_where_deploy < 1 or number_shard_where_deploy > 3:
            print(
                "Errore: \n"
                + "La shard su cui effettuare il deploy dello smart contract deve essere compresa tra 1 e 3"
            )
            return None, None

        if number_shard_where_deploy == 1:
            shard_where_deploy = connections[1]
        elif number_shard_where_deploy == 2:
            shard_where_deploy = connections[2]
        elif number_shard_where_deploy == 3:
            shard_where_deploy = connections[3]

        return shard_where_deploy, number_shard_where_deploy

    def estimate_gas(self, connections, shard_where_deploy, on_chain_manager_contract, abi_to_deploy, bytecode_to_deploy, number_shard_where_deploy):

        # stima del gas necessario per fare il deploy dello smart contract e per aggiornare l'on-chain manager
        contratto = shard_where_deploy.eth.contract(
            abi=abi_to_deploy, bytecode=bytecode_to_deploy)

        # gas price fisso impostato da noi (Gwei)
        gas_price_onchain = self.__config_params.get_gas_price_onchain()
        gas_price_shard = self.__config_params.get_gas_price_shard()

        # stima vera e propria del gas necessario per le due transazioni
        stima_gas_deploy = contratto.constructor().estimate_gas()

        stima_gas_aggiornamento_on_chain = on_chain_manager_contract.functions.register_contract(
            '0x0000000000000000000000000000000000000000', number_shard_where_deploy).estimate_gas()

        # stima dei costi delle due transazioni, in Gwei, tenendo conto del presso fisso definito sopra
        stima_costo_deploy = stima_gas_deploy * gas_price_shard
        stima_costo_aggiornamento_onchain = stima_gas_aggiornamento_on_chain * gas_price_onchain

        bilancio_onchain_gwei = connections[0].eth.get_balance(
            connections[0].eth.default_account)

        bilancio_shard_gwei = shard_where_deploy.eth.get_balance(
            shard_where_deploy.eth.default_account)

        print("Bilancio wallet utente sulla shard sulla quale fare il deploy: " +
              str(bilancio_shard_gwei)+' wei')
        print("Bilancio wallet utente sulla blockchain dell'on-chain manager: " +
              str(bilancio_onchain_gwei)+' wei')

        if (stima_costo_deploy > bilancio_shard_gwei) or (stima_costo_aggiornamento_onchain > bilancio_onchain_gwei):
            if (stima_costo_deploy > bilancio_shard_gwei):
                print(
                    "Attenzione: \n"
                    + "Il gas a tua disposizione non è sufficiente a completare il deploy dello smart contract sulla shard interessata. \n"
                    + "Il deploy non può essere completato. \n"
                )
            if (stima_costo_aggiornamento_onchain > bilancio_onchain_gwei):
                print(
                    "Attenzione: \n"
                    + "Il gas a tua disposizione non è sufficiente a completare l'aggiornamento dell'on-chain manager. \n"
                    + "Il deploy non può essere completato. \n"
                )

            return False

        return True

    def deploy_contract(self, abi_to_deploy, bytecode_to_deploy, contract_name, connections, on_chain_manager_contract):

        shard_where_deploy, number_shard_where_deploy = self.shard_where_deploy(
            connections, on_chain_manager_contract)
        if shard_where_deploy is None and number_shard_where_deploy is None:
            return
        contract = shard_where_deploy.eth.contract(
            abi=abi_to_deploy, bytecode=bytecode_to_deploy)

        if not self.estimate_gas(connections, shard_where_deploy, on_chain_manager_contract, abi_to_deploy, bytecode_to_deploy, number_shard_where_deploy):
            return None

        try:
            tx_hash = contract.constructor().transact()
            tx_receipt = shard_where_deploy.eth.wait_for_transaction_receipt(
                tx_hash)
        except Exception as exception:
            print("Errore: \n")
            print(exception)
            print(
                "La transazione di deploy dello smart contract non è andata a buon fine \n")
            return None

        contratto_deployato = shard_where_deploy.eth.contract(
            address=tx_receipt.contractAddress,
            abi=abi_to_deploy
        )

        print("Indirizzo dello smart contract: ", contratto_deployato.address)
        print()
        self.register_contract(on_chain_manager_contract,
                               contratto_deployato, number_shard_where_deploy)
        self.save_sc_datas(contratto_deployato.address, abi_to_deploy,
                           number_shard_where_deploy, contract_name)

    def register_contract(self, on_chain_manager, contratto_deployato, number_shard_where_deploy):
        try:
            on_chain_manager.functions.register_contract(
                contratto_deployato.address, number_shard_where_deploy).transact()
        except Exception as exception:
            os.system('clear')
            print("Errore: \n")
            print(exception)
            print(
                "La transazione di aggiornamento dell'on-chain manager non è andata a buon fine")
            return None

    def save_sc_datas(self, address, abi, number_shard_where_deploy, contract_name):

        result = {address: [abi, contract_name, number_shard_where_deploy]}

        if number_shard_where_deploy == 1:
            file_path = self.__config_params.get_path_abis_shard_1()
        elif number_shard_where_deploy == 2:
            file_path = self.__config_params.get_path_abis_shard_2()
        elif number_shard_where_deploy == 3:
            file_path = self.__config_params.get_path_abis_shard_3()

        if os.path.exists(file_path):
            with open(file_path) as json_file:
                data = json.load(json_file)
                result = data | result
                json_file.close()
        f = open(file_path, 'w+')
        f.write(json.dumps(result))
        f.close()
