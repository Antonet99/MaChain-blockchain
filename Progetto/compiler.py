import json
import os
import ntpath
from solcx import compile_standard
import re


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

        path = self.get_path()  # chiedere

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
            match choice.upper():
                case "Y":
                    return self.read_contract()
                case "N":
                    print("Arrivederci!")
                    return ""
                case _:
                    print("Scelta non valida. Riprova.")

    def get_solidity_version(self, path):

        with open(path, 'r') as f:

            # legge il contenuto del file
            file = f.read()

            # espressione regolare utilizzata per trovare dentro allo smart contract la versione di solidity richiesta
            pragma_expression = "pragma solidity .*;"

            # ricerca della stringa pragma dentro lo smart contract tramite espressione regolare
            pragma = re.search(pragma_expression, file)

            # se la versione di solidity è stata trovata, la ritorna
            if pragma:
                # rimozione dei caratteri superflui
                text_version = match.group()
                return text_version
            else:
                return None

    def get_imports(self):

        file = self.read_contract()

        # espressione regolare utilizzata per trovare dentro allo smart contract gli import
        regular_expression = "import .*;"

        # ricerca della stringa import dentro lo smart contract tramite espressione regolare
        match = re.findall(regular_expression, file)

        # caratteri da rimuovere per rimanere con la stringa composta solo dai nomi dei contratti importati
        chars_to_remove = [';', '"']

        # rimozione dei caratteri
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

    def compile_smart_contract(self, path):

        try:
            # Legge la versione di Solidity e imports richiesti dallo smart contract
            text_version = self.get_solidity_version()
            imports = self.get_imports()

            solcx.set_solc_version_pragma(text_version, check_new=True)

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

            return compiled_solidity, abis, bytecodes

        except Exception as exception:
            os.system('clear')
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

        else:
            if bytecodes[0] == '':
                os.system('clear')
                print("Lo smart contract presente nel file .sol è una interfeccia o un contratto astratto, \n"
                      + "non è quindi possibile effettuarno il deploy")
        # return
            else:
                abi_to_deploy = abis[0]
                bytecode_to_deploy = bytecodes[0]

        # controllino in più che lo smart contract selezionato sia effettivamente deployabiles
    if bytecode_to_deploy == '':
        print(
            'Errore, dello smart contract da te selezionato non può essere fatto il deploy')
        # return
