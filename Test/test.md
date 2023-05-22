## Test effettuati

**Classe `Login`:**

    - Login con troppi tentativi
    - Eseguire funzioni senza aver effettuato il login

**Classe `Bootstrap`:**

    - File config.json assente
    - File config.json non conforme
    - Parametri di configurazione errati
    - Container ganache spenti, uno e più di uno
    - Errore compilazione on-chain manager
    - Errore deploy on-chain manager
    - Contratto on-chain manager non risponde
    - Contratto on-chain manager non funzionante
    - File ABIs non presenti
    - On-chain manager manda risposte errate

**Classe `Register`:**

    - Registrazione con password non conforme ai parametri impostati
    - Registrazione con chiavi non conformi ai parametri impostati

**Classe `Compiler`:**

    - Compilazione di uno smart contract errato

**Classe `Deployer`:**

    - Deploy di smart contract con bilancio insufficiente
    - Deploy effettuato ma on-chain manager non risponde per registrarlo
    - On-chain manager non risponde alla richiesta di quale shard si trova un contratto

**Classe `Transactioner`:**

    - Errori nel passaggio dei parametri della transazione
    - On-chain manager non risponde alla richiesta di quale shard si trova un contratto
    - Errore di esecuzione della funzione dello smart contract richiesta



