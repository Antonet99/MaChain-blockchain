import json
import os
import ntpath
import solcx
from solcx import compile_standard
import re

from support_functions import clear_terminal


class Compiler:

    def get_path(self):
        path = input("Inserisci il percorso del contratto: ")
        return path

    def get_file_name(self, path):
        try:
            filename = ntpath.basename(path)
            return filename
        except AttributeError:
            print("Errore: il percorso del contratto non è stato ancora specificato.")

    def read_contract(self):
        """
        Legge il file del contratto situato al percorso specificato e restituisce il contenuto nella variabile textfile.
        """

        path = self.get_path()

        try:
            with open(path, "r") as file:
                textfile = file.read()
                print(
                    f"Il file nel percorso {path} esiste e il suo contenuto è stato letto correttamente.")
                return textfile, path

        except FileNotFoundError:
            print(f"Il file nel percorso {path} non esiste.")
            return self.ask_for_new_path()

        except PermissionError as e:
            print(f"Non hai i permessi per accedere al file {path}.")
            print(f"Dettagli dell'errore: {e}")
            return self.ask_for_new_path()

        except OSError as e:
            print(
                f"C'è stato un errore di sistema nell'apertura del file {path}.")
            print(f"Dettagli dell'errore: {e}")
            return self.ask_for_new_path()

    def ask_for_new_path(self):
        while True:
            choice = input("Vuoi inserire un altro percorso? (Y/N) ")
            if choice.upper() == "Y":
                return self.read_contract()
            elif choice.upper() == "N":
                print("Arrivederci!")
                return ""
            else:
                print("Scelta non valida. Riprova.")

    def get_solidity_version(self, text_contract):

        # espressione regolare utilizzata per trovare dentro allo smart contract la versione di solidity richiesta
        pragma_expression = "pragma solidity .*;"

        # ricerca della stringa pragma dentro lo smart contract tramite espressione regolare
        pragma = re.search(pragma_expression, text_contract)

        # se la versione di solidity è stata trovata, la ritorna
        if pragma:
            # rimozione dei caratteri superflui
            text_version = pragma.group()
            print(text_version)

            return text_version.translate(str.maketrans('', '', 'pragma solidity><=^;'))

        else:
            return None

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

        try:
            # Legge la versione di Solidity e imports richiesti dallo smart contract
            solidity_version = self.get_solidity_version(text_contract)
            imports = self.get_imports(text_contract)

            solcx.install_solc(solidity_version)
            solcx.set_solc_version(solidity_version)

            compiled_solidity = solcx.compile_files(
                [path], allow_paths=imports)

            # Estrae i bytecode e ABIs degli smart contract compilati
            bytecodes = []
            for key in compiled_solidity.keys():
                bytecodes.append(compiled_solidity[key]['bin'])

            abis = []
            for key in compiled_solidity.keys():
                abis.append(json.loads(json.dumps(
                    compiled_solidity[key]))['abi'])

            if len(bytecodes) > 1:
                abi_to_deploy, bytecode_to_deploy = self.choose_contract(
                    compiled_solidity, abis, bytecodes)

            else:
                abi_to_deploy = abis[0]
                bytecode_to_deploy = bytecodes[0]

            if bytecode_to_deploy == '':
                print("Attenzione! Non è stato possibile compilare lo smart contract.")
                return None, None

            return abi_to_deploy, bytecode_to_deploy

        except Exception as exception:
            # clear_terminal()
            jsonError = json.loads(json.dumps(exception.__dict__))
            print("Attenzione! E' stato generato il seguente errore durante la compilazione: \n" + jsonError["stderr_data"]
                  + "In " + "\"" + jsonError["command"][1] + "\"" +
                  ", con return code: " + str(jsonError["return_code"]) + ".")
            return None, None

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
            return abi_to_deploy, bytecode_to_deploy

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

            # controllino in più che lo smart contract selezionato sia effettivamente deployabiles
        if bytecode_to_deploy == '':
            print(
                'Errore, dello smart contract da te selezionato non può essere fatto il deploy')
            return '', ''
