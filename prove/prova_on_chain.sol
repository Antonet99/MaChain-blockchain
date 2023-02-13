// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0;

contract on_chain_manager {

    // Evento emesso quando uno smart contract viene registrato, prende come parametri il numero della shard
    // sul quale è stato deployato e il suo indirizzo
    event Contract_registered (uint8 shard_number, address contract_adress);

    // Mapping che memorizza quanti smart contract sono stati deployati sulle singole shard
    mapping (uint8 => uint256) number_of_contracts;

    // Mapping che memorizza, per ogni smart contract, il numero della shard sul quale è stato deployato
    mapping (address => uint8) smart_contracts;

    // Funzione che registra il deploy di un nuovo smart contract
    function register_contract (address contract_adress, uint8 shard_number) public {
        require(shard_number >= 1 && shard_number <= 3, "Il numero della shard dove e' stato deployato lo smart contract deve essere compreso tra 1 e 3.");
        smart_contracts[contract_adress] = shard_number;
        number_of_contracts[shard_number]++;
        emit Contract_registered(shard_number, contract_adress);
    }

    // Funzione che restituisce il numero della shard sulla quale sono stati deployati meno smart contract e quindi quella dopve fare il deploy di uno nuovo
    function get_shard_where_deploy () public view returns (uint8 shard_number) {

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

    // Funzione che restituisce il numero della shard sul quale si trova lo smart contract del quale è stato passato l'indirizzo
    // Se quell'inidirizzo non è stato trovato ritornerà 0
    function get_shard_where_contract (address contract_adress) public view returns (uint8 shard_number) {
        return smart_contracts[contract_adress];
    }

}