pragma solidity ^0.8.0;

contract CarSale {
    // Dichiarare il proprietario del contratto
    address public owner;

    // Dichiarare la struttura dell'automobile
    struct Car {
        string make;
        string model;
        uint year;
        uint price;
        address buyer;
        bool sold;
    }

    // Mapping di automobili in vendita
    mapping (uint => Car) public cars;

    // Contatore per tenere traccia del numero di automobili in vendita
    uint public carCount;

    // Costruttore per impostare il proprietario del contratto all'indirizzo che lo ha creato
    constructor() public {
        owner = msg.sender;
    }

    // Funzione per aggiungere un'auto in vendita
    function addCar(string memory _make, string memory _model, uint _year, uint _price) public {
        require(msg.sender == owner, "Solo il proprietario può aggiungere un'auto in vendita.");

        carCount++;
        cars[carCount] = Car(_make, _model, _year, _price, address(0), false);
    }

    // Funzione per acquistare un'auto
    function buyCar(uint _carId) public payable {
        require(_carId > 0 && _carId <= carCount, "ID auto non valido.");
        require(cars[_carId].sold == false, "Auto già venduta.");
        require(cars[_carId].price <= msg.value, "Prezzo offerto non sufficiente.");

        // Aggiornare i dettagli dell'auto
        cars[_carId].buyer = msg.sender;
        cars[_carId].sold = true;

        // Trasferire il prezzo dell'auto al proprietario del contratto
        owner.transfer(cars[_carId].price);
    }
}
