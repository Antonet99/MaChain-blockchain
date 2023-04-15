from bootstrap import Bootstrap
import menu

if __name__ == "__main__":

    bootstrap = Bootstrap()
    json_config, connections, on_chain_manager_contract = bootstrap.get_program_variables()

    menu.menu()
