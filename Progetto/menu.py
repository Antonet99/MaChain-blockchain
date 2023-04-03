def menu():
    while True:

        print("Scegli cosa fare: ")
        print("1. Seleziona gli account con cui effettuare le transazioni")
        print("2. Effettua il deploy di uno smart contract")
        print("3. Effettua una transazione su uno smart contract di cui è stato fatto il deploy")
        print("4. Esci")
        choice = input("Scelta: ")

        match choice:
            case "1":
                print("1")
                break
            case "2":
                print("2")
                break
            case "3":
                print("3")
                break
            case "4":
                print("4")
                return
            case _:
                print("\nScelta non valida.\n")


menu()
