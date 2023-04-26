from bootstrap import Bootstrap
import menu

if __name__ == "__main__":

    bootstrap = Bootstrap()
    config_params, connections, on_chain_manager_contract = bootstrap.get_program_variables()

    menu.menu(config_params, connections, on_chain_manager_contract)
