from transactioner import Transactioner
from deployer import Deployer
from compiler import Compiler
from login import Login
from register import Register


def menu(config_params, connections, on_chain_manager_contract):

    logged_in = False

    while True:

        while not logged_in:
            print("Scegli cosa fare: ")
            print("1. Effettua la registrazione")
            print("2. Effettua il login")
            print("3. Esci")
            choice = input("Scelta: ")

            if choice == "1":
                register = Register(connections, config_params)
                if register.register():
                    logged_in = True
            elif choice == "2":
                login = Login(connections, config_params)
                if login.login():
                    logged_in = True
            elif choice == "3":
                print("Arrivederci.")
                return
            else:
                print("\nScelta non valida.\n")

        print("1. Effettua il deploy di uno smart contract")
        print("2. Effettua una transazione su uno smart contract di cui è stato fatto il deploy")
        print("3. Logout")
        print("4. Esci")
        choice = input("Scelta: ")

        if choice == "1":

            compiler = Compiler()
            abi_to_deploy, bytecode_to_deploy = compiler.compile_smart_contract()

            if abi_to_deploy == None or bytecode_to_deploy == None:
                print("Errore: \n"
                      + "Lo smart contract non è stato compilato correttamente")
                break
            print("Smart contract compilato")

            deployer = Deployer(config_params)
            deployer.deploy_contract(
                abi_to_deploy, bytecode_to_deploy, connections, on_chain_manager_contract)

        elif choice == "2":
            transactioner = Transactioner(config_params, connections, on_chain_manager_contract)
            transactioner.print_and_choose_smart_contract()

            # break
        elif choice == "3":
            logged_in = False
            logout = Login(connections, config_params)
            logout.logout(connections)
        elif choice == "4":
            print("Arrivederci.")
            return
        else:
            print("\nScelta non valida.\n")
