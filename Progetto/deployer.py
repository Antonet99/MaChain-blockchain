import json
import os

from compiler import Compiler


class Deployer:

    # richiesta all'on-chain-manager su quale shard deployare lo smart contract
    def shard_where_deploy(self, onchain):
        try:
            shard_where_deploy = onchain.functions.get_shard_where_deploy().call()
            return shard_where_deploy

        except Exception as exception:
            os.system('clear')
            print("Errore: ")
            print(exception)
            print("La richiesta all'on-chain manager per la shard su cui fare il deploy dello smart contract non è andata a buon fine")
            return

    def blockchain_where_deploy(self, shard_where_deploy):

        with open('nome_file.json') as f:
            data = json.load(f)

        s1 = data['url_shard_1']
        s2 = data['url_shard_2']
        s3 = data['url_shard_3']  # cambiare

        if shard_where_deploy < 1 or shard_where_deploy > 3:
            print(
                "Errore: \n"
                + "La shard su cui effettuare il deploy dello smart contract deve essere compresa tra 1 e 3"
            )

        if shard_where_deploy == 1:
            blockchain_where_deploy = s1
        elif shard_where_deploy == 2:
            blockchain_where_deploy = s2
        elif shard_where_deploy == 3:
            blockchain_where_deploy = s3

        return blockchain_where_deploy

    def estimate_gas(self, on_chain_manager, compiled_solidity, abi_to_deploy, bytecode_to_deploy):

        blockchain_where_deploy = self.blockchain_where_deploy()
        shard_where_deploy = self.shard_where_deploy()

        # stima del gas necessario per fare il deploy dello smart contract e per aggiornare l'on-chain manager
        contratto = blockchain_where_deploy.eth.contract(
            abi=abi_to_deploy, bytecode=bytecode_to_deploy)

        # gas price fisso impostato da noi (Gwei)
        with open('nome_file.json') as f:
            data = json.load(f)

        gas_price_shard = data['gas_price_shard']
        gas_price_onchain = data['gas_price_onchain']

        # stima vera e propria del gas necessario per le due transazioni
        stima_gas_deploy = contratto.constructor().estimate_gas()

        stima_gas_aggiornamento_on_chain = on_chain_manager.functions.register_contract(
            '0x0000000000000000000000000000000000000000', shard_where_deploy).estimate_gas()

        # stima dei costi delle due transazioni, in Gwei, tenendo conto del presso fisso definito sopra
        stima_costo_deploy = stima_gas_deploy * gas_price_shard
        stima_costo_aggiornamento_onchain = stima_gas_aggiornamento_on_chain * gas_price_onchain

        # MODIFICARE METTENDO COME ACCOUNT GLI INDIRIZZI DELL'UTENTE SULLE VARIE BLOCKCHAIN
        bilancio_onchain_gwei = on_chain_manager.eth.get_balance(
            on_chain_manager.eth.accounts[0])/(10 ^ 9)

        bilancio_shard_gwei = blockchain_where_deploy.eth.get_balance(
            blockchain_where_deploy.eth.accounts[0])/(10 ^ 9)

        print("Bilancio wallet utente sulla shard sulla quale fare il deploy: \n" +
              str(bilancio_shard_gwei)+' Gwei')
        print("Bilancio wallet utente sulla blockchain dell'on-chain manager: \n" +
              str(bilancio_onchain_gwei)+' Gwei')

        if (stima_costo_deploy > bilancio_shard_gwei) or (stima_costo_aggiornamento_onchain > bilancio_onchain_gwei):
            os.system('clear')

            if (stima_costo_deploy > bilancio_shard_gwei):
                print(
                    "Attenzione: \n"
                    + "Il gas a tua disposizione potrebbe non essere sufficiente a completare il deploy dello smart contract sulla shard interessata!"
                )
            if (stima_costo_aggiornamento_onchain > bilancio_onchain_gwei):
                print(
                    "Attenzione: \n"
                    + "Il gas a tua disposizione potrebbe non essere sufficiente a completare l'aggiornamento dell'on-chain manager!"
                )

            print(
                "Se vuoi, puoi comunque procedere e tentare di effettuare il deploy dello smart contract. \n"
                + "Tuttavia se anche solo una delle due transazioni non dovessero andare a buon fine perderai il gas investito. \n"
                + "Vuoi procedere? [S/N]"
            )
            selezione = ''
            selezione = input()
            while (selezione != 's' or selezione != 'n'):
                print("Inserire solo caratteri consentiti (S/N).")
                selezione = input()

            # Decommentare il return e cancellare il pass quando verrà messo in una funzione python vera e propria
            if selezione == 'n':
                pass
                return

    def deploy_contract(self, compiled_solidity, abi_to_deploy, bytecode_to_deploy):

        try:
            tx_hash = contract.constructor().transact()
            tx_receipt = blockchain.eth.wait_for_transaction_receipt(tx_hash)
        except Exception as exception:
            os.system('clear')
            print("Errore: \n")
            print(exception)
            print(
                "La transazione di deploy dello smart contract non è andata a buon fine")
            return None

        contratto_deployato = blockchain.eth.contract(
            address=tx_receipt.contractAddress,
            abi=abi_to_deploy
        )

        print(contratto_deployato.address)
        return contratto_deployato

    def register_contract(self, on_chain_manager, contratto_deployato, shard_where_deploy):
        try:
            on_chain_manager.functions.register_contract(
                contratto_deployato.address, shard_where_deploy).transact()
        except Exception as exception:
            os.system('clear')
            print("Errore: \n")
            print(exception)
            print(
                "La transazione di aggiornamento dell'on-chain manager non è andata a buon fine")

        print(on_chain_manager.functions.get_shard_where_deploy().call())
