import json
import os
import ntpath
import solcx
import re

class Compiler:

    def get_path(self):
        path = input("Inserisci il percorso del contratto: ")
        print()
        while not os.path.exists(path):
            print(f"Il file nel percorso {path} non esiste.")
            choice = input("Vuoi inserire un altro percorso (s/n)?: ")
            if choice.lower() == "s":
                path = input("Inserisci il percorso del contratto: ")
            elif choice.lower() == "n":
                return None
            else:
                print("Scelta non valida. Riprova. \n")
        return path

    def read_contract(self):
        """
        Legge il file del contratto situato al percorso specificato e restituisce il contenuto nella variabile textfile.
        """

        path = self.get_path()
        if path is None:
            return None, None

        try:
            with open(path, "r") as file:
                textfile = file.read()
                print(
                    f"Il file nel percorso {path} esiste e il suo contenuto è stato letto correttamente.")
                return textfile, path

        except FileNotFoundError:
            print(f"Il file nel percorso {path} non esiste.")
            return None, None

        except PermissionError as e:
            print(f"Non hai i permessi per accedere al file {path}.")
            print(f"Dettagli dell'errore: {e}")
            return None, None

        except OSError as e:
            print(
                f"C'è stato un errore di sistema nell'apertura del file {path}.")
            print(f"Dettagli dell'errore: {e}")
            return None, None

    def get_solidity_version(self, text_contract):

        # espressione regolare utilizzata per trovare dentro allo smart contract la versione di solidity richiesta
        pragma_expression_1 = "pragma solidity [<,>,=,^][<,>,=,^][0-9]\.[0-9]\.[0-9]"

        # ricerca della stringa pragma dentro lo smart contract tramite espressione regolare
        pragma = re.search(pragma_expression_1, text_contract)

        # se la versione di solidity è stata trovata, la ritorna
        if pragma is not None:
            # rimozione dei caratteri superflui
            text_version = pragma.group()
            return text_version.translate(str.maketrans('', '', 'pragma solidity><=^;'))
        else:
            pragma_expression_2 = "pragma solidity [<,>,=,^][0-9]\.[0-9]\.[0-9]"
            pragma = re.search(pragma_expression_2, text_contract)
            text_version = pragma.group()
            return text_version.translate(str.maketrans('', '', 'pragma solidity><=^;'))

    def get_imports(self, text_contract):

        # espressione regolare utilizzata per trovare dentro allo smart contract gli import
        regular_expression = "import .*;"

        # ricerca della stringa import dentro lo smart contract tramite espressione regolare
        match = re.findall(regular_expression, text_contract)

        chars_to_remove = [';', '"']
        imports = ''

        for index, item in enumerate(match):
            import_text = item.split()[1]
            import_text = import_text.translate(
                str.maketrans('', '', ''.join(chars_to_remove)))
            if index == 0:
                imports = imports + import_text
            else:
                imports = imports + ', ' + import_text

        return imports

    def compile_smart_contract(self):

        text_contract, path = self.read_contract()

        if text_contract is None and path is None:
            return None, None, None

        try:
            # Legge la versione di Solidity e imports richiesti dallo smart contract
            solidity_version = self.get_solidity_version(text_contract)
            imports = self.get_imports(text_contract)

            solcx.install_solc(solidity_version)
            solcx.set_solc_version(solidity_version)

            compiled_solidity = solcx.compile_files([path], allow_paths=imports)

            # Estrae i bytecode e ABIs degli smart contract compilati
            bytecodes = []
            for key in compiled_solidity.keys():
                bytecodes.append(compiled_solidity[key]['bin'])

            abis = []
            for key in compiled_solidity.keys():
                abis.append(json.loads(json.dumps(
                    compiled_solidity[key]))['abi'])

            if len(bytecodes) > 1:
                abi_to_deploy, bytecode_to_deploy, contract_name = self.choose_contract(
                    compiled_solidity, abis, bytecodes)

            else:
                abi_to_deploy = abis[0]
                bytecode_to_deploy = bytecodes[0]
                contract_name = list(compiled_solidity.keys())[0].split(':')[1]

            if bytecode_to_deploy == '':
                print("Attenzione! Non è stato possibile compilare lo smart contract. \n")
                return None, None, None

            return abi_to_deploy, bytecode_to_deploy, contract_name

        except Exception as exception:
            print("Attenzione! E' stato generato il seguente errore durante la compilazione: \n" + str(exception) )
            print()
            print("Lo smart contract non è stato compilato correttamente \n")
            return None, None, None

    def choose_contract(self, compiled_solidity, abis, bytecodes):

        if len(bytecodes) > 1:

            os.system('clear')
            print("Nel file sol appena compilato sono presenti più di uno smart contract. \n"
                  + "Gli smart contract compilati sono: "
                  )

            possibili_selezioni = []

            for index, key in enumerate(compiled_solidity.keys()):
                if bytecodes[index] != '':
                    print(str(index) + ') ' + str(key).split(':')[1])
                    possibili_selezioni.append(str(index))
                else:
                    print(str(index) + ') ' + str(key).split(':')
                          [1] + ' [non è possibile effettuarne il deploy]')
            print(
                "NB: Delle interfacce e gli abstract contract non può essere effettuato il deploy.")
            print(
                "Di quale smart contract vuoi fare il deploy? [inserire il numero di fianco al nome dello smart contract]")

            selezione = input()

            while str(selezione) not in possibili_selezioni:
                print(
                    "Inserisci un indice tra quelli degli smart contract di cui è possibile fare il deploy")
                selezione = input()

            indice_selezionato = int(selezione)
            abi_to_deploy = abis[indice_selezionato]
            bytecode_to_deploy = bytecodes[indice_selezionato]
            contract_name = list(compiled_solidity.keys())[indice_selezionato].split(':')[1]
            return abi_to_deploy, bytecode_to_deploy, contract_name

        else:
            if bytecodes[0] == '':
                os.system('clear')
                print("Lo smart contract presente nel file .sol è una interfaccia o un contratto astratto, \n"
                      + "non è quindi possibile effettuarne il deploy")
                return '', ''
            else:
                abi_to_deploy = abis[0]
                bytecode_to_deploy = bytecodes[0]

                return abi_to_deploy, bytecode_to_deploy
