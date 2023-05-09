// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

abstract contract AbstractStorage {
    function retrieve1() public view virtual returns (uint256);
}

contract Storage1 is AbstractStorage{
    uint256 number1;
    function store1(uint256 num) public virtual {
        number1 = num;
    }
    function retrieve1() public view override returns (uint256){
        return number1;
    }
}
contract Storage2 {
    uint256 number2;
    function store2(uint256 num) public {
        number2 = num;
    }
    function retrieve2() public view returns (uint256){
        return number2;
    }
}

contract TryInheritance is Storage1, Storage2 {
    uint256 public number3;
    function store1(uint256 num) public override {
        Storage1.store1(num);
        number3 = num;
    }
}
