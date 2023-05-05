// SPDX-License-Identifier: GPL-3.0
// N.B. con il commento "//<0.7.0;" dopo non funzionava
pragma solidity >=0.4.16;

contract Greeter {
    string public greeting;

    constructor() public {
        greeting = "Hello";
    }

    function setGreeting(string memory _greeting) public {
        greeting = _greeting;
    }

    function greet() public view returns (string memory) {
        return greeting;
    }
}
