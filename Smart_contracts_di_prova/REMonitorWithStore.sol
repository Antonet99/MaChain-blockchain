// SPDX-License-Identifier: MIT

pragma solidity >=0.8.0 <0.9.0;

contract REmonitor {
    // G(evA U evB)
    // 0 -- evA, evB /store --> 0
    // 0 -- evC      /dump  --> 1
    // 1 -- evA, evB /store --> 0
    // 1 -- evC      /dump  --> 1
    // 0 -- evD      /halt  --> 2
    // 1 -- evD      /halt  --> 2
    // 2 -- evA, evB, evC, evD /halt --> 2

    event Verdetto(string err);

    enum Stato {s0, s1, s2}
    enum Evento {evA, evB, evC, evD}

    bool dumping;

    Stato public st = Stato.s0;
    Evento[] public ev;

    modifier response (Evento current_ev, address ad) {
        require((st!=Stato.s2),"Error state, please reset!");
        if (current_ev==Evento.evD) {
            st = Stato.s2;
            // halt
            emit Verdetto("Event D is not allowed");
         }
        else if ((current_ev==Evento.evA)&&(!dumping)) {
            st=Stato.s0;
            // store
            ev.push(Evento.evA); 
            emit Verdetto("Event A is stored");
        }
        else if ((current_ev==Evento.evA)&&(dumping)) {
            _;
        }
        else if ((current_ev==Evento.evB)&&(!dumping)) {
            st=Stato.s0;
            // store
            ev.push(Evento.evB); 
            emit Verdetto("Event B is stored");
        }
        else if ((current_ev==Evento.evB)&&(dumping)) {
            _;
        }
        else if (current_ev==Evento.evC) {
            st=Stato.s1;
            // dump
            dumping=true;
            for (uint256 i=0; i<ev.length; i++) {
                // in questo monitor facciamo lo store solo di evA
                // quindi l'if è inutile, potremmo usare direttamente
                // Prova(address(ad)).evA();
                if (ev[i]==Evento.evA) Prova(address(ad)).evA();
                else if (ev[i]==Evento.evB) Prova(address(ad)).evB();
             }
            dumping=false;
            delete ev;
            _;
        }
    }

    function reset() public {
        st=Stato.s0;
        dumping=false;
        delete ev;
    }
}

contract Prova is REmonitor {
    event Messaggio(string msgEv);

    function evA() public response(Evento.evA,address(this)) {
        // fa qualche cosa
        emit Messaggio("Evento A");
    }

    function evB() public response(Evento.evB,address(this)) {
        // fa qualche cosa
        emit Messaggio("Evento B");
    }

    function evC() public response(Evento.evC,address(this)) {
        // fa qualche cosa
        emit Messaggio("Evento C");
    }

    function evD() public response(Evento.evD,address(this)) {
        // fa qualche cosa
        emit Messaggio("Evento D");
    }

}