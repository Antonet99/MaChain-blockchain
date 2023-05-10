// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.16;

contract SimpleStorage {
    uint256 public storedData = 5;

    function set(uint256 x) public {
        storedData = x;
    }

    function get() public view returns (uint256) {
        return storedData;
    }

    //function destruct() public {
    //   selfdestruct(payable(address(this)));
    //}
}
