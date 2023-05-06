from bootstrap import Bootstrap
import menu
import web3

# Se dovesse dare problemi con solc, eseguire comando "pip install py-solc-x==0.8.0" (windows)

if __name__ == "__main__":
    bootstrap = Bootstrap()
    config_params, connections, on_chain_manager_contract = bootstrap.get_program_variables()

    menu.menu(config_params, connections, on_chain_manager_contract)
