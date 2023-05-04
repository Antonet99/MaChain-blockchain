def menu():
    while True:
        print("Scegli cosa fare: ")
        print("1. Seleziona gli account con cui effettuare le transazioni")
        print("2. Effettua il deploy di uno smart contract")
        print("3. Effettua una transazione su uno smart contract di cui è stato fatto il deploy")
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
            '''
            transactioner.choose_smart_contract(
                config_params, connections, on_chain_manager_contract)
            '''
            # break
        elif choice == "3":
            logged_in = False
            logout = Login()
            logout.logout(connections)
        elif choice == "4":
            print("Arrivederci.")
            return
        else:
            print("\nScelta non valida.\n")
