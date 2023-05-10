# ProgettoSSB

Repository per il progetto di **Software Cybersecurity and Blockchain**.

# Guida all'uso

Questi sono i passaggi per poter utilizzare la nostra app.

## 1. Installazione di Docker

Installa Docker sul tuo pc.

## 2. Git clone

Clona la repository del progetto

## 3. Deploy delle blockchain

Nella directory principale del progetto è presente un file chiamato docker-compose.yml. Apri una finestra del terminale del tuo pc e dopo esserti posizionato nella directory del progetto, esegui il seguente comando:

    docker compose up -d

## 4. Deploy del programma

Ora è il turno del deploy del programma. Nella stessa directory di prima, esegui il comando:

    docker run -ti --network="desktop_progetto" --name maChain
    --publish 8089:8089 andreaciv/progetto_ssb_gruppo_3

## 5. Apertura del programma

Ora puoi usare il programma.
