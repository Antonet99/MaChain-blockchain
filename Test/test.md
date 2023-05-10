## Test effettuati

**Classe `Login`:**

    - Login con troppi tentativi
    - Eseguire funzioni senza aver effettuato il login

**Classe `Bootstrap`:**

    - File config.json assente
    - File config.json non conforme
    - Parametri di configurazione errati

## Test da effettuare:

    -Container ganache spenti, uno e più di uno
    -Errore compilazione on-chain manager
    -Errore deploy on-chain manager
    -Contratto on-chain manager non risponde
    -Contratto on-chain manager non funzionante
    -File ABIs non presenti
    -On-chain manager manda risposte errate
    -Registrazione con password non conforme ai parametri impostati
    -Registrazione con chiavi non conformi ai parametri impostati
    -Compilazione di uno smart contract errato
    -Tentativo di deploy con bilancio non sufficiente
    -Deploy effettuato ma on-chain manager non risponde per registrarlo
    -Errore nella scrittura delle abi del contratto appena deployato
    -On-chain manager non risponde alla richiesta di quale shard si trova un contratto
    -Parametri di input della funzione richiesta non conformi
    -Errore di esecuzione della funzione dello smart contract richiesta