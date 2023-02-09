// SPDX-License-Identifier: MIT

pragma solidity >=0.8.0 <0.9.0;

contract REmonitor {
    // Questo monitor è "corretto" ma non è "trasparente"
    // G(invia -> not F-(leggi))
    // 0 -- invia, altro / dump --> 0
    // 0 -- leggi        / dump --> 1
    // 1 -- leggi, altro / dump --> 1
    // 1 -- invia        / halt --> 1
    enum Stato {s0, s1}
    enum Evento {invia, leggi, altro}

    Stato public st;

    modifier noSendAfterRead (Evento ev) {
        require(!((st==Stato.s1)&&(ev==Evento.invia)),"No send after read");
        if ((ev==Evento.leggi) && (st==Stato.s0)) {
            st=Stato.s1;
        }
        _;
    }

}

contract Prova is REmonitor {
    event Messaggio(Evento msgEv);

    function leggeEvento() public noSendAfterRead(Evento.leggi) returns (Evento) {
        // fa qualche cosa
        emit Messaggio(Evento.leggi);
        return Evento.leggi;
    }

    function inviaEvento() public noSendAfterRead(Evento.invia) returns (Evento) {
        // fa qualche cosa
        emit Messaggio(Evento.invia);
       return Evento.invia;
    }

    function altroEvento() public noSendAfterRead(Evento.altro) returns (Evento) {
        // fa qualche cosa
        emit Messaggio(Evento.altro);
       return Evento.altro;
    }

}