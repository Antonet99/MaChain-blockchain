// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.16;

contract SimpleStorage {
    uint public storedData = 5;

    function set(uint x) public {
        storedData = x;
    }

    function get() public view returns (uint) {
        return storedData;
    }

    //function destruct() public {
    //   selfdestruct(payable(address(this)));
    //}
}
