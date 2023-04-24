import transactioner

def menu(config_params, connections, on_chain_manager_contract):
    while True:
        print("Scegli cosa fare: ")
        print("1. Seleziona gli account con cui effettuare le transazioni")
        print("2. Effettua il deploy di uno smart contract")
        print("3. Effettua una transazione su uno smart contract di cui è stato fatto il deploy")
        print("4. Esci")
        choice = input("Scelta: ")

        if choice == "1":
                print("1")
                break
        elif choice == "2":
                print("2")
                break
        elif choice == "3":
                transactioner.choose_smart_contract(config_params, connections, on_chain_manager_contract)
                #break
        elif choice == "4" :
                print("4")
                break
        else :
            print("\nScelta non valida.\n")
