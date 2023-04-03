import json
from solcx import compile_standard


def read_contract():
    """
    Legge il file del contratto situato al percorso specificato e restituisce il contenuto nella variabile text_file.
    """

    path = input("Inserisci il percorso del contratto: ")

    try:
        with open(path, "r") as file:
            text_file = file.read()
            print(
                f"Il file nel percorso {path} esiste e il suo contenuto è stato letto correttamente.")

            return text_file

    except FileNotFoundError:
        print("Il file non esiste.")

        while True:
            choice = input("Vuoi inserire un altro percorso? (Y/N) ")
            if choice.upper() == "Y":
                break
            elif choice.upper() == "N":
                print("Arrivederci!")
                return ""
            else:
                print("Scelta non valida.")


def compile_contract():
    """
    Compila il file del contratto situato al percorso specificato e restituisce il bytecode e l'ABI.
    """

    text_file = read_contract()

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"prova_on_chain.sol": {"content": text_file}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                    }
                }
            },
        },
        solc_version='0.8.0',
    )

    bytecode = compiled_sol["contracts"]["prova_on_chain.sol"]["on_chain_manager"]["evm"]["bytecode"]["object"]
    abi = json.loads(compiled_sol["contracts"]["prova_on_chain.sol"]
                     ["on_chain_manager"]["metadata"])["output"]["abi"]

    return bytecode, abi


def deploy_on_chain_manager(onchain, abi, bytecode):
    """
    Deploy dello smart contract su On Chain Manager e creazione di un oggetto contratto per interagire con esso.

    Parametri:
        onchain (Web3): Un'istanza della classe Web3 connessa al nodo Ethereum in cui verrà deployato il contratto.
        abi (str): abi dell'applicazione dello smart contract
        bytecode (str): bytecode dello smart contract

    Restituisce:
        contract (Contract): Un'istanza della classe Contract che rappresenta il contratto deployato.
    """
    # deploy dello smart contract dell'onchain manager
    abi, bytecode = compile_contract()

    On_Chain_Manager = onchain.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = On_Chain_Manager.constructor().transact()
    tx_receipt = onchain.eth.wait_for_transaction_receipt(tx_hash)

    # creazione dell'oggetto contract per lo smart contract dell'onchain manager in modo da poterci interagire
    on_chain_manager = onchain.eth.contract(
        address=tx_receipt.contractAddress,
        abi=abi
    )

    return on_chain_manager
