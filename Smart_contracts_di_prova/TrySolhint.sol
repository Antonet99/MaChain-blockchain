// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.0;

contract A {
        
    mapping(address => uint) private shares;

    // Reentrancy vulnerabilities = Avoid state changes after transfer
    function a() external {
        uint amount = shares[msg.sender];
        payable(msg.sender).transfer(amount);
        shares[msg.sender] = 0;
    }

    // No vulnerble version 
    function b() external {
        uint amount = shares[msg.sender];
        shares[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }

}