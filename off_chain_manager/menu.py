def menu ():
    print_menu_0()
    selezione = selezione_menu_0()

    if selezione_menu_0 == 4:
        return
    


def print_menu_0 ():
    print("Scegli cosa fare: ")
    print("1: Seleziona gli account con cui effettuare le transazioni")
    print("2: Effettua il deploy di uno smart contract")
    print("3: Effettua una transazione su uno smart contract di cui è stato fatto il deploy")
    print("4: Esci")
    return



def selezione_menu_0():
    selezione = 0
    while (selezione < 1 or selezione > 4):
        try:
            selezione = int(input())
            if (selezione < 1 or selezione > 4):
                print("Inserire un numero tra 1 e 4")
                selezione = 0
        except:
            print("Inserire un numero tra 1 e 4")
            selezione = 0
    
    return selezione

