// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
//pragma experimental SMTChecker;

interface on_chain_manager_interface {
    function register_contract (address contract_address, uint8 shard_number) external;
    function remove_contract (address contract_address, uint8 shard_number) external;
    function get_shard_where_deploy () external view returns (uint8 shard_number);
    function check_shard_where_contract (address contract_address, uint8 shard_number) external view returns (bool exists);
}

contract on_chain_manager is on_chain_manager_interface {

    // Evento emesso quando uno smart contract viene registrato, prende come parametri il numero della shard
    // sul quale è stato deployato e il suo indirizzo
    event Contract_registered (address contract_address, uint8 shard_number);
    event Contract_removed (address contract_address, uint8 shard_number);

    // Mapping che memorizza quanti smart contract sono stati deployati sulle singole shard
    mapping(uint8 => uint256) internal number_of_contracts;

    // Mapping che memorizza, per ogni smart contract, il numero della shard sul quale è stato deployato
    //mapping (address => uint8) smart_contracts;

    // Struct per memorizzare contratti
    struct Contract {
        address contract_address;
        uint8 shard_number;
    }
    // Array degli smart contract registrati
    Contract[] internal contracts;

    // Funzione per rimuovere un contratto dall'array
    function remove (uint index) private {
        require (index < contracts.length);

        for (uint i = index; i<contracts.length-1; i++){
            contracts[i] = contracts[i+1];
        }
        contracts.pop();
    }

    // Funzione per verificare che due struct contratto siano uguali
    function contract_equals (Contract memory a, Contract memory b) private pure returns (bool equal) {
        if (a.contract_address == b.contract_address && a.shard_number == b.shard_number)
            return true;
        return false;
    }

    // Funzione che registra il deploy di un nuovo smart contract
    function register_contract (address contract_address, uint8 shard_number) public override {
        require(shard_number >= 1 && shard_number <= 3, "Il numero della shard dove e' stato deployato lo smart contract deve essere compreso tra 1 e 3.");
        Contract memory contratto = Contract(contract_address, shard_number);
        contracts.push(contratto);
        number_of_contracts[shard_number]++;
        emit Contract_registered(contract_address, shard_number);
    }

    // Funzione per elminare uno smart contract
    function remove_contract (address contract_address, uint8 shard_number) public override {
        require(shard_number >= 1 && shard_number <= 3, "Il numero della shard dove e' stato deployato lo smart contract deve essere compreso tra 1 e 3.");
        Contract memory contratto = Contract(contract_address, shard_number);
        for (uint i=0; i<contracts.length; i++) {
            if (contract_equals(contratto, contracts[i])){
                remove(i);
            }
        }
        number_of_contracts[shard_number]--;
        emit Contract_removed(contract_address, shard_number);
    }

    // Funzione che restituisce il numero della shard sulla quale sono stati deployati meno smart contract e quindi quella dove fare il deploy di uno nuovo
    function get_shard_where_deploy () public view override returns (uint8 shard_number) {

        uint256 contracts_on_1 = number_of_contracts[1];
        uint256 contracts_on_2 = number_of_contracts[2];
        uint256 contracts_on_3 = number_of_contracts[3];

        if (contracts_on_1 <= contracts_on_2 && contracts_on_1 <= contracts_on_3) {
            return 1;
        }

        if (contracts_on_2 <= contracts_on_1 && contracts_on_2 <= contracts_on_3) {
            return 2;
        }

        if (contracts_on_3 <= contracts_on_1 && contracts_on_3 <= contracts_on_2) {
            return 3;
        }
    }

    // Funzione che restituisce controlla se il contratto a quell'indirizzo su quella shard esiste
    function check_shard_where_contract (address contract_address, uint8 shard_number) public view override returns (bool exists) {
        Contract memory contratto = Contract(contract_address, shard_number);
        for (uint i=0; i<contracts.length; i++) {
            if (contract_equals(contratto, contracts[i])){
                return true;
            }
        }
        return false;
    }
    
}